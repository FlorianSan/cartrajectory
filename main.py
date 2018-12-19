#début programme

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

import affichage_piste
import voiture
import piste
import affichage
import mouse_tracker

FILE=['None','data']

if __name__ == "__main__":
    choice = 0 if input("1: aléatoire / 2: enregistré ? ") == '1' else 1
    # Initialize Qt
    app = QtWidgets.QApplication([])
    car = voiture.Voiture(10,10,10)

    main_window = affichage_piste.Dessin(FILE[choice])
    car.position = main_window.point
    moving_car = affichage.CarMotion(main_window, car)


    timer = QTimer()
    timer.timeout.connect(moving_car.updateValues)
    timer.start(33)



    # show the window
    main_window.show()
    # enter the main loop
    app.exec_()