import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import pandas as pd
from datetime import datetime
import time
import warnings
warnings.filterwarnings('ignore')

#credentials of user to send mail
# myMail='testingbirthday12'
# key='viocgysjfqjmugsm'
myMail='bt20ece121@students.vnit.ac.in'
key='dkztkbkiexetuklp'
to=['bt20ece121@students.vnit.ac.in']
location=r"C:\Users\rmsre\Downloads\EnailData.csv"
imagelocation=r"C:\Users\rmsre\Downloads\smitiPapa.jpg"

def makeData(location):
    data={'Name':['Ranga','Chinna','Sabareesh'],'Email':[myMail,'rmsreddy17@gmail.com','chakkasabareesh45@gmail.com'],'Birthday':['16-7-2003','17-2-2003','16-07-2003']}
    df=pd.DataFrame(data)
    print(df)
    df.to_csv(location,index=False)

def sendMail(to_addrs,type,name,imagePath=None,attachmentsPath=None):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(myMail, key)
    [subject,text,imagePath,attachmentsPath]=select(type,name)
    msg=message(subject=subject,text=text,image=imagePath,attachments=attachmentsPath)
    msg['from']=myMail
    msg['to']=to_addrs
    smtp.sendmail(myMail,to_addrs,msg.as_string())
    smtp.quit()

def select(type,name):
    if(type=="Birthday"):
        return ["Happy Birthday","Wish you many more happy returns of the day "+name,imagelocation,None]
    elif(type=="Meeting"):
        return ["Meeting remainder","You have sheduled a meeting today "+name,None,None]
    return ["Test mail","This mail is sent for testing",None,None]

def message(subject="",text="",image=None,attachments=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    if image is not None:
        if type(image) is not list:
            image=[image]
        for img in image:
            img_data=open(img,'rb').read()
            msg.attach(MIMEImage(img_data,directory=os.path.basename(img)))
    if attachments is not None:
        if type(attachments) is not list:
            attachments=[attachments]
        for attachment in attachments:
            with open(attachment,'rb') as f:
                file = MIMEApplication(f.read(),directory=os.path.basename(attachment))
            file['Content-Disposition'] = f'attachment;\filename="{os.path.basename(attachment)}"'
            msg.attach(file)
    return msg

def dataPart(location):
    df=pd.read_csv(location)
    print(df)
    today=datetime.now().strftime("%d-%m")
    # iloc
    for idx,item in df.iterrows():
        bday=datetime.strptime(item['Birthday'], "%d-%m-%Y")
        bday=bday.strftime("%d-%m")
        if(bday==today):
            sendMail(to_addrs=item['Email'],type="Birthday",name=item['Name'])

if __name__=="__main__":
    # makeData(location)    # optimal to make data or directly read the csv file
    currTime=time.now()
    if(currTime=='10:00'):
        dataPart(location)
        time.sleep(86400-400)
    else:
        time.sleep(50)
    # sendMail(myMail,key,to)
