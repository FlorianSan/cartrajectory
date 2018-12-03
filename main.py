#début programme

from PyQt5 import QtWidgets
import affichage_piste
import voiture

if __name__ == "__main__":
    # Initialize Qt
    app = QtWidgets.QApplication([])
    car = voiture.Voiture(10,10,10)

    # create the radar view and the time navigation interface
    main_window = affichage_piste.Dessin()

    # enter the main loop
    app.exec_()