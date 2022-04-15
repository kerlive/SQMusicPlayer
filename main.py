from Qui.music_player import *
import sys
import UIresource_rc
from multiprocessing import shared_memory


if __name__ == '__main__':
    
    key = "SQMusic"

    try:
        single = shared_memory.SharedMemory(key, create=False)
        single.buf[0] = 0
        sys.exit("App is runing")
        
    except:
        single = shared_memory.SharedMemory(key, create=True,size=1)
        single.buf[0] = 1

        app = QApplication(sys.argv)
        demo = Main()
        demo.show()
        
        
    sys.exit(app.exec_())