# coding:utf-8
from PyQt5.QtGui import QColor
from qfluentwidgets.components.widgets.acrylic_label import AcrylicLabel
from qfluentwidgets import FluentIcon as FIF

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.config import cfg

from PyQt5.QtCore import QPoint, Qt, QStandardPaths
from PyQt5.QtGui import QColor, QImage, QPixmap, QPainter, QWheelEvent, QMouseEvent
from PyQt5.QtWidgets import (QAction, QWidget, QLabel, QVBoxLayout, QFileDialog, QActionGroup, QLabel,
                             QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QGraphicsView,
                             QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QVBoxLayout)
from qfluentwidgets import (RoundMenu, PushButton, Action, CommandBar, Action, TransparentDropDownPushButton,
                            setFont, CommandBarView, Flyout, ImageLabel, FlyoutAnimationType, CheckableMenu,
                            MenuIndicatorType, AvatarWidget, isDarkTheme, BodyLabel, CaptionLabel, HyperlinkButton,
                            ComboBox, PrimaryPushButton, InfoBarIcon, LineEdit)
from qfluentwidgets import FluentIcon as FIF
import cv2
import libGD_f.libGD as libGD

# 定义一个名为MaterialInterface的类，继承自GalleryInterface
class MaterialInterface(GalleryInterface):
    """ Material interface """

    # 初始化方法
    def __init__(self, parent=None):
        # 创建一个Translator对象
        t = Translator()
        self.src = None
        self.result = None
        # 调用父类的初始化方法，设置标题和子标题
        super().__init__(
            title=t.material,
            subtitle='遥感原理与图像处理-图像融合',
            parent=parent
        )
        self.imagePathMs = None
        self.imagePathPan  = None
        # 设置对象的名称为'materialInterface'
        self.setObjectName('materialInterface')

        # 浮出命令栏
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout())  # 设置布局为垂直布局
        self.widget.layout().setContentsMargins(0, 0, 0, 0)  # 设置布局的边距
        self.widget.layout().setSpacing(10)  # 设置布局的间距

        # 创建导入图片按钮A
        self.button_input_A = PushButton(self.tr("导入图片MS多光谱影像"))
        self.button_input_A.setFixedWidth(180)  # 设置按钮大小
        self.h_layout = QHBoxLayout(self.widget)# 创建水平布局
        self.h_layout.setSpacing(10)# 设置水平布局的间距
        self.h_layout.addWidget(self.button_input_A, 0, Qt.AlignLeft)# 将按钮添加到水平布局中
        self.vBoxLayout.addLayout(self.h_layout)# 将水平布局添加到垂直布局中
        self.button_input_A.clicked.connect(self.inputPhoto)  # 连接按钮的点击信号导入图片并显示


        # 创建导入图片按钮B
        self.button_input_B = PushButton(self.tr("导入图片PAN全色图"))
        self.button_input_B.setFixedWidth(150)  # 设置按钮大小
        self.h_layout = QHBoxLayout(self.widget)# 创建水平布局
        self.h_layout.setSpacing(10)# 设置水平布局的间距
        self.h_layout.addWidget(self.button_input_B, 0, Qt.AlignLeft)# 将按钮添加到水平布局中
        self.vBoxLayout.addLayout(self.h_layout)# 将水平布局添加到垂直布局中
        self.button_input_B.clicked.connect(self.inputPhoto_B)  # 连接按钮的点击信号导入图片并显示


        # 创建下拉框
        self.comboBox_filter = ComboBox()  # 创建下拉框
        self.comboBox_filter.setPlaceholderText("请选择图像融合方法")
        items = ['IHSF', 'GIHSF', 'AIHSF', 'IAIHSF']  # 下拉框的选项
        self.comboBox_filter.addItems(items)  # 添加下拉框的选项
        self.comboBox_filter.setCurrentIndex(-1)  # 设置下拉框的默认选项
        self.comboBox_filter.setFixedWidth(100)  # 设置下拉框的宽度
        self.comboBox_filter.setMaximumWidth(180)  # 设置下拉框的最大宽度
        self.h_layout.addWidget(self.comboBox_filter, 0, Qt.AlignLeft)  # 将下拉框添加到水平布局中
        self.comboBox_filter.currentIndexChanged.connect(self.GetcomboBox_value)  # 当下拉框的选项改变时，触发事件

        # 创建导入Apply按钮
        self.button_input_apply = PushButton(self.tr("Apply"))
        self.button_input_apply.setFixedWidth(100)  # 设置按钮大小
        self.button_input_apply.clicked.connect(self.Apply_IMGFusion)  # 连接按钮的点击信号导入图片并显示
        self.h_layout.addWidget(self.button_input_apply, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中

        # 创建保存滤波图像按钮
        self.button_input_save = PrimaryPushButton(self.tr("保存融合图像"))
        self.button_input_save.setFixedWidth(120)  # 设置按钮大小
        self.h_layout.addWidget(self.button_input_save, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中
        self.button_input_save.clicked.connect(self.Filter_saveImage)  # 连接按钮的点击信号导入图片并显示

        # 创建一个标签
        label = QLabel(self.tr('单击图片打开命令栏，图片将在滤波后自动更换！'))
        self.imageLabel = ImageLabel('Photos/resource/interface_background/magic.jpg')# 创建一个ImageLabel对象
        self.imageLabel2 = ImageLabel('Photos/resource/interface_background/magic3.jpg')# 创建一个ImageLabel对象

        # 设置图片功能
        self.imageLabel.scaledToWidth(500)  # 设置图片的宽度
        self.imageLabel2.scaledToWidth(500)  # 设置图片的宽度
        self.imageLabel.setBorderRadius(8, 8, 8, 8)  # 设置图片的圆角
        self.imageLabel2.setBorderRadius(8, 8, 8, 8)  # 设置图片的圆角
        self.imageLabel.clicked.connect(self.createCommandBarFlyout)  # 连接图片的点击信号，打开命令栏
        self.imageLabel2.clicked.connect(self.createCommandBarFlyout)# 连接图片的点击信号，打开命令栏

        # 创建一个水平布局
        self.h_layout_photos = QHBoxLayout(self.widget)
        self.h_layout_photos.setSpacing(10)# 设置水平布局的间距
        self.h_layout_photos.addWidget(self.imageLabel, 0, Qt.AlignLeft)# 将图片A添加到水平布局中
        self.h_layout_photos.addWidget(self.imageLabel2, 0, Qt.AlignLeft)# 将图片B添加到水平布局中

        self.widget.layout().addWidget(label)  # 将标签添加到布局中
        self.widget.layout().addLayout(self.h_layout_photos)  # 将水平布局添加到布局中

        # 添加一个示例卡片，包含了标签的翻译，标签对象，示例代码的链接，和拉伸值
        self.addExampleCard(
            self.tr('遥感影像'),
            self.widget,
            'https://github.com/LyxWxj/libGD',
            stretch=1
        )

    # 当下拉框的选项改变时，触发事件
    def GetcomboBox_value(self):
        # 获取下拉框的选项
        comboBox_value = self.comboBox_filter.currentText()
        print(comboBox_value)
        res = -1
        if comboBox_value == 'IHSF':
            res = 1
        elif comboBox_value == 'GIHSF':
            res = 2
        elif comboBox_value == 'AIHSF':
            res = 3
        elif comboBox_value == 'IAIHSF':
            res = 4
        else:
            res = -1
        return res

    # 创建命令栏弹出窗口的方法
    def createCommandBarFlyout(self):
        view = CommandBarView(self)

        view.addAction(Action(FIF.SHARE, self.tr('Share')))
        view.addAction(Action(FIF.SAVE, self.tr('Save'), triggered=self.saveImage))
        view.addAction(Action(FIF.HEART, self.tr('Add to favorate')))
        view.addAction(Action(FIF.DELETE, self.tr('Delete')))

        view.addHiddenAction(Action(FIF.PRINT, self.tr('Print'), shortcut='Ctrl+P'))
        view.addHiddenAction(Action(FIF.SETTING, self.tr('Settings'), shortcut='Ctrl+S'))
        view.resizeToSuitableWidth()

        x = self.imageLabel.width()
        pos = self.imageLabel.mapToGlobal(QPoint(x, 0))
        Flyout.make(view, pos, self, FlyoutAnimationType.FADE_IN)

    # 保存图片的方法
    def saveImage(self):
        path, ok = QFileDialog.getSaveFileName(
            parent=self,
            caption=self.tr('Save image'),
            directory=QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),
            filter='TIF (*.tif)'
        )
        if not ok:
            return

        self.imageLabel.image.save(path)

    # 导入图片A的方法
    def inputPhoto(self):
        # 打开一个QFileDialog并获取用户选择的图片路径
        filepath, _ = QFileDialog.getOpenFileName()
        if filepath:
            # 将用户选择的图片路径赋值给ImageLabel
            self.imageLabel.setPixmap(filepath)
            # 设置图片的最大宽度
            self.imageLabel.setMaximumWidth(800)
            self.imageLabel.scaledToWidth(500)  # 设置图片的宽度
            self.imagePathMs = filepath  # 保存图片路径
            self.src = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)  # 用opencv读取图片

    # 导入图片B的方法
    def inputPhoto_B(self):
        # 打开一个QFileDialog并获取用户选择的图片路径
        filepath, _ = QFileDialog.getOpenFileName()
        if filepath:
            # 将用户选择的图片路径赋值给ImageLabel
            self.imageLabel2.setPixmap(filepath)
            # 设置图片的最大宽度
            self.imageLabel2.setMaximumWidth(800)
            self.imageLabel2.scaledToWidth(500)  # 设置图片的宽度
            self.imagePathPan = filepath  # 保存图片路径
            self.src = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)  # 用opencv读取图片

    # 图像滤波的应用方法
    def Apply_IMGFusion(self):
        # 获取inputPhoto的图片路径
        enum = self.GetcomboBox_value()
        if self.imagePathMs == None or self.imagePathPan == None:
            self.showFlyout("WARNING", "灾难性错误： 请先导入图片！")
            return
        Ms = cv2.imread(self.imagePathMs)  # 用opencv读取图片Ms
        Pan = cv2.imread(self.imagePathPan)  # 用opencv读取图片Pan
        if enum == -1:
            self.showFlyout("WARNING", "灾难性错误： 请先选择图像融合方法！")
            return
        # 创建opencv窗口（固定大小）
        cv2.namedWindow('Fusion', cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow('Fusion', 1000, 1000)  # 设置窗口的大小
        result = None
        if enum == 1:
            # IHSF图像融合
            # 创建opencv窗口（固定大小）
            fusion = libGD.IHSFusion(Ms, Pan)# 调用libGD库中的IHSF函数
            fusion.Fusion()
            result = fusion.result
        elif enum == 2:
            # GIHSF图像融合
            fusion = libGD.GIHSFusion(Ms, Pan)  # 调用libGD库中的IHSF函数
            fusion.Fusion()
            result = fusion.result
        elif enum == 3:
            # AIHSF图像融合
            fusion = libGD.AIHSFusion(Ms, Pan)  # 调用libGD库中的IHSF函数
            fusion.Fusion()
            result = fusion.result
        elif enum == 4:
            # AIHSF图像融合
            fusion = libGD.IAIHSFusion(Ms, Pan)  # 调用libGD库中的IHSF函数
            fusion.Fusion()
            result = fusion.result
        else:
            return
        self.result = result
        libGD.imshow('Fusion', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 创建浮出警告窗口的方法
    def showFlyout(self, title, content):
        Flyout.create(
            icon=InfoBarIcon.WARNING,
            title= title,
            content= content,
            target=self.button_input_apply,
            parent=self,
            isClosable=True
        )

    # 保存滤波图片的方法
    def Filter_saveImage(self):
        path, ok = QFileDialog.getSaveFileName(
            parent=self,
            caption=self.tr('保存图片'),
            directory=QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),
            filter='TIF (*.tif)'
        )
        if not ok:
            return

        cv2.imwrite(path, self.result/255.0)

