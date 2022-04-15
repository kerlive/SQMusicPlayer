# PyQt5 Audio player
#code by kevin
__author__ = "Kevin Chan"
__copyright__ = "Copyright (C) 2022 Kevin Chan"
__license__ = "GPL-3.0"

import os, sys
import datetime
from multiprocessing import shared_memory
key = "SQMusicPlayer"
instance = 1
try:
    single = shared_memory.SharedMemory(key, create=False)
    single.buf[0] = 0
except:
    instance = 0
if instance == 0:
    single = shared_memory.SharedMemory(key, create=True,size=1)
    single.buf[0] = 1
else:
    sys.exit("App is runing")

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist


ui_path = os.path.dirname(os.path.abspath(__file__))
form_1, base_1 = uic.loadUiType(os.path.join(ui_path,"SQMP.ui"))

class Main(base_1, form_1):
    def __init__(self):
        super(base_1, self).__init__()
        self.setupUi(self)
        
        self.player = QMediaPlayer()
        #set can not minisize for trayicon
        self.setWindowFlags(QtCore.Qt.Dialog)

        self.setFixedSize(340,220)
        self.setWindowIcon(QtGui.QIcon(':/Icon/Apricot_SQMP.ico'))
        # Player control panel

        self.PlayButton.clicked.connect(self.media_play)
        self.pauseButton.clicked.connect(self.media_pause)
        self.muteButton.clicked.connect(self.volumeMute)
        self.Slider_player_volume.valueChanged.connect(self.volumeUpdate)
        self.Slider_player_volume.setValue(80)
        self.horizontalSlider.sliderReleased.connect(self.slider_moved)
        self.seekforwardButton.clicked.connect(self.move_forward)
        self.seekbackwardButton.clicked.connect(self.move_backward)
        self.addButton.clicked.connect(self.musicAdd)
        self.delButton.clicked.connect(self.music_del)
        self.listWidget.itemClicked.connect(self.music_add)
        self.loopButton.clicked.connect(self.loop_control)
        self.looplistButton.clicked.connect(self.list_charge)
        self.skipbackwardButton.clicked.connect(self.skip_backward)
        self.skipforwardButton.clicked.connect(self.skip_forward)
        self.listcontrolButton.clicked.connect(self.list_control)

        # loop signal
        self.loop = 0
        self.listloop = 0

        self.list_music()


        # Media player signals
        self.player.stateChanged.connect(self.show_mediaState)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)

        # Set Button Icon to QtStandardIcon

        self.PlayButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.muteButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.loopButton.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.looplistButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.addButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.delButton.setIcon(self.style().standardIcon(QStyle.SP_DialogDiscardButton))
        self.seekbackwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.seekforwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.skipbackwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.skipforwardButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.listcontrolButton.setIcon(self.style().standardIcon(QStyle.SP_ToolBarVerticalExtensionButton))

        # Icon change signal
        self.pause = 0

        # Block Button
        self.PlayButton.setEnabled(False)
        self.loopButton.setEnabled(False)
        self.listcontrolButton.setEnabled(False)

        #QTrayIcon
        QApplication.setQuitOnLastWindowClosed(False)

        icon = QtGui.QIcon(":/Icon/Apricot_SQMP.ico")
        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.setIcon(icon)
        self.trayIcon.setVisible(True)

        self.trayIcon.activated.connect(self.onTrayIconActivated)

        menu = QMenu()
        
        
        show = QAction("Pause",self)
        show.triggered.connect(self.media_pause)
        menu.addAction(show)
        show = QAction("Reload",self)
        show.triggered.connect(self.skip_backward)
        menu.addAction(show)
        hide = QAction("Next",self)
        hide.triggered.connect(self.skip_forward)
        menu.addAction(hide)
        
        quit = QAction("Quit",self)
        quit.triggered.connect(self.trayicon_quit)
        menu.addAction(quit)

        self.trayIcon.setContextMenu(menu)

        self.anotherCall()

    def anotherCall(self):
        cTimer = QtCore.QTimer(self)
        cTimer.start(1000)
        cTimer.timeout.connect(self.checkNew)
    def checkNew(self):
         if single.buf[0] == 0:
             self.show()
             single.buf[0] = 1
    
    def trayicon_quit(self):
        sys.exit(1)
    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.hide()
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def music_add(self):
        name = self.listWidget.currentItem().text()
        sound_path =  os.path.dirname(os.path.abspath(__name__)) + "/Music/" + name
        url = QtCore.QUrl.fromLocalFile(sound_path)
        content = QMediaContent(url)
        self.soundtrack = QMediaPlaylist()
        self.soundtrack.addMedia(content)
        self.soundtrack.setCurrentIndex(1)

        self.player.setPlaylist(self.soundtrack)
        self.PlayButton.setEnabled(True)
        self.loopButton.setEnabled(True)
        self.listcontrolButton.setEnabled(False)
    
    def list_charge(self):
        self.soundtrack_list = QMediaPlaylist()
        name_list = os.listdir(os.getcwd()+"/Music/")
        for n,name in enumerate(name_list):
            url = QtCore.QUrl.fromLocalFile(os.getcwd()+"/Music/"+name)
            content = QMediaContent(url)
            self.soundtrack_list.addMedia(content)

        self.soundtrack_list.setCurrentIndex(1)
        self.player.setPlaylist(self.soundtrack_list)
        self.soundtrack_list.setPlaybackMode(QMediaPlaylist.Loop)
        self.PlayButton.setEnabled(True)
        self.loopButton.setEnabled(True)
        self.listcontrolButton.setEnabled(True)
        self.loopButton.setEnabled(False)

        self.media_play()
    def list_control(self):
        match self.listloop:
            case 0:
                self.listloop = 1
                self.listcontrolButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarContextHelpButton))
                self.soundtrack_list.setPlaybackMode(QMediaPlaylist.Sequential)
            case 1:
                self.listloop = 2
                self.soundtrack_list.setPlaybackMode(QMediaPlaylist.Random)
                self.listcontrolButton.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
            case 2:
                self.listloop = 0
                self.soundtrack_list.setPlaybackMode(QMediaPlaylist.Loop)
                self.listcontrolButton.setIcon(self.style().standardIcon(QStyle.SP_ToolBarVerticalExtensionButton))
    
    def loop_control(self):
        if self.loop == 0:
            self.loop = 1
            self.loopButton.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
            self.soundtrack.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        elif self.loop == 1:
            self.loop = 0
            self.loopButton.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
            self.soundtrack.setPlaybackMode(QMediaPlaylist.CurrentItemOnce)

    def skip_forward(self):
        self.set_position(self.horizontalSlider.maximum())
    def skip_backward(self):
        self.set_position(0)
    def move_forward(self):
        self.set_position(self.horizontalSlider.sliderPosition()+15000)
    def move_backward(self):
        self.set_position(self.horizontalSlider.sliderPosition()-15000)
    
    def slider_moved(self):
        self.set_position(self.horizontalSlider.value())

    def set_position(self, position):
        self.player.setPosition(position)

    def duration_changed(self, duration):
        self.horizontalSlider.setRange(0, duration)

    def position_changed(self, position):
        self.horizontalSlider.setValue(position)

    def show_mediaState(self):
        match self.player.state():
            case 1:
                self.setWindowTitle("Music Playing")
            case 2:
                self.setWindowTitle("Music Paused")
            case 0:
                self.setWindowTitle("Small Music Player")
                self.horizontalSlider.setValue(0)
                self.label_time.setText("00:00:00/00:00:00")
                self.PlayButton.setText("Play")
                self.PlayButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))


    def music_del(self):
        if self.listWidget.currentRow() == -1:
            self.setWindowTitle("NO Music select in List")
        else:
            name = self.listWidget.currentItem().text()
            QtCore.QFile.remove("./Music/"+name)
            self.listWidget.clear()
            self.list_music()

    def musicAdd(self):
        ADD = QFileDialog()
        MFile = ADD.getOpenFileName(self,"Add New Music", "","Music Files(*.mp3 *.wav)")
        Mname = os.path.split(MFile[0])
        QtCore.QFile.copy(MFile[0],"./Music/"+Mname[1])
        self.listWidget.clear()
        self.list_music()

    def list_music(self):
        music_path = os.path.dirname(os.path.abspath(__name__)) + "/Music"
        dir_list = os.listdir(music_path)
        for m in dir_list:
            self.listWidget.addItem(m)
    
    def media_position(self):
        self.time = QtCore.QTimer(self)
        self.time.start(1000)
        self.time.timeout.connect(self.media_viewtime)
    
    def media_viewtime(self):
        pos_sec = int(self.player.position()/1000)
        pos = str(datetime.timedelta(seconds=pos_sec))
        dat_sec = int(self.player.duration()/1000)
        dat = str(datetime.timedelta(seconds=dat_sec))
        text = pos + "/" + dat
        self.label_time.setText(text)

    def volumeMute(self):
        if self.player.isMuted():
            self.player.setMuted(False)
            self.muteButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        else:
            self.player.setMuted(True)
            self.muteButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
            
    def volumeUpdate(self):
        self.player.setVolume(self.Slider_player_volume.value())

    def media_pause(self):
        if self.pause == 0:
            self.pause = 1
            self.player.pause()
            self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.pause = 0
            self.player.play()
            self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))    
        
    def media_play(self):
        if self.PlayButton.text() == "Play":
            self.PlayButton.setText("Stop")
            self.PlayButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))

            self.player.play()

            self.media_position()
        else:
            self.PlayButton.setText("Play")
            self.PlayButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.player.stop()

            self.pause = 0
            self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))   

            self.time.stop()
            self.label_time.setText("00:00:00/00:00:00")

