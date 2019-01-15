#début programme
import sys
from PyQt5.QtWidgets import QApplication

import Selector

if __name__ == "__main__":
    app = QApplication(sys.argv)
    selector = Selector.Selector()
    selector.show()
    app.exec_()