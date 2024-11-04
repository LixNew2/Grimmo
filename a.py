import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QCalendarWidget

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calendrier Qt")
        self.setGeometry(100, 100, 400, 300)

        # Widget central
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.layout = QVBoxLayout(self.central_widget)

        # Créer le QCalendarWidget
        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)

        # Créer un label pour afficher la date sélectionnée
        self.date_label = QLabel("Date sélectionnée : ", self)
        self.date_label.setStyleSheet("font-size: 18px;")

        # Connecter le signal clicked à une méthode
        self.calendar.clicked.connect(self.show_selected_date)

        # Ajouter le calendrier et le label à la mise en page
        self.layout.addWidget(self.calendar)
        self.layout.addWidget(self.date_label)

    def show_selected_date(self, date):
        """Afficher la date sélectionnée dans le label au format jj/mm/aaaa."""
        formatted_date = date.toString("dd/MM/yyyy")  # Formatage de la date
        self.date_label.setText(f"Date sélectionnée : {formatted_date}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec_())
