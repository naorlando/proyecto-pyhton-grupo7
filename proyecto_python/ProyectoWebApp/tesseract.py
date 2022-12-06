import pytesseract
import PIL.Image
import cv2 as cv
import json



myconfig = r"--psm 6 --oem 3"


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

text = pytesseract.image_to_string(PIL.Image.open('proyecto_python/foto.png'),lang='eng' ,config=myconfig)

texto_limpio = text.replace("\n\n", "\n")

lineas = texto_limpio.split('\n')

lineas.remove('')

print(lineas)







