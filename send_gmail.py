import credentials
import stock_data

import smtplib
import imghdr
import os

from email.message import EmailMessage

def send(df):
    msg = EmailMessage()
    msg['Subject'] = 'Update Wishlist'
    msg['From'] = credentials.EMAIL_ADRESS
    msg['To'] = credentials.EMAIL_ADRESS
    msg.set_content('Your stock info ')
    
    msg.add_alternative(df, subtype='html')

    directory = os.fsencode('plots/')
    for file in os.listdir(directory):
        name_of_file = os.fsdecode(file)
        if str(stock_data.TODAYS_DATE.strftime('%Y-%m-%d')) not in name_of_file:
            os.remove('plots/'+name_of_file)
        else:
            with open("plots/"+name_of_file, 'rb') as f:
                    file_data = f.read()
                    file_type = imghdr.what(f.name)
                    file_name = f.name
            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename = file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(credentials.EMAIL_ADRESS, credentials.EMAIL_PASSWORD)    
        smtp.send_message(msg)
        print('ERFOLGREICH VERSENDET')

"""
send with local email: 
- input into consol: python -m smtpd -c DebuggingServer -n localhost:1025
- comment out smtp.ehol and starttls and login
- comment out with smtplib.SMTP('smtp.gmail.com', 587) as smtp: and use with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
"""