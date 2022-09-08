import barcode
from barcode.writer import ImageWriter

from PIL import Image
import math

import tkinter
from tkinter import font as tkFont
from . DictOfLabels import logos_label

def make_Code128(pdf,number, x, y, w=50, h=20,write_text=False):
    number=str(number)
    code_128=barcode.get('code128', number, writer=ImageWriter())
    number=number.replace("/","_").replace("*","")
    filename=number
    code_128.save("working_labels/code"+"\\"+filename, {"module_width":0.35, "module_height":10, "font_size": 18, "text_distance": 1, "quiet_zone": 3,"write_text": write_text})

    pdf.set_xy(x, y)

    pdf.image("working_labels/code"+"\\"+filename+".png", w=w, h=h)

def GetTextDimensions(text, points, font):
    tkinter.Frame().destroy()  # Enough to initialize resources
    arial = tkFont.Font(family=font, size=points)
    width = arial.measure(text)

    return (width/3.779527559055)

def height_to_mm(x):
    return(x/2.835)

def fit2(dl, wys, txt, font):
    
    i = 4
    while True:
        if dl-GetTextDimensions(txt, i, font) > 0 and wys-height_to_mm(i) > 0:
            i = i+1
        else:
            i = i-1
            return(i)

def fit(dl, txt, font):
    i = 4
    while True:
        if dl-GetTextDimensions(txt, i, font) > 0:
            i = i+1
        else:
            i = i-1
            return(i)

def frame_of_labels(pdf, y, x):
    pdf.line(0, 0, 0, y)
    pdf.line(x, 0, x, y)

    pdf.line(0, 0, x, 0)
    pdf.line(0, y, x, y)

def new_size(w, h, img):
    w_img, h_img = img.size
    multiplyer = w/h_img
    w2 = multiplyer*w_img
    if w2 < w:
        return(math.floor(w2), h)
    else:
        multiplyer2 = h/w_img
        h2 = multiplyer2*h_img
        return(w, math.floor(h2))

def logo(pdf, nameOfBrand, x, y):
    
    pdf.set_xy(x, y)
    
    sciezka_loga = "Static"+"\\"+logos_label[nameOfBrand]
    img = Image.open(sciezka_loga)
    a, b = new_size(80, 59, img)
    pdf.image(sciezka_loga,w=a,h=b)