#début programme

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

import affichage_piste
import voiture
import piste
import affichage

if __name__ == "__main__":
    # Initialize Qt
    app = QtWidgets.QApplication([])
    car = voiture.Voiture(10,10,10)


    # create the radar view and the time navigation interface
    main_window = affichage_piste.Dessin()
    car.position = main_window.point
    moving_car = affichage.CarMotion(main_window, car)


    timer = QTimer()
    timer.timeout.connect(moving_car.updateValues)
    timer.start(10)


    # show the window
    main_window.show()
    # enter the main loop
    app.exec_()