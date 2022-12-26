import sqlite3
from utils import Database
from PyQt5 import QtWidgets, QtGui

class MainWindow(QtWidgets.QMainWindow, database):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Guild Wars 2 Item Prices")
        self.setWindowIcon(QtGui.QIcon("gw2_icon.png"))

        # Créez une connection à la base de données SQLite
        self.conn = database
        self.cursor = self.conn.cursor()

        # Récupérez la liste de tous les objets de la base de données
        self.cursor.execute("SELECT id, name FROM items")
        self.items = {row[0]: row[1] for row in self.cursor.fetchall()}

        # Créez un menu déroulant pour sélectionner l'objet
        self.item_combo_box = QtWidgets.QComboBox()
        self.item_combo_box.addItems(self.items.values())
        self.item_combo_box.currentIndexChanged.connect(self.update_item_info)

        # Créez des champs pour afficher les informations de l'objet
        self.current_buy_price_label = QtWidgets.QLabel("Current buy price:")
        self.current_sell_price_label = QtWidgets.QLabel("Current sell price:")
        self.cheapest_buy_day_label = QtWidgets.QLabel("Cheapest buy day:")
        self.highest_sell_day_label = QtWidgets.QLabel("Highest sell day:")
        # Créez un layout vertical pour disposer les widgets horizontalement
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.item_combo_box)
        layout.addWidget(self.current_buy_price_label)
        layout.addWidget(self.current_sell_price_label)
        layout.addWidget(self.cheapest_buy_day_label)
        layout.addWidget(self.highest_sell_day_label)

        # Créez un widget central pour contenir le layout
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Affichez la fenêtre
        self.show()

    def update_item_info(self):
        # Récupérez l'ID de l'objet sélectionné à partir de la liste des objets
        selected_item_id = list(self.items.keys())[self.item_combo_box.currentIndex()]
        # Récupérez les informations de l'objet de la base de données
        self.cursor.execute("SELECT current_buy_price, current_sell_price, cheapest_buy_day, highest_sell_day FROM items WHERE id=?", (selected_item_id,))
        current_buy_price, current_sell_price, cheapest_buy_day, highest_sell_day = self.cursor.fetchone()
        # Mettez à jour les champs pour afficher les informations de l'objet
        self.current_buy_price_label.setText(f"Current buy price: {current_buy_price}")
        self.current_sell_price_label.setText(f"Current buy price: {current_buy_price}")
        self.cheapest_buy_day_label.setText(f"Cheapest buy day: {cheapest_buy_day}")
        self.highest_sell_day_label.setText(f"Highest sell day: {highest_sell_day}")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    database = Database("prices.db")
    window = MainWindow(database)
    app.exec_()

