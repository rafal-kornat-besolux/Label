from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject

import os

from .Template_Label.Label_universal_10x15 import labels_10x15
from .Template_Label.Label_universal_10x5 import labels_10x5

def combining_universal_10x20(writer,setOfDataLabel):
    for i in setOfDataLabel:
            pdf=labels_10x15(i)
            pdf.output("working_labels/10x15"+"\\"+"10x15 "+str(i.uniqueBesoCode)+".pdf")

            pdf=labels_10x5(i)
            pdf.output("working_labels/10x5"+"\\"+"10x5 "+str(i.uniqueBesoCode)+".pdf")
        
            reader1 = PdfFileReader(
                open("working_labels/10x15"+"\\"+"10x15 "+str(i.uniqueBesoCode)+".pdf",'rb'))

            page_10x15 = reader1.getPage(0)
            widthPage1 = page_10x15.mediaBox.getWidth()
            heightPage1 = page_10x15.mediaBox.getHeight()

            reader2 = PdfFileReader(
                open("working_labels/10x5"+"\\"+"10x5 "+str(i.uniqueBesoCode)+".pdf", 'rb'))

            page_10x5 = reader2.getPage(0)
            heightPage2 = page_10x5.mediaBox.getHeight()
            widthPage2 = page_10x5.mediaBox.getWidth()


            translated_page = PageObject.createBlankPage(
                None, 100, 195)
            translated_page.mergeRotatedScaledTranslatedPage(
                page_10x15, 90, 1, heightPage1, heightPage2)
            translated_page.mergeRotatedScaledTranslatedPage(
                page_10x5,0, 1, 0, 0)

            writer.addPage(translated_page)
    return(writer)

def combining_dropshiping_10x20(writer, setOfDataLabel, campaign):
    
    path = "working_labels/VP" +"\\"+ campaign+"\\"+"pdf"
    list_files = os.listdir(path)
    
    for i in setOfDataLabel:

        pdf=labels_10x5(i)
        pdf.output("working_labels/10x5"+"\\"+"10x5 "+str(i.uniqueBesoCode)+".pdf")

        reader1=None

        for j in list_files:
                if str(i.client) in j:
                    reader1 = PdfFileReader(
                        open(path+"\\"+j, 'rb'), strict=False)

        if reader1==None:
            print(i.client)
    
        page_10x15 = reader1.getPage(0)
        # widthPage1 = page_10x15.mediaBox.getWidth()
        # heightPage1 = page_10x15.mediaBox.getHeight()

        reader2 = PdfFileReader(
            open("working_labels/10x5"+"\\"+"10x5 "+str(i.uniqueBesoCode)+".pdf", 'rb'))

        page_10x5 = reader2.getPage(0)
        heightPage2 = page_10x5.mediaBox.getHeight()
        # widthPage2 = page_10x5.mediaBox.getWidth()


        translated_page = PageObject.createBlankPage(
             None, 100, 195)

        translated_page.mergeRotatedScaledTranslatedPage(
                page_10x15,0, 1, 0, heightPage2, expand=True)
        translated_page.mergeRotatedScaledTranslatedPage(
                page_10x5,0, 1, 0, 0, expand=True)

        writer.addPage(translated_page)
    return(writer)

def combining_dropshiping_A4(writer, setOfDataLabel, campaign):
    width_A4 = 595
    height_A4 = 841

    path = "working_labels/VP" +"\\"+ campaign+"\\"+"pdf"
    list_files = os.listdir(path)
    counter = 0
    for i in setOfDataLabel:
        
        pdf=labels_10x5(i)
        pdf.output("working_labels/10x5"+"\\"+"10x5 "+str(i.uniqueBesoCode)+".pdf")

        reader2 = PdfFileReader(
            open("working_labels/10x5"+"\\"+"10x5 "+str(i.uniqueBesoCode)+".pdf", 'rb'))

        page_10x5 = reader2.getPage(0)
        heightPage2 = page_10x5.mediaBox.getHeight()
        widthPage2 = page_10x5.mediaBox.getWidth()
        
        reader1=None

        for j in list_files:
                if str(i.client) in j:
                    reader1 = PdfFileReader(
                        open(path + "\\" + j, 'rb'), strict=False)
        
        if reader1==None:
            print(i.client)
        try:
            page_10x15 = reader1.getPage(0)
        except:
            print(len(list_files))
            print(i.client)
            page_10x15 = reader1.getPage(0)
            
        # widthPage1 = page_10x15.mediaBox.getWidth()
        # heightPage1 = page_10x15.mediaBox.getHeight()

        if counter % 2 == 0:
            
            translated_page = PageObject.createBlankPage(
                None, height_A4, width_A4)
            translated_page.mergeRotatedScaledTranslatedPage(
                page_10x15, 0, 1, 75, heightPage2)
            translated_page.mergeRotatedScaledTranslatedPage(
                page_10x5, 0, 1, 75, 0)

            if counter == len(setOfDataLabel)-1:
                writer.addPage(translated_page)

        elif counter % 2 == 1:


            translated_page.mergeRotatedScaledTranslatedPage(
                page_10x15, 0, 1, height_A4 - widthPage2-75,  heightPage2)
            translated_page.mergeRotatedScaledTranslatedPage(
                page_10x5, 0, 1, height_A4 - widthPage2-75, 0)

            writer.addPage(translated_page)
        counter += 1
    return writer