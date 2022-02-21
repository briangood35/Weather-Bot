from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import smtplib

###############################################################################
#                                                                             #
#======================== EDIT THE FOLLOWING SECTION =========================#
#                                                                             #
###############################################################################

sender_email = 'address@email.com'                                              # Sender email address
sender_email_password = 'P@ssword4Emai1'                                        # Sender email address password
recievers = ['address1@email.com', 'address2@email.com', 'address3@email.com']  # List of reciever email addresses
weather_dot_com_first_city_link = "https://weather.com/....."                   # Weather.com link to first city
weather_dot_com_second_city_link = "https://weather.com/....."                  # Weather.com link to second city

path_to_chrome_webdriver = "C:/Path/To/Chrome/Webdriver"                        # User's path to Chrome Webdriver file

xpath_to_temperature = '//*[@id="WxuCurrentConditions-main-b3094163-ef75-4558-8d9a-e35e6b9b1034"]/div/section/div/div[2]/div[1]/div[1]/span'
                                                                                # In the event that Weather.com's design changes, the xpath to temperature must be updated

###############################################################################
#                                                                             #
#=========================== EDIT THE ABOVE SECTION ==========================#
#                                                                             #
###############################################################################

# SETUP FOR WEBDRIVER
options = webdriver.ChromeOptions()

chro = webdriver.Chrome(path_to_chrome_webdriver, chrome_options=options)

# UPDATES WILL BE SENT UNTIL PROGRAM IS TERMINATED
while True:

    # GET TEMPERATURES OF THE TWO CITIES AND COMPARE
    chro.get(weather_dot_com_first_city_link)
    currentTempCA = chro.find_elements_by_xpath(xpath_to_temperature)
    for i in currentTempCA:
        pasadenaTemp = i.text[:2]

    chro.get(weather_dot_com_second_city_link)
    currentTempMI = chro.find_elements_by_xpath(xpath_to_temperature)
    for i in currentTempMI:
        rochesterTemp = i.text[:2]

    tempDifference = int(pasadenaTemp) - int(rochesterTemp)

    # CONSTRUCT SENTENCE FOR MESSAGE
    if (tempDifference > 0):
        warmerOrColder = 'warmer'
    else:
        warmerOrColder = 'colder'

    tempDifStr = "It is currently " + pasadenaTemp + " degrees in Pasadena, CA which is " + str(abs(tempDifference)) + " degrees " + warmerOrColder + " than in Rochester Hills, MI"

    #################################################################
    #   Customize the From, To, and Subject lines below as wanted   #
    #################################################################
    message = """\
From: Brian's Python Bot
To: Brian
Subject: WEATHER BOT UPDATE

%s

-PyBot
""" % (tempDifStr)


    # ATTEMPT TO SEND EMAIL
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender_email, sender_email_password)
        server.sendmail(sender_email, recievers, message)
        server.close()
        print ("Successfully sent")
    # IF EMAIL FAILS TO SEND, PRINT ERROR TO TERMINAL
    except:
      print ("Error: Could not send")

    # WAIT TIME, AND SEND ANOTHER EMAIL
    time.sleep(3600) # Change to set how many milliseconds in between emails

