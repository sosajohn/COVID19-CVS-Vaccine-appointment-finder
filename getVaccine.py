import requests
import datetime
import time
import beepy
import smtplib

def sendEmail(city):
    gmail_user = 'someone@gmail.com'
    gmail_password = '#############'
    
    sent_from = gmail_user
    to = 'someone@gmail.com'
    text = 'Appointment slot found in ' + city
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, text)
        server.close()
    
        print ('Email sent!')
    except:
        print ('Something went wrong sending the email.')    

def findAppointment():
    while True:
        state = 'CA' 

        try:
            response = requests.get("https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{}.json?vaccineinfo".format(state.lower()), headers={"Referer":"https://www.cvs.com/immunizations/covid-19-vaccine"})
            payload = response.json()
    
            cities = ['SANTA CRUZ', 'SCOTTS VALLEY', 'LOS GATOS', 'CAPITOLA', 'APTOS'] 
    
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            for item in payload["responsePayloadData"]["data"][state]:
                city = item['city']
                status = item['status']
                
                if city in cities:
                    print(city, status)
                    if status != 'Fully Booked':
                        beepy.beep(sound = 'coin')
                        beepy.beep(sound = 'coin')
                        beepy.beep(sound = 'coin')
                        sendEmail(city)                
        except:
            print('Something went wrong fetching and processing the appointment data.')
            
        time.sleep(60)
        print('\n')

findAppointment()
