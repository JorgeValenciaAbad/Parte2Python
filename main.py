# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox



class Product:
    def __init__(self, title, price, category, rating):
        self.title = title
        self.price = price
        self.category = category
        self.rating = rating


class Zara(QMainWindow):
    precio_total = 0
    products = []
    carrito = []
    num_matches = 20
    res = requests.get('https://fakestoreapi.com/products')

    def __init__(self):
        super().__init__()
        uic.loadUi("LaLiga.ui", self)
        self.load_data()
        self.table.cellClicked.connect(self.get_match)
        self.agregar.clicked.connect(self.add_list)
        self.limpiar.clicked.connect(self.clean_list)
        self.eliminar.clicked.connect(self.del_item)
        self.comprar.clicked.connect(self.buy)
    def get_match(self, row):

        self.title.setText(self.products[row].title)
        self.category.setText("Categoria: " + self.products[row].category)
        self.price.setText("Precio: " + str(self.products[row].price) + "€")
        self.rating.setText("Valoraciones: " + str(self.products[row].rating))

    def load_data(self):

        self.table.setRowCount(self.num_matches)
        self.table.setColumnWidth(0, 500)
        for num in range(self.num_matches):
            self.products.append(
                Product(self.res.json()[num]['title'], self.res.json()[num]['price'], self.res.json()[num]['category'],
                        self.res.json()[num]['rating']["rate"]))
            self.table.setItem(num, 0, QtWidgets.QTableWidgetItem(
                self.res.json()[num]['title'] + ' ' + str(self.res.json()[num]['price']) + '€'))

    def add_list(self):
        for item in self.table.selectedItems():
            self.lista.addItem(
                QtWidgets.QListWidgetItem(self.products[item.row()].title + ' ' + str(self.products[item.row()].price)))
            self.precio_total += self.products[item.row()].price
            self.precio.setText(str(self.precio_total) + '€')
            self.carrito.append(Product(self.products[item.row()].title,self.products[item.row()].price,self.products[item.row()].category,self.products[item.row()].rating))

    def clean_list(self):
        self.lista.clear()
        self.precio_total = 0
        self.precio.setText("0")

    def select_match(self):
        for item in self.lista.selectedItems():
            self.lista.takeItem(item.row())

    def del_item(self):
        if(self.lista.currentRow()>=0):
            self.lista.takeItem(self.lista.currentRow())
            self.precio_total -= self.carrito[self.lista.currentRow()].price
            self.precio.setText("0€")
            self.carrito.pop(self.lista.currentRow())

    def buy(self):
        msg_box = QMessageBox()
        msg_box.setText("¿Confirmar pedido?\nPrecio total: "+self.precio.text())
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # Get the user's response
        response = msg_box.exec_()

        # Check if the user clicked "Yes" or "No"
        if response == QMessageBox.Yes:
            archivo = open("factura.txt","w")
            archivo.write("Factura del Pedido:\n")
            for item in self.carrito:
                archivo.write(item.title+"\n")

            archivo.write(self.precio.text())
            archivo.close()
            self.carrito.clear()
            self.clean_list()
        else:
            # User clicked "No", do something else
            print("Pedido cancelado.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Zara()
    gui.show()
    sys.exit(app.exec())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
