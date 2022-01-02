import os
import re
import shutil
import requests

def zpl_to_pdf_bzc(numberOfBzc="104087"):

    path = "working_labels/BZC/zpl"
    list_files = os.listdir(path)
    for j in list_files:
        if numberOfBzc in j:
            file = j
    
    with open(path+"\\"+file, "r",encoding="utf-8") as zpl:
        contents = zpl.read()

    
    pathCheck = "working_labels/BZC"+"\\"+"campaign"+"\\"+numberOfBzc
    pathOut = pathCheck+"\\"+"pdf"
    if os.path.isdir(pathCheck) == False:
        os.mkdir(pathCheck)
        os.mkdir(pathOut)
    elif os.path.isdir(pathOut) == False:
        os.mkdir(pathOut)
        


    array_labels=contents.split("^XZ")
    dictOfBZC={}
    for j in range(len(array_labels)):
        array_labels[j]=array_labels[j]+"^XZ"

        # change french symbols
        array_labels[j]=array_labels[j].replace("C)","é")
        array_labels[j]=array_labels[j].replace("C(","è")

        # adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
        url = 'http://api.labelary.com/v1/printers/8dpmm/labels/4x6/0/'
        files = {'file' : array_labels[j]}
        try:
            zpl_ref = re.search(r'(?<=FO535,767\^FD).*(?=\^FS\^FO535,766)',array_labels[j]).group()   
            zpl_id  = re.search(r'(?<=\^FO15,23\^FD).*(?=\^FS\^CF0,23,23)',array_labels[j]).group()
            zpl_bzc  = re.search(r'(?<=FO565,767\^FD).*(?=\^FS\^FO566,767)',array_labels[j]).group()
            zpl_bzc = zpl_bzc.replace("Réf Article :       ","")

        except:
            print(j)
        
        headers = {'Accept' : 'application/pdf'} 

        response = requests.post(url, headers = headers, files = files, stream = True)
        if response.status_code == 200:
            response.raw.decode_content = True
            path=pathOut+"/"+numberOfBzc+"-"+zpl_bzc+"-"+zpl_id+".pdf"
            if os.path.exists(path) != True:
                with open(path,'wb') as out_file: # change file name for PNG images
                    shutil.copyfileobj(response.raw, out_file)
            else:
               print("mistake")
            dictOfBZC[j]={
               "REF":zpl_ref,
                "BZC":zpl_bzc,
                "ID":zpl_id,
                "PACK":zpl_id[-5:-4],
                "SET":zpl_id[-3:-2] 
            }
        else:
            print('Error: ' + response.text)

    return dictOfBZC    