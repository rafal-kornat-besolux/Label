import fpdf

from .Label_functions import make_Code128, fit2, frame_of_labels


def labels_10x5(i):
    
    pdf = fpdf.FPDF('p', 'mm', (100, 50))

    pdf.add_font('DejaVu', '', 'STATIC/FONT/DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'STATIC/FONT/DejaVuSansCondensed-Bold.ttf', uni=True)

    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=0.0)


    make_Code128(pdf, number=i.uniqueBesoCode, x=0, y=39,w=100,h=10)

    pdf.set_font('DejaVu', 'B', 12)
    text = str(i.uniqueBesoCode)
    pdf.set_xy(0, 33)
    pdf.cell(w=90,h=7, align="C", txt=text)
    

    # fLabels.frame_of_labels(pdf, 50, 100)
    pdf.line(0, 11, 100, 11)
    pdf.line(0, 22, 100, 22)
    pdf.line(0, 33, 100, 33)

    pdf.line(13, 11, 13, 22)
    pdf.line(26, 11, 26, 22)
    pdf.line(40, 11, 40, 22)
    pdf.line(35, 22, 35, 33)
    pdf.line(70, 22, 70, 33)

    pdf.set_font('DejaVu', 'B', 5)
    pdf.set_xy(35, 22)
    pdf.cell(w=35, h=11, fill=True)

    #pdf.set_xy(2, 2)
    #pdf.cell(w=0, align="L", txt="Reference")
    pdf.set_xy(2, 13)
    pdf.cell(w=0, align="L", txt="Packages")
    pdf.set_xy(15, 13)
    pdf.cell(w=0, align="L", txt="Quantity")
    pdf.set_xy(28, 13)
    pdf.cell(w=0, align="L", txt="LP")

    
    

    text = str(i.besoRef)
    pdf.set_font('DejaVu', 'B', fit2(
        70, 7, text, 'DejaVu'))
    pdf.set_xy(2, 3)

    pdf.cell(w=96, h=7, align="C", txt=text)

    pdf.set_xy(42, 13)
    text = i.order+"/"+i.country
    pdf.set_font('DejaVu', 'B', fit2(
        50, 7, text, 'DejaVu'))
    pdf.cell(w=56, h=7, align="C", txt=text)

    
    
    pdf.set_xy(70, 22)
    text = i.brand
    pdf.set_font('DejaVu', 'B', fit2(
        28, 10, text, 'DejaVu'))
    pdf.cell(w=30, h=10, align="C", txt=text)

    if "BEX" in i.order:
        pdf.set_xy(1, 23)
        text = i.factoryRef
        pdf.set_font('DejaVu', '', fit2(
            30, 4, text, 'DejaVu'))
        pdf.cell(w=33, h=4, align="C", txt=text)

    # if df["ORDER"][0][-3:] == "DOL":
    #     pdf.set_xy(1, 23)
    #     text = removeAccents(str(df["Strona"][i]))
    #     pdf.cell(w=33, h=4, align="C", txt=text)

    pdf.set_xy(1, 28)
    text = i.fabric
    if text != "nan":
        pdf.set_font('DejaVu', 'B', fit2(
            32, 5, text, 'DejaVu'))
        pdf.cell(w=33, h=5, align="C", txt=text)


    

    text = str(i.pack)+"/"+str(i.packagesQuantity)

    pdf.set_font('DejaVu', 'B', fit2(
                    12, 6, text, 'DejaVu'))
    pdf.set_xy(1, 14)
    pdf.cell(w=12, h=7, align="C", txt=text)

    
    text = str(i.qty)

    pdf.set_font('DejaVu', 'B', fit2(
                    12, 6, text, 'DejaVu'))
    pdf.set_xy(14, 14)
    pdf.cell(w=12, h=7, align="C", txt=text)

    text = str(i.ordN)
    
    pdf.set_font('DejaVu', 'B', fit2(
                    12, 6, text, 'DejaVu'))
    pdf.set_xy(27, 14)
    pdf.cell(w=12, h=7, align="C", txt=text)

    pdf.set_font('DejaVu', 'B', 7)

    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(0, 0)
    pdf.set_xy(35, 22)

    if i.infoFactory!="":
        text = i.infoFactory
        pdf.set_font('DejaVu', 'B', fit2(30, 10, text, 'DejaVu'))
        pdf.cell(w=35, h=11, align="C", txt=text)
    elif i.order[:3] == "DAS":
        text = i.ean
        pdf.set_font('DejaVu', 'B', fit2(30, 10, text, 'DejaVu'))
        pdf.cell(w=35, h=11, align="C", txt=text)
        
    # vr = 0
    # try:
    #     if df["ORDER"][0][-3:] == "DAS":
    #         text = str(int(df["EAN"][i]))
    #         vr = 1
    #     elif df["ORDER"][0][-3:] == "CPT":
    #         if "," in df["FABRIC"][i]:
    #             text = str(df["FABRIC"][i].split(",")[1])
    #             vr = 1
    #     else:
    #         if ("SetNo" in df.columns) == True:
    #             text = str(df["SetNo"][i])
    #             vr = 1
    #         elif ("seria" in df.columns) == True:

    #             if df["seria"].isnull()[i] != True:
    #                 text = str(df["seria"][i])
    #                 vr = 1
    # except:
    #     vr = 0

    # if vr == 1:
    #     pdf.set_font('DejaVu', 'B', fLabels.fit2(
    #         30, 10, text, 'DejaVu'))
    #     pdf.cell(w=35, h=11, align="C", txt=text)
    frame_of_labels(pdf,50,100)

    return pdf