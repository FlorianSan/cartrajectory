#début programme

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

import affichage_piste
import voiture
import piste
import affichage
import mouse_tracker


if __name__ == "__main__":
    choice = int(input("1: aléatoire / 2: enregistré / 3 : dessin ? "))
    # Initialize Qt
    app = QtWidgets.QApplication([])
    main_window = affichage_piste.Dessin(choice)
    timer = QTimer()
    timer.timeout.connect(main_window.miseajour)
    timer.start(330)
    main_window.show()
    app.exec_()