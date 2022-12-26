import time
import requests
import sqlite3

def get_item_batches(item_ids, batch_size):
    """Génère des paquets d'IDs d'objets de taille batch_size à partir de la liste item_ids"""
    # Calculez le nombre de paquets d'objets nécessaires
    num_batches = (len(item_ids) + batch_size - 1) // batch_size
    # Générez chaque paquet d'objets
    for batch_index in range(num_batches):
        # Récupérez les IDs des objets de ce paquet
        batch_start = batch_index * batch_size
        batch_end = min((batch_index + 1) * batch_size, len(item_ids))
        yield item_ids[batch_start:batch_end]

def update_prices():
    # Créez une connection à la base de données SQLite
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()

    # Vérifiez si la table "prices" existe déjà
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='prices';")
    if not cursor.fetchone():
        # Créez la table "prices" si elle n'existe pas déjà
        cursor.execute(
            """CREATE TABLE prices (
                item_id INTEGER NOT NULL,
                timestamp INTEGER NOT NULL,
                buy INTEGER,
                sell INTEGER,
                buys_quantity INTEGER,
                sells_quantity INTEGER,
                PRIMARY KEY (item_id, timestamp)
            )"""
        )

    # Récupérez la liste de tous les IDs d'objets de Guild Wars 2
    item_ids = []
    item_ids_response = requests.get("https://api.guildwars2.com/v2/items")
    if item_ids_response.status_code == 200:
        item_ids = item_ids_response.json()

    # Pour chaque paquet d'objets, récupérez les prix et enregistrez-les en base de données
    for batch_ids in get_item_batches(item_ids, 200):
        # Récupérez les prix de ces objets à partir de l'API de commerce
        price_response = requests.get(f"https://api.guildwars2.com/v2/commerce/prices?ids={','.join(str(x) for x in batch_ids)}")
        if price_response.status_code == 200:
            price_data = price_response.json()
            # Pour chaque objet, récupérez ses prix et la quantité vendue et achetée dans les 24 dernières heures, s'ils sont disponibles
            for item_id, item_prices in price_data.items():
                buy_price = item_prices.get("buy", None)
                sell_price = item_prices.get("sell", None)
                buys_quantity = item_prices.get("buys", {}).get("quantity", None)
                sells_quantity = item_prices.get("sells", {}).get("quantity", None)
                # Enregistrez les prix de l'objet en base de données
                cursor.execute(
                    """INSERT INTO prices (item_id, timestamp, buy, sell, buys_quantity, sells_quantity)
                       VALUES (?, ?, ?, ?, ?, ?),
                    (item_id, int(time.time()), buy_price, sell_price, buys_quantity, sells_quantity)
                )
    # Enregistrez les modifications en base de données
    conn.commit()

# Exécutez la fonction update_prices toutes les 5 minutes
while True:
    update_prices()
    time.sleep(300)

