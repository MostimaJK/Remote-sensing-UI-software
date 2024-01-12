import os

this_dir = os.path.dirname(__file__)
os.add_dll_directory(this_dir + "\\")

os.add_dll_directory(this_dir)
import sys
sys.path.append(this_dir)


import GD
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QImage
# Path: libGD.py

def toQPixmap(img: np.ndarray):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    height, width, channel = img.shape
    bytesPerLine = 3 * width
    qImg = QPixmap(QPixmap.fromImage(QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)))
    return qImg

def toNDarray(img: QPixmap):
    img = img.toImage()
    width = img.width()
    height = img.height()
    byte_string = img.bits().asstring(width * height * 4)
    img_array = np.frombuffer(byte_string, np.uint8).reshape((height, width, 4))
    return img_array

class filter:
    def __init__(self, img: np.ndarray):
        self.src = img
    
    def Filter(self, kernel: np.ndarray):
        res = None
        if self.src.dtype == np.uint8:
            res = GD.filterui8(self.src, kernel)
        elif self.src.dtype == np.float32:
            res = GD.filterf32(self.src, kernel)
        self.result = res
        return res
    
    def save(self, filePath):
        cv2.imwrite(filePath, self.result)

class Medianfilter:
    def __init__(self, img: np.ndarray):
        self.src = img
    
    def Filter(self):
        res = None
        if self.src.dtype == np.uint8:
            res = GD.Medianfilterui8(self.src)
        elif self.src.dtype == np.float32:
            res = GD.Medianfilterf32(self.src)
        self.result = res
        return res
    
    def save(self, filePath):
        cv2.imwrite(filePath, self.result)

class Gaussianfilter:
    def __init__(self, img: np.ndarray):
        self.src = img

    def Filter(self, ksize, stdx, stdy):
        res = None
        if self.src.dtype == np.uint8:
            res = GD.Gaussianfilterui8(self.src, ksize, stdx, stdy)
        elif self.src.dtype == np.float32:
            res = GD.Gaussianfilterf32(self.src, ksize, stdx, stdy)
        self.result = res
        return res
    
    def save(self, filePath):
        cv2.imwrite(filePath, self.result)

class Sobel:
    def __init__(self, img: np.ndarray):
        self.src = img

    def Filter(self):
        res = None
        if self.src.dtype == np.uint8:
            res = GD.Sobelui8(self.src)
        elif self.src.dtype == np.float32:
            res = GD.Sobelf32(self.src)
        self.result = res
        return res
    
    def save(self, filePath):
        cv2.imwrite(filePath, self.result)

class Laplacian:
    def __init__(self, img: np.ndarray):
        self.src = img

    def Filter(self):
        res = None
        if self.src.dtype == np.uint8:
            res = GD.Laplaceui8(self.src)
        elif self.src.dtype == np.float32:
            res = GD.Laplacef32(self.src)
        self.result = res
        return res
    
    def save(self, filePath):
        cv2.imwrite(filePath, self.result)

class toGray:
    def __init__(self, img: np.ndarray):
        self.src = img

    def Filter(self):
        res = None
        if self.src.dtype == np.uint8:
            res = GD.toGrayui8(self.src)
        elif self.src.dtype == np.float32:
            res = GD.toGrayf32(self.src)
        self.result = res
        return res
    
    def save(self, filePath):
        cv2.imwrite(filePath, self.result)

class IHSFusion:
    def __init__(self, Ms:np.ndarray, Pans:np.ndarray):
        self.Ms = Ms
        self.Pans = Pans

    def Fusion(self):
        res = None
        if self.Ms.dtype != self.Pans.dtype:
            raise Exception("Ms and Pans must be the same dtype") 
        if self.Ms.dtype == np.uint8:
            res = GD.IHSFusingui8(self.Ms, self.Pans)
        elif self.Ms.dtype == np.float32:
            res = GD.IHSFusingf32(self.Ms, self.Pans)
        self.result = res
        return res
    
    def save(self, filePath):
        cv2.imwrite(filePath, self.result)

class GIHSFusion:
    def __init__(self, Ms:np.ndarray, Pans:np.ndarray):
        self.Ms = Ms
        self.Pans = Pans

    def Fusion(self):
        res = None
        if self.Ms.dtype != self.Pans.dtype:
            raise Exception("Ms and Pans must be the same dtype")
        if self.Ms.dtype == np.uint8:
            res = GD.GIHSFusingui8(self.Ms, self.Pans)
        elif self.Ms.dtype == np.float32:
            res = GD.GIHSFusingf32(self.Ms, self.Pans)
        self.result = res
        return res
    
    def save(self, filePath):
        cv2.imwrite(filePath, self.result)

class AIHSFusion:
    def __init__(self, Ms:np.ndarray, Pans:np.ndarray):
        self.Ms = Ms
        self.Pans = Pans

    def Fusion(self):
        res = None
        if self.Ms.dtype != self.Pans.dtype:
            raise Exception("Ms and Pans must be the same dtype")
        if self.Ms.dtype == np.uint8:
            res = GD.AIHSFusingui8(self.Ms, self.Pans)
        elif self.Ms.dtype == np.float32:
            res = GD.AIHSFusingf32(self.Ms, self.Pans)
        self.result = res
        return res
    
    def save(self, filePath):
        cv2.imwrite(filePath, self.result)

class IAIHSFusion:
    def __init__(self, Ms:np.ndarray, Pans:np.ndarray):
        self.Ms = Ms
        self.Pans = Pans

    def Fusion(self):
        res = None
        if self.Ms.dtype != self.Pans.dtype:
            raise Exception("Ms and Pans must be the same dtype")
        if self.Ms.dtype == np.uint8:
            res = GD.IAIHSFusingui8(self.Ms, self.Pans)
        elif self.Ms.dtype == np.float32:
            res = GD.IAIHSFusingf32(self.Ms, self.Pans)
        self.result = res
        return res
    
    def save(self, filePath):
        cv2.imwrite(filePath, self.result)

class SLICSegment:
    def __init__(self, img:np.ndarray, gradient_reflected:np.ndarray):
        self.src = img
        self.gradient_reflected = gradient_reflected

    def Segment(self, K):
        res = None
        if self.src.dtype == np.uint8:
            res = GD.SLICSegmentui8(self.src, self.gradient_reflected, K)
        elif self.src.dtype == np.float32:
            res = GD.SLICSegmentf32(self.src, self.gradient_reflected, K)
        self.result = res
        return res
    
    def save(self, filePath):
        cv2.imwrite(filePath, self.result)

def reflect(img: np.ndarray):
    res = None
    if img.dtype == np.uint8:
        res = GD.ReflectImgui8(img)
    elif img.dtype == np.float32:
        res = GD.ReflectImgf32(img)
    return res

def HistogramEqualization(img: np.ndarray):
    res = None
    if img.dtype == np.uint8:
        res = GD.HistgramEqualizeui8(img)
    elif img.dtype == np.float32:
        res = GD.HistgramEqualizef32(img)
    return res


def Information():
    print(GD.GDInformation())



def testWorking():
    print(GD.test())

def imshow(title, img:np.ndarray):
    if img.dtype == np.float32:
        cv2.imshow(title, img / 255.0)
    else:
        cv2.imshow(title, img)

workplace = "D:\\LearnRS\\LearnRS\\output\\"

if __name__ == "__main__":
    testWorking()
    Information()