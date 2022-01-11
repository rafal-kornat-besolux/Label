from .Label_functions import make_Code128, fit, fit2, frame_of_labels, logo

import fpdf


#can be 10x15 and 10x14.5
def labels_10x15(i,x=145, y=100):

    pdf = fpdf.FPDF('p', 'mm', (x, y))  # pdf format
    pdf.set_auto_page_break(auto=True, margin=0.0)

    pdf.add_page()
    frame_of_labels(pdf,100,145)
    # fLabels.frame_of_labels(pdf, y, x)

    number = i.ean

    

    #vertical lines
    pdf.line(60, 60, 60, 100)
    pdf.line(30, 80, 30, 100)
    pdf.line(60, 0, 60, 25)

    #horizontal lines 
    pdf.line(0, 25, x, 25)
    pdf.line(0, 80, 60, 80)
    pdf.line(60, 60, x, 60)  

    logo(pdf,i.brand, 65, 61)

    make_Code128(pdf, number, 5, 3)


    #set font Arial, Bold, 9pt
    pdf.set_font('Arial', 'B', 9)

    #"EAN"

    pdf.set_xy(5, 2)
    pdf.cell(w=0, align="L", txt="EAN")

    #"Reference"
    pdf.set_xy(60, 2)
    pdf.cell(w=0, align="L", txt="Reference")

    #"full name"
    pdf.set_xy(5, 30)
    pdf.cell(w=0, align="L", txt="Full Name")

    #"color"
    pdf.set_xy(5, 50)
    pdf.cell(w=0, align="L", txt="Color")

    #"LEGS PLACEMENT"
    pdf.set_xy(5, 60)
    pdf.cell(w=0, align="L", txt="LEGS PLACEMENT")

    #"PO"
    pdf.set_xy(5, 70)
    pdf.cell(w=0, align="L", txt="PO")

    #set font Arial, Bold, 11pt
    pdf.set_font('Arial', 'B', 11)

    #"Set Number"
    pdf.set_xy(5, 85)
    pdf.cell(w=0, align="c", txt="Set Number")

    #"Packages"
    pdf.set_xy(35, 85)
    pdf.cell(w=0, align="c", txt="Packages")

    #color
    
    text = i.color
    pdf.set_font('Arial', size=fit2(
        62, 4, text, 'Arial'))
    pdf.set_xy(10, 51)
    pdf.cell(w=62, h=6, align="L", txt=text)
    

    #feet_plm
    text = i.legsPlacement

    pdf.set_font('Arial', size=8)
    pdf.set_xy(10, 65)
    pdf.cell(w=0, align="L", txt=text)
    

    #PO
    pdf.set_font('Arial', size=8)
    pdf.set_xy(10, 75)
    pdf.cell(w=0, align="L", txt=i.description)

    #zet
    pdf.set_font('Arial', 'B', size=18)
    pdf.set_xy(12, 93)
    pdf.cell(w=0, align="c", txt=str(i.qty))

    #pack/set
    tekst = str(i.pack)+"/"+str(i.packagesQuantity)
    pdf.set_font('Arial', 'B', size=18)
    pdf.set_xy(40, 93)
    pdf.cell(w=0, align="c", txt=tekst)

    #EAN

    pdf.set_font('Arial', 'B', 7)
    pdf.set_xy(18, 24)
    pdf.cell(w=0, align="L", txt=str(i.ean))

    #ref
    pdf.set_font('Arial', "B", size=fit2(
        70, 12, i.besoRef, 'Arial'))
    pdf.set_xy(60, 10)
    pdf.cell(w=80, h=12, align="C", txt=i.besoRef)

    #full
    text_full = i.full
    if(len(text_full) > 100):
        text_full1 = text_full[:100]
        pdf.set_font('Arial', 'B', size=fit(
            120, text_full1, 'Arial'))
        pdf.set_xy(10, 35)
        pdf.cell(w=0, align="L", txt=text_full1)
        text_full2 = text_full[100:]
        pdf.set_xy(10, 39)
        pdf.cell(w=0, align="L", txt=text_full2)
    else:
        pdf.set_font('Arial', 'B', size=fit(
            90, text_full, 'Arial'))
        pdf.set_xy(10, 37)
        pdf.cell(w=0, align="L", txt=text_full)

    # if ("ww" in df.columns) == True:
    #     #"SKU"
    #     pdf.set_font('Arial', 'B', size=9)
    #     pdf.set_xy(75, 50)
    #     pdf.cell(w=0, align="L", txt="SKU")

    #     #SKU
    #     pdf.set_font('Arial', 'B', size=9)
    #     pdf.set_xy(85, 50)
    #     pdf.cell(w=0, align="L", txt=str(df["ww"][i]))

    #     #"2MH"
    #     pdf.set_font('Arial', 'B', size=11)
    #     pdf.set_xy(120, 44)
    #     pdf.cell(w=0, align="L", txt="2MH")
    

    return pdf