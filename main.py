from Qui.music_player import *
import sys
import UIresource_rc


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Main()
    demo.show()
    
    sys.exit(app.exec_())