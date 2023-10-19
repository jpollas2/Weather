#get weather info from weather.com and output as html file

import requests
from bs4 import BeautifulSoup as bs
import time
import datetime
import os
from yattag import Doc

CITY='Chicago'
FILEPATH=os.path.join(os.getcwd(), 'report.html')

#specifying degree sign
degree_sign= u'\N{DEGREE SIGN}'
hyphen= u'\N{HYPHEN}'

def get_weather(city):
    #dictionary of city and its corresponding url
    cityNowURL={'champaign': 'https://weather.com/weather/today/l/USIL0209:1:US',
                 'elburn': 'https://weather.com/weather/today/l/USIL0355:1:US',
                 'corpus christi': 'https://weather.com/weather/today/l/USTX0294:1:US',
                        'wisconsin dells':'https://weather.com/weather/today/l/USWI0756:1:US',
                        'chicago':'https://weather.com/weather/today/l/USIL0225:1:US',
                        'ames':'https://weather.com/weather/today/l/USIA0026:1:US'
                        }
    url=cityNowURL[city.lower()]
    #get api from site and make soup object
    r=requests.get(url)
    soup=bs(r.content, "html.parser")

    l=[]
    
    #for what city?
    l.append(city.upper())
    
    #get actual temp info    
    temp=soup.find_all('span', {"data-testid":'TemperatureValue'})
    tempTemp = temp[0].get_text()
    tempString='Temperature: '+tempTemp
    l.append(tempString)

    #get feels like info
    feelTemp = temp[7].get_text()
    feelString='Feels Like: '+feelTemp
    l.append(feelString)

    #get current condition
    curr=soup.find('div', {"data-testid":'wxPhrase'}).get_text()
    currString='Currently '+curr
    l.append(currString)

    #get high and low information
    highTemp = temp[1].get_text()
    lowTemp = temp[2].get_text()
    highString='High: '+highTemp
    lowString='Low: '+lowTemp
    l.append(highString)
    l.append(lowString)

    #get wind and humidity
    many=soup.find_all('div', {"data-testid":'wxData'})
    wind = many[1]
    humid = many[2]
    windTemp = wind.find('span').get_text()
    windString='Wind: '+windTemp
    l.append(windString)
    humidPerc=humid.find('span').get_text()
    humidString='Humidity: '+humidPerc
    l.append(humidString)

    #creates the text message that can be passed to the sms portion
    global message
    message=''
    for i in l:
        message=message+i+'<br>'


def get_5day(city):
    #dict of cities and corresponding url's
    city10URL={'champaign': 'https://weather.com/weather/5day/l/USIL0209:1:US'
             ,'elburn': 'https://weather.com/weather/5day/l/USIL0355:1:US'
             ,'corpus christi': 'https://weather.com/weather/5day/l/USTX0294:1:US'
             ,'chicago':'https://weather.com/weather/5day/l/USIL0225:1:US'
             ,'wisconsin dells':'https://weather.com/weather/5day/l/USWI0756:1:US'
             ,'ames':'https://weather.com/weather/5day/l/USIA0026:1:US'
               }
    url=city10URL[city.lower()]
    #scrapes site
    r=requests.get(url)
    soup=bs(r.content,'html.parser')

    #gets the next 5 days and puts into a list
    x=soup.find_all(class_='date-time')
    y=list(x)
    days=[]
    for i in y:
        days.append(i.text)

    #gets descriptions for each day and puts into list
    x1=soup.find_all(class_='description')
    y1=list(x1)
    descriptions=[]
    for i in y1:
        descriptions.append(i.get_text())

    #gets hi-lo's for each day and puts into list
    x2=soup.find_all(class_='temp')
    y2=list(x2)
    hilo=[]
    for i in y2:
        hilo.append(i.get_text())

    #remove description
    descriptions.pop(0)
    #remove hilo
    hilo.pop(0)

    #split the hilo's
    i=0
    hilos=[]
    while i < len(hilo):
        if i==0:
            #only first two chars
            high=hilo[i][0:2]
            low=hilo[i][2:]
        else:
            #first 3 chars
            high=hilo[i][0:3]
            low=hilo[i][3:]
        #add high/low to list
        add=(high,low)
        hilos.append(add)
        i=i+1
    
    #for every day in the list, create a line that will display day: description, hilo
    m=''
    i=0
    while i<len(days):
        z=days[i]+': '+descriptions[i]+', '+hilos[i][0]+' / '+hilos[i][1]+'<br>'
        m=m+z
        i=i+1

    global m5
    m5=m

def get_hour(city):
    #dict of cities and corresponding url's
    cityHourURL={'champaign': 'https://weather.com/weather/hourbyhour/l/USIL0209:1:US'
             ,'elburn': 'https://weather.com/weather/hourbyhour/l/USIL0355:1:US'
             ,'corpus christi': 'https://weather.com/weather/hourbyhour/l/USTX0294:1:US'
             ,'chicago':'https://weather.com/weather/hourbyhour/l/USIL0225:1:US'
             ,'wisconsin dells':'https://weather.com/weather/hourbyhour/l/USWI0756:1:US'
             ,'ames':'https://weather.com/weather/hourbyhour/l/USIA0026:1:US'
                 }
    url=cityHourURL[city.lower()]
    #scrapes site
    r=requests.get(url)
    soup=bs(r.content,'html.parser')

    #get next data about next four hours
    rows = soup.find_all('details', {'data-testid':'ExpandedDetailsCard'})

    i=1
    global me
    me = ''
    while i < 13:
        vals = rows[i].find('div', {'data-testid':'DetailsSummary'})
        atime = vals.find('h2').get_text()
        atemp = vals.find('span', {'data-testid':'TemperatureValue'}).get_text()
        asky = vals.find('span', {'class':'aaFeV'}).get_text()
        aprecip = vals.find('span', {'data-testid':'PercentageValue'}).get_text()
        awind = vals.find('span', {'data-testid':'Wind'}).get_text()
        me = me + atime+' | '+atemp+' | '+asky+' | '+aprecip+' | '+awind+'<br>'
        i = i + 1


def run(city,filepath):

    #run weather fetching functions
    get_weather(city) #message
    get_5day(city) #m5
    get_hour(city) #me

    #encode information to string (ignores degree signs)
    m1=message.encode('ascii','ignore')
    m2=m5.encode('ascii','ignore')
    m3=me.encode('ascii','ignore')

    #get date and time info
    dt=time.strftime("%m/%d/%Y")
    tm=time.strftime("%I:%M")
    now = datetime.datetime.now()
    day=now.strftime("%A")
    dayString=' For '+day+' ('+dt+') at '+tm
    
    htmlString='''
    <html>
        <h1>Weather Report {ds}</h1>
        <body>
            <h3>Current Conditions</h3>
            <p>{m1}</p>
            <h3>Next 5 Days</h3>
            <p>{m2}</p>
            <h3>Next Few Hours</h3>
            <p>{m3}</p>
        </body>
    </html>
    '''.format(m1=m1.decode('utf-8')
               , m2=m2.decode('utf-8')
               , m3=m3.decode('utf-8')
               , ds=dayString)
    f=open(filepath,'w')
    f.write(htmlString)
    f.close()

    os.startfile(filepath)


run(CITY,FILEPATH)
