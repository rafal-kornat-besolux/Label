import barcode
from barcode.writer import ImageWriter

import tkinter
from tkinter import font as tkFont

def make_Code128(pdf,number, x, y, w=50, h=20):
    number=str(number)
    code_128=barcode.get('code128', number, writer=ImageWriter())
    number=number.replace("/","_").replace("*","")
    filename=number
    code_128.save("working_labels/code"+"\\"+filename, {"module_width":0.35, "module_height":10, "font_size": 18, "text_distance": 1, "quiet_zone": 3,"write_text": False})

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