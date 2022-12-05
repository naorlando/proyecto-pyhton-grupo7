import pytesseract
import PIL.Image
import cv2 as cv



myconfig = r"--psm 6 --oem 3"


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

text = pytesseract.image_to_string(PIL.Image.open('proyecto_python/tarea.jpg'),lang='eng' ,config=myconfig)
print(text)