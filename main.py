#début programme

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

import affichage_piste
import voiture


if __name__ == "__main__":
    choice = int(input("1: aléatoire / 2: enregistré (sans A*) / 3: enregistré (avec A*) / 4: dessin ? "))
    # Initialize Qt
    app = QtWidgets.QApplication([])
    car = voiture.Voiture()
    main_window = affichage_piste.Dessin(choice, car)
    timer = QTimer()
    timer.timeout.connect(main_window.miseajour)
    timer.start(33)
    main_window.show()
    app.exec_()