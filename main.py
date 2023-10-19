import os
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import Qt # потрібна константа Qt.KeepAspectRatio для зміни розмірів із збереженням пропорцій
from PyQt5.QtGui import QPixmap # оптимізована для показу на екрані картинка
 
from PIL import Image
from PIL.ImageQt import ImageQt # Для перенесення графіки з Pillow до QT
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)


app = QApplication([])
win = QWidget()

win.setWindowTitle("PHOTOshoP 3000") 
win.resize(700, 500)

btn_folder = QPushButton("Папка")
list_files = QListWidget()

picture = QLabel("Kapтинкa")

btn_left=QPushButton("Bлiво")
btn_right=QPushButton("Вправо")
btn_flip = QPushButton("Віддзеркалити")
btn_sharp = QPushButton("Piзкість")
btn_bw = QPushButton("Ч\Б")

layout = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(list_files)

col2.addWidget(picture)

line = QHBoxLayout()

line.addWidget(btn_left)
line.addWidget(btn_right)
line.addWidget(btn_flip)
line.addWidget(btn_sharp)
line.addWidget(btn_bw)

col2.addLayout(line)

layout.addLayout(col1, 20)
layout.addLayout(col2, 80)

win.setLayout(layout)


workdir = ""
def chooseWorkDir():
   global workdir
   workdir = QFileDialog.getExistingDirectory()


def filter(files, extencions):
   resoult = []
   for filename in files:
      for ext in extencions:
         if filename.endswith(ext):
            resoult.append(filename)
   return resoult


def showFilenamesList():
   chooseWorkDir()
   extencions = [".jpg", ".png", ".jpeg", ".bmp"]
   filenames = filter(os.listdir(workdir), extencions)
   list_files.clear()
   for filename in filenames:
      list_files.addItem(filename)

btn_folder.clicked.connect(showFilenamesList)


class ImageProcessor():
   def __init__(self):
      self.image = None
      self.folder = None
      self.filename = None
      self.save_folder = "Оброблені фото"


   def loadImage(self, folder, filename):
      self.filename = filename
      self.folder = folder
      image_path = os.path.join(folder, filename)
      self.image = Image.open(image_path)


   def showImage(self, path):
      picture.hide()
      pixmapimage = QPixmap(path)
      w, h = picture.width(), picture.height()
      pixmapimage = pixmapimage.scaled(w, h)
      picture.setPixmap(pixmapimage)
      picture.show()


   def saveImage(self):
      path = os.path.join(workdir, self.save_folder)
      if not (os.path.exists(path)):
         os.mkdir(path)
      md_path = os.path.join(path, self.filename)
      self.image.save(md_path)


   def do_bw(self):
      self.image = self.image.convert("L")
      self.saveImage()
      image_path = os.path.join(workdir, self.save_folder, self.filename)
      self.showImage(image_path)


   def do_left(self):
      self.image = self.image.transpose(Image.ROTATE_90)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_folder, self.filename)
      self.showImage(image_path)

   def do_right(self):
      self.image = self.image.transpose(Image.ROTATE_270)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_folder, self.filename)
      self.showImage(image_path)


   def do_flip(self):
      self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_folder, self.filename)
      self.showImage(image_path)


   def do_sharpen(self):
      self.image = self.image.filter(SHARPEN)
      self.saveImage()
      image_path = os.path.join(workdir, self.save_folder, self.filename)
      self.showImage(image_path)


   
workimage = ImageProcessor()


def showChosenImage():
   if list_files.currentRow() >= 0:
      filename = list_files.currentItem().text()
      workimage.loadImage(workdir, filename)
      image_path = os.path.join(workdir, workimage.filename)
      workimage.showImage(image_path)

list_files.currentRowChanged.connect(showChosenImage)



btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_flip.clicked.connect(workimage.do_flip)
btn_sharp.clicked.connect(workimage.do_sharpen)

win.show()
app.exec_()