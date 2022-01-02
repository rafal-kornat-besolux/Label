import pandas as pd

def campaign_to_dic(name):
    path="working_labels/VP"+"\\"+name
    df = pd.read_excel(path+"\\"+name+"-all.xlsx")
    df=df[["Parcel number","Transporter","ref","pack","rep"]]
    df=df.transpose()
    dic=df.to_dict()
    return(dic)