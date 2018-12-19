import affichage_piste
import affichage

def Simulation(car):
    main_window = affichage_piste.Dessin()
    car.position = main_window.point
    moving_car = affichage.CarMotion(main_window, car)


    timer = QTimer()
    timer.timeout.connect(moving_car.updateValues)
    timer.start(33)


    # show the window
    main_window.show()