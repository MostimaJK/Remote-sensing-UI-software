# coding: utf-8
from PyQt5.QtCore import QObject


class Translator(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.text = self.tr('Text')
        self.view = self.tr('View')
        # self.menus = self.tr('Menus & toolbars')
        self.menus = self.tr('工具栏')
        self.icons = self.tr('Icons')
        # self.layout = self.tr('Layout')
        self.layout = self.tr('图像分割')
        self.dialogs = self.tr('Dialogs & flyouts')
        self.scroll = self.tr('Scrolling')
        # self.material = self.tr('Material')
        self.material = self.tr('图像融合')
        self.dateTime = self.tr('Date & time')
        self.navigation = self.tr('Navigation')
        # self.basicInput = self.tr('Basic input')
        self.basicInput = self.tr('图像滤波')
        self.statusInfo = self.tr('Status & info')