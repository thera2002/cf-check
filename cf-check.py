import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox
from codicefiscale import codicefiscale

class CodiceFiscaleChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setFixedWidth(400)
        layout = QVBoxLayout()
        
        # Campo per il sesso
        layout.addWidget(QLabel("Sesso"))
        self.gender_field = QComboBox()
        self.gender_field.addItems(["M", "F"])
        layout.addWidget(self.gender_field)
        
        # Creazione campi input
        self.fields = {}
        labels = ["Cognome", "Nome", "Data di nascita (GG/MM/AAAA)", "Luogo di nascita", "Codice Fiscale"]
        
        for label in labels:
            layout.addWidget(QLabel(label))
            self.fields[label] = QLineEdit()
            layout.addWidget(self.fields[label])
        
        # Pulsante di verifica
        self.check_button = QPushButton("Verifica Codice Fiscale")
        self.check_button.clicked.connect(self.verify_codice_fiscale)
        layout.addWidget(self.check_button)
        
        self.setLayout(layout)
        self.setWindowTitle("Verifica Codice Fiscale")
    
    def verify_codice_fiscale(self):
        sesso = self.gender_field.currentText()
        cognome = self.fields["Cognome"].text().strip()
        nome = self.fields["Nome"].text().strip()
        data_nascita = self.fields["Data di nascita (GG/MM/AAAA)"].text().strip()
        luogo_nascita = self.fields["Luogo di nascita"].text().strip()
        cf_input = self.fields["Codice Fiscale"].text().strip().upper()

        try:
            cf_generato = codicefiscale.encode(
                lastname=cognome,
                firstname=nome,
                gender=sesso,
                birthdate=data_nascita,
                birthplace=luogo_nascita
            )
            is_omocode = codicefiscale.is_omocode(cf_input)
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Errore nella generazione del codice fiscale: {str(e)}")
            return
        
        if cf_input == cf_generato:
            QMessageBox.information(self, "Successo", "Il codice fiscale inserito è corretto!")
        elif is_omocode:
            QMessageBox.information(self, "Attenzione", f"Il codice fiscale inserito è un codice omocodico valido!\nIl codice fiscale originale sarebbe: {cf_generato}")
        else:
            QMessageBox.warning(self, "Errore", f"Il codice fiscale inserito non è corretto!\nDovrebbe essere: {cf_generato}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodiceFiscaleChecker()
    window.show()
    sys.exit(app.exec_())
