import sqlite3
from collections import defaultdict

# Créez une connection à la base de données SQLite
conn = sqlite3.connect("prices.db")
cursor = conn.cursor()

# Récupérez la liste de tous les IDs d'objets de la base de données
cursor.execute("SELECT DISTINCT item_id FROM prices")
item_ids = [row[0] for row in cursor.fetchall()]

# Pour chaque objet, récupérez ses prix et trouvez le jour de la semaine où son prix d'achat est le moins cher et celui où son prix de vente est le plus cher
for item_id in item_ids:
    # Récupérez les prix de l'objet de la base de données
    cursor.execute("SELECT timestamp, buy, sell FROM prices WHERE item_id=?", (item_id,))
    prices = cursor.fetchall()
    # Si l'objet a des prix enregistrés, trouvez le jour de la semaine où son prix d'achat est le moins cher et celui où son prix de vente est le plus cher
    if prices:
        # Créez des dictionnaires pour stocker le prix d'achat le moins cher et le prix de vente le plus cher de chaque jour de la semaine
        cheapest_buy_prices_by_day = defaultdict(lambda: float("inf"))
        highest_sell_prices_by_day = defaultdict(lambda: float("-inf"))
        # Pour chaque prix, mettez à jour les dictionnaires en fonction du jour de la semaine de l'enregistrement
        for timestamp, buy_price, sell_price in prices:
            day_of_week = datetime.datetime.fromtimestamp(timestamp).weekday()
            # Trouvez le jour de la semaine où le prix d'achat est le moins cher et celui où le prix de vente est le plus cher
            cheapest_buy_day = min(cheapest_buy_prices_by_day, key=cheapest_buy_prices_by_day.get)
            highest_sell_day = max(highest_sell_prices_by_day, key=highest_sell_prices_by_day.get)
            # Ajoutez le jour de la semaine où le prix d'achat est le moins cher et celui où le prix de vente est le plus cher à l'objet en base de données
            cursor.execute("UPDATE items SET cheapest_buy_day=?, highest_sell_day=? WHERE id=?", (cheapest_buy_day, highest_sell_day, item_id))

# Enregistrez les modifications en base de données
conn.commit()

