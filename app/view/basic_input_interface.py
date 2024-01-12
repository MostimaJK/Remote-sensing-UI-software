# coding:utf-8
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

from .gallery_interface import GalleryInterface
from ..common.translator import Translator



class BasicInputInterface(GalleryInterface):
    """ Basic input interface """

    # 初始化方法
    def __init__(self, parent=None):
        t = Translator()
        self.src = None
        super().__init__(
            title=t.basicInput,
            subtitle='遥感原理与图像处理-图像滤波',
            parent=parent
        )
        self.imagePath = None
        self.setObjectName('basicInputInterface')

        # 浮出命令栏
        self.widget = QWidget(self)
        self.widget.setLayout(QVBoxLayout())  # 设置布局为垂直布局
        self.widget.layout().setContentsMargins(0, 0, 0, 0)  # 设置布局的边距
        self.widget.layout().setSpacing(10)  # 设置布局的间距

        # 创建导入图片按钮A
        self.button_input_A = PushButton(self.tr("导入图片"))
        self.button_input_A.setFixedWidth(180)  # 设置按钮大小
        self.h_layout = QHBoxLayout(self.widget)  # 创建水平布局
        self.h_layout.setSpacing(10)  # 设置水平布局的间距
        self.h_layout.addWidget(self.button_input_A, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中
        self.vBoxLayout.addLayout(self.h_layout)  # 将水平布局添加到垂直布局中
        self.button_input_A.clicked.connect(self.inputPhoto)  # 连接按钮的点击信号导入图片并显示

        # 创建下拉框
        self.comboBox_filter = ComboBox()  # 创建下拉框
        self.comboBox_filter.setPlaceholderText("请选择图像滤波方法")
        items = ['中值滤波', '高斯滤波', 'Sobel算子', 'Laplace算子']  # 下拉框的选项
        self.comboBox_filter.addItems(items)  # 添加下拉框的选项
        self.comboBox_filter.setCurrentIndex(-1)  # 设置下拉框的默认选项
        self.comboBox_filter.setFixedWidth(100)  # 设置下拉框的宽度
        self.comboBox_filter.setMaximumWidth(180)  # 设置下拉框的最大宽度
        self.h_layout.addWidget(self.comboBox_filter, 0, Qt.AlignLeft)  # 将下拉框添加到水平布局中
        self.comboBox_filter.currentIndexChanged.connect(self.GetcomboBox_value)  # 当下拉框的选项改变时，触发事件

        # 创建导入Apply按钮
        self.button_input_apply = PushButton(self.tr("Apply"))
        self.button_input_apply.setFixedWidth(100)  # 设置按钮大小
        self.button_input_apply.clicked.connect(self.Apply_Filter)  # 连接按钮的点击信号导入图片并显示
        self.h_layout.addWidget(self.button_input_apply, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中


        # 创建保存滤波图像按钮
        self.button_input_save = PrimaryPushButton(self.tr("保存滤波图像"))
        self.button_input_save.setFixedWidth(120)  # 设置按钮大小
        self.h_layout.addWidget(self.button_input_save, 0, Qt.AlignLeft)  # 将按钮添加到水平布局中
        self.button_input_save.clicked.connect(self.Filter_saveImage)  # 连接按钮的点击信号导入图片并显示

        label = QLabel(self.tr('单击图片打开命令栏，图片将在滤波后自动更换！'))
        self.imageLabel = ImageLabel('Photos/resource/interface_background/aiyafla.jpg')
        self.imageLabel2 = ImageLabel('Photos/resource/interface_background/Storm2k.jpg')  # 创建一个ImageLabel对象

        # 创建一个水平布局
        self.h_layout_photos = QHBoxLayout(self.widget)
        self.h_layout_photos.setSpacing(10)  # 设置水平布局的间距
        self.h_layout_photos.addWidget(self.imageLabel, 0, Qt.AlignLeft)  # 将图片A添加到水平布局中
        self.h_layout_photos.addWidget(self.imageLabel2, 0, Qt.AlignLeft)  # 将图片B添加到水平布局中

        # 创建高斯滤波时的三个输入框
        self.lineEdit_Ksize = LineEdit()  # 创建输入框Ksize核大小
        self.lineEdit_stdx = LineEdit()  # 创建输入框stdx标准差x
        self.lineEdit_stdy = LineEdit()  # 创建输入框stdy标准差y
        self.lineEdit_Ksize.setPlaceholderText("Ksize")
        self.lineEdit_stdx.setPlaceholderText("stdx")
        self.lineEdit_stdy.setPlaceholderText("stdy")
        self.lineEdit_Ksize.setFixedWidth(100)  # 设置输入框的宽度
        self.lineEdit_stdx.setFixedWidth(100)  # 设置输入框的宽度
        self.lineEdit_stdy.setFixedWidth(100)  # 设置输入框的宽度
        self.h_layout2 = QHBoxLayout(self.widget)  # 创建水平布局
        self.h_layout2.addWidget(self.lineEdit_Ksize, 0, Qt.AlignLeft)  # 将输入框添加到水平布局中
        self.h_layout2.addWidget(self.lineEdit_stdx, 0, Qt.AlignLeft)  # 将输入框添加到水平布局中
        self.h_layout2.addWidget(self.lineEdit_stdy, 0, Qt.AlignLeft)  # 将输入框添加到水平布局中
        self.h_layout2.setSpacing(10)  # 设置水平布局的间距
        self.h_layout.addLayout(self.h_layout2)  # 将水平布局添加到垂直布局中
        self.lineEdit_Ksize.setEnabled(False)
        self.lineEdit_stdx.setEnabled(False)
        self.lineEdit_stdy.setEnabled(False)

        # 设置图片功能
        self.imageLabel.scaledToWidth(500)  # 设置图片的宽度
        self.imageLabel2.scaledToWidth(500)  # 设置图片的宽度
        self.imageLabel.setBorderRadius(8, 8, 8, 8)  # 设置图片的圆角
        self.imageLabel2.setBorderRadius(8, 8, 8, 8)  # 设置图片的圆角
        self.imageLabel.clicked.connect(self.createCommandBarFlyout)  # 连接图片的点击信号，打开命令栏
        self.imageLabel2.clicked.connect(self.createCommandBarFlyout)  # 连接图片的点击信号，打开命令栏


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
        if comboBox_value == '中值滤波':
            res = 1
        elif comboBox_value == '高斯滤波':
            res = 2
        elif comboBox_value == 'Sobel算子':
            res = 3
        elif comboBox_value == 'Laplace算子':
            res = 4
        else:
            res = -1

        if res == 2:
            self.lineEdit_Ksize.setEnabled(True)
            self.lineEdit_stdx.setEnabled(True)
            self.lineEdit_stdy.setEnabled(True)
        else:
            self.lineEdit_Ksize.setEnabled(False)
            self.lineEdit_stdx.setEnabled(False)
            self.lineEdit_stdy.setEnabled(False)
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
            self.imagePath = filepath  # 保存图片路径
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
            self.imagePathFin = filepath  # 保存图片路径
            self.src = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)  # 用opencv读取图片


    def get_input_box(self):
        size_value = self.lineEdit_Ksize.text()
        stdx_value = self.lineEdit_stdx.text()
        stdy_value = self.lineEdit_stdy.text()
        if size_value == '' or stdx_value == '' or stdy_value == '':
            return 0, 0, 0
        else:
            return int(size_value), float(stdx_value), float(stdy_value)


    # 图像滤波的应用方法
    def Apply_Filter(self):
        # 获取下拉框的选项
        enum = self.GetcomboBox_value()
        # 判断inputPhoto的图片路径
        if self.imagePath == None:
            self.showFlyout("WARNING", "灾难性错误： 请先导入图片！")
            return
        img = cv2.imread(self.imagePath)  # 用opencv读取图片
        if enum == -1:
            self.showFlyout("WARNING", "灾难性错误： 请先选择图像滤波方法！")
            return
        result = None
        if enum == 1:
            # 中值滤波
            filter = libGD.Medianfilter(img)  # 调用libGD库中的中值滤波函数
            filter.Filter()  # 调用中值滤波函数
            result = filter.result
        elif enum == 2:
            # 高斯滤波
            # 如果输入框未全部填写则警告
            # 获取三个输入框的值
            ksize_value, stdx_value, stdy_value = self.get_input_box()
            if ksize_value == 0 or stdx_value == 0 or stdy_value == 0:
                self.showFlyout("WARNING", "参数错误： 参数必须全部填写！")
                return
            if ksize_value < 0 or stdx_value < 0 or stdy_value < 0:
                self.showFlyout("WARNING", "参数错误： 参数必须全大于0")
                return
            if ksize_value % 2 == 0:
                self.showFlyout("WARNING", "参数错误： 参数Ksize必须是奇数！")
                return
            filter = libGD.Gaussianfilter(img)  # 调用libGD库中的高斯滤波函数
            filter.Filter(ksize_value, stdx_value, stdy_value)  # 调用高斯滤波函数
            result = filter.result
        elif enum == 3:
            # Sobel算子
            filter = libGD.Sobel(img)  # 调用libGD库中的Sobel算子
            filter.Filter()  # 调用Sobel算子
            result = filter.result
        elif enum == 4:
            # Laplacian算子
            filter = libGD.Laplacian(img)  # 调用libGD库中的Laplacian算子
            filter.Filter()  # 调用Laplacian算子
            result = filter.result
        else:
            return
        self.result = result
        # 将处理后的图片显示在imagePathFin窗口中
        self.imageLabel2.setPixmap(libGD.toQPixmap(result))
        self.imageLabel2.scaledToWidth(500)
        # 创建opencv窗口（固定大小）
        cv2.namedWindow('Filter', cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow('Filter', 1000, 1000)  # 设置窗口的大小
        cv2.imshow('Filter', result)  # 用opencv显示图片
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

        cv2.imwrite(path, self.result)

