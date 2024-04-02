import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QCheckBox, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Checkbox in Each Row Example")

        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Checkbox"])

        # Add rows and set checkbox
        self.addRowWithCheckbox("Item 1")
        self.addRowWithCheckbox("Item 2")
        self.addRowWithCheckbox("Item 3")

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def addRowWithCheckbox(self, text):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)

        item = QTableWidgetItem(text)
        self.tableWidget.setItem(rowPosition, 0, item)

        checkbox = QCheckBox()
        self.tableWidget.setCellWidget(rowPosition, 1, checkbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
