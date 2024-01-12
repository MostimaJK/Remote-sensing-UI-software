# coding: utf-8
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF


from .gallery_interface import GalleryInterface # 图库
from .home_interface import HomeInterface   # 主页-Home
from .basic_input_interface import BasicInputInterface  # 基本输出-图像滤波
from .layout_interface import LayoutInterface   # 布局-图像分割
from .material_interface import MaterialInterface   # 材料-图像融合
from .menu_interface import MenuInterface   # 菜单
from .setting_interface import SettingInterface # 设置-Setting

from ..common.config import SUPPORT_URL, cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common import resource

from PyQt5.QtCore import QTimer

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        # 初始化窗口
        self.initWindow()

        # 创建子界面
        self.homeInterface = HomeInterface(self)# 主页-Home
        self.basicInputInterface = BasicInputInterface(self)# 基本输出-图像滤波
        self.layoutInterface = LayoutInterface(self) # 布局-图像分割
        self.materialInterface = MaterialInterface(self)# 材料-图像融合
        self.menuInterface = MenuInterface(self)
        self.settingInterface = SettingInterface(self)

        # 启用丙烯效果
        self.navigationInterface.setAcrylicEnabled(True)

        # 连接信号和槽
        self.connectSignalToSlot()

        # 添加项目到导航界面
        self.initNavigation()
        # 结束启动屏幕
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        # 连接信号和槽
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # 添加导航项目
        t = Translator()
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))# 主页-Home
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.basicInputInterface, FIF.CHECKBOX,t.basicInput, pos)  # 基本输出-图像滤波
        self.addSubInterface(self.layoutInterface, FIF.LAYOUT, t.layout, pos)   # 布局-图像分割
        self.addSubInterface(self.materialInterface, FIF.PIE_SINGLE, t.material, pos)  # 材料-图像融合
        # FIF.PALETTE
        self.addSubInterface(self.menuInterface, FIF.APPLICATION, t.menus, pos)   # 菜单
        # Icon.MENU

        # 在底部添加自定义小部件
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('Jacky', 'Photos/resource/用户头像Mei.png'),
            onClick=self.onSupport,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        # 初始化窗口
        self.resize(1300, 800)
        self.setMinimumWidth(760)
        # self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowIcon(QIcon('Photos/resource/遥感测绘.png'))  # 设置窗口图标
        self.setWindowTitle('遥感原理与图像处理')# 设置窗口标题

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))# 设置丙烯效果

        # 创建启动屏幕
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(150, 150))
        self.splashScreen.raise_()

        # 设置延时，单位为毫秒，例如这里设置为 5000 毫秒，即 5 秒
        QTimer.singleShot(2000, self.splashScreen.close)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def onSupport(self):
        w = MessageBox(
            'Member：Jacky Louyuxuan Liushigang',
            '遥感原理与图像处理期末作业！！٩(^ω^*)و',
            self
        )
        w.yesButton.setText('财源滚滚！')
        w.cancelButton.setText('恭喜发财!')
        if w.exec():
            SUPPORT_URL2 = 'https://github.com/LyxWxj/libGD'
            QDesktopServices.openUrl(QUrl(SUPPORT_URL2))

    SUPPORT_URL
    # 重写窗口大小改变事件
    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def switchToSample(self, routeKey, index):
        """ 切换到sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)
