import os
import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QFileDialog, QSlider, QStyle, QMessageBox, qApp
from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt
from qtpy import QtCore


class AudioPlayer(QWidget):
    # конструктор
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.qsound = None
        self.init_ui()
        self.show()
        self.x = 0
        self.y = 0

    def init_ui(self):
        self.label_image = QLabel(self)
        self.label_image.setPixmap(QtGui.QPixmap("images/image.png"))

        # установка появления и размера окна, а также настройка шрифтов
        self.setGeometry(700, 400, 600, 200)
        self.setFixedSize(590, 200)
        self.setWindowTitle('MP3 Player')
        font = QFont("Arial", 18)
        font1 = QFont("Arial", 12)

        # раскраска заднего фона
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.gray)
        self.setPalette(p)

        # кнопка воспроизведения/паузы
        self.button_stop = QPushButton(self)
        self.button_stop.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.button_stop.move(160, 159)
        self.button_stop.resize(30, 30)

        # кнопка выхода
        self.button_exit = QPushButton("Exit", self)
        self.button_exit.move(490, 160)
        self.button_exit.setStyleSheet('QPushButton {background-color: #000000; color: white;}')

        # кнопка для выбора открываемого файла
        self.button_dialog = QPushButton("Open file", self)
        self.button_dialog.move(10, 160)
        self.button_dialog.setStyleSheet('QPushButton {background-color: #000000; color: white;}')

        # соединения сигналов к кнопкам выхода и выбора открываемого файла
        self.button_dialog.clicked.connect(self.button_openfile)
        self.button_exit.clicked.connect(self.closeEvent)
        self.button_stop.clicked.connect(self.stop)

        # слайдер для изменения громкости
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.move(300, 165)
        self.sld.setValue(100)
        self.sld.valueChanged.connect(self.changeValue)

        # создание и настройка label для положеня изменения громкости
        self.label1 = QLabel(self)
        self.label1.setPixmap(QtGui.QPixmap("images/speaker-volume.png"))
        self.label1.move(280, 166)
        self.label1.setFont(font1)

        self.button_prev = QPushButton(self)
        self.button_prev.move(120, 160)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/control-skip-180.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_prev.setIcon(icon1)

        self.button_next = QPushButton(self)
        self.button_next.move(240, 160)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/control-skip.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_next.setIcon(icon2)

        # слайдер для промотки самого трека
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.resize(570, 20)
        self.slider.move(10, 130)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_pos)

        # сигналы для слайдера для промотки трека
        self.player.stateChanged.connect(self.izm_of_mediastate)
        self.player.positionChanged.connect(self.izm_of_position)
        self.player.durationChanged.connect(self.izm_of_duration)

        self.stp = QPushButton(self)
        self.stp.move(200, 160)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/control-stop-square.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stp.setIcon(icon3)
        self.stp.pressed.connect(self.player.stop)

        # создания label для показа названия трека
        self.label = QLabel(self)
        self.label.setFont(font)
        self.label.move(10, 10)

    def set_pos(self, position):
        self.player.setPosition(position)

    def izm_of_mediastate(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.button_stop.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.button_stop.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    # Изменяет размерность слайдера по длительности
    def izm_of_duration(self, duration):
        self.slider.setRange(0, duration)

    # Изменяет позицию слайдера.
    def izm_of_position(self, position):
        self.slider.setValue(position)

    # Функция, чтобы вылезало сообщение принажатии на крестик или на кнопку выход
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Предупреждение', 'Вы точно хотите выйти?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            qApp.quit()
        else:
            try:
                event.ignore()
            except AttributeError:
                pass

    def changeValue(self):
        self.player.setVolume(self.sld.value())

    # функция для кнопки воспроизведения
    def stop(self):
        if self.player is not None:
            if self.x == 0:
                self.player.play()
                self.button_stop.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
                self.x += 1
            else:
                self.player.pause()
                self.button_stop.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
                self.x -= 1

    # функция для кнопки открываемого файла
    def button_openfile(self):
        filepath, _ = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Audio files (*.mp3)")
        filepath = os.path.abspath(filepath)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(filepath)))
        self.filename = os.path.basename(filepath)
        self.label.setText(self.filename[:-4])
        self.label.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ex = ()
    w = AudioPlayer()
    palette = QPalette()
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.Text, Qt.white)
    app.setPalette(palette)
    app.exit(app.exec_())
