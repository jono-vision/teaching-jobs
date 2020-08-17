#! python3
# teaching_jobs.py - sends email/text with supplied text
"""
Created on Sun Jan 19 19:53:33 2020

@author: jonathandown
"""

import time
import pyinputplus
from selenium import webdriver
import os
import ezgmail
from selenium.webdriver.common.keys import Keys

os.chdir('/Users/jonathandown/Google Drive/Coding/Automate Boring Stuff')

recipient = 'EMAIL@gmail.com' #ENTER EMAIL
cellnumber = 'NUMBER@pcs.rogers.com' #Phone number messaging system
mycell = 'NUMBER@msg.telus.com'
locationwebdriver = '/usr/local/bin/geckodriver'

class SchoolBoard:
    board = []
    def __init__(self, name, username, password, loginweb, jobboardweb):
        self.name = name
        self.username = username
        self.password = password
        self.loginweb = loginweb
        self.jobboardweb = jobboardweb
        SchoolBoard.board.append(self)

parkland = SchoolBoard('Parkland',
                       'username_parkland',
                       'password_parkland',
                       'https://ab07.atrieveerp.com/parkland/login.aspx?ReturnUrl=%2fparkland%2fservlet%2fBroker',
                       'https://ab07.atrieveerp.com/parkland/servlet/Broker?env=ads&template=ads.JobShop1.xml')

stalbert = SchoolBoard('St_Albert',
                       'username_stalbert',
                       'password_stalbert',
                       'https://bc09.atrieveerp.com/stalbertpublic/login.aspx?ReturnUrl=%2fstalbertpublic%2fservlet%2fBroker',
                       'https://bc09.atrieveerp.com/stalbertpublic/servlet/Broker?env=ads&template=ads.JobShop1.xml')

blackgold = SchoolBoard('Blackgold',
                        'username_blackgold',
                        'password_blackgold',
                        'https://ab07.atrieveerp.com/blackgold/login.aspx?ReturnUrl=%2fblackgold%2fservlet%2fBroker',
                        'https://ab07.atrieveerp.com/blackgold/servlet/Broker?env=ads&template=ads.JobShop1.xml')

stthomas = SchoolBoard('St_Thomas',
                        'username_stthomas',
                        'password_stthomas',
                        'https://ab02.atrieveerp.com/stthomas/login.aspx?ReturnUrl=%2fstthomas%2fservlet%2fBroker%3fenv%3dads%26template%3dads.JobShop1.xml',
                        'https://ab02.atrieveerp.com/stthomas/servlet/Broker?env=ads&template=ads.JobShop1.xml')

####################################################################

# Designate how long you want the program to run in hours
searchtime = pyinputplus.inputInt('Duration of search in hours: ',max=10)
refresh_interval_min = pyinputplus.inputInt('How often, in minutes, do you want to search for jobs?: ',min=3,max=28) #Refresh Interval

def accountlogin(board):
    browser = webdriver.Firefox(executable_path=locationwebdriver)
    browser.get(board.loginweb)
    userElem = browser.find_element_by_id("ctl00_body_Login1_UserName")
    userElem.send_keys(board.username)
    page = browser.find_element_by_tag_name('html')
    page.send_keys(Keys.END)
    time.sleep(.5)
    passElem = browser.find_element_by_name('ctl00$body$Login1$Password')
    passElem.send_keys(board.password)
    continueElem = browser.find_element_by_name('ctl00$body$Login1$LoginButton')
    continueElem.click()
    browser.get(board.jobboardweb)

    return browser
    

###### CHECKS RESULTS OF EACH ########
import bs4

os.makedirs('job_board',exist_ok=True) #makes job board folder

jobdict = {} # keeps a history log of all jobs that have been seen  
jobsavailable = {}
driver = {}

#Print progress updates to the user
iterations = searchtime*60//refresh_interval_min
quarter = iterations//4 # quarter done
half = quarter*2
threequarter = quarter*3
refresh_int = refresh_interval_min*60
print('\nSearching in Progress...')

# Initial Login
start_time = time.perf_counter()
for board in SchoolBoard.board:
    driver[board.name] = accountlogin(board) #retrieves loaded page
end_time = time.perf_counter()
print('Login took ' + str(round(end_time - start_time)) + ' seconds')

for i in range(iterations):
    jobdict = jobsavailable
    newjobdict={} # Resets to blank
    if i != 0: #if not first run
        time.sleep(refresh_int) #refresh interval time
        if i == quarter:
            print(f'Approxim. 25% Completed Runs at {time.ctime()}')
        elif i == half:
            print(f'Approxim. 50% Completed Runs at {time.ctime()}')
        elif i == threequarter:
            print(f'Approxim. 75% Completed Runs at {time.ctime()}')    
    # Saving webpage to folder
    for board in SchoolBoard.board:
        if i != 0: #if not the first run
            try:
                driver[board.name].refresh() #refresh pages
            except: 
                print(f'Error occurred logging into {board.name} and was removed from search')               
                del SchoolBoard.board
                break
        
        rawcontent = driver[board.name].page_source
        filename = os.path.join('job_board',(board.name+'.html')) # creates file named after school board
        File = open(filename,'w')
        File.write(rawcontent) #writes the content to the file
        File.close()
        
        # opens the file for parsing to extract useful data
        exampleFile = open(filename,'rb')
        Soup = bs4.BeautifulSoup(exampleFile,'html.parser')
            
            #Select content within table
        try:
            rows = Soup.select('tr')
            for row in rows[2:]: #for every row after the first 2 heading rows
                data = row.select('td')
                
                # find the unique ID Code
                id_code = data[0].getText().strip()
                
                # See if ID Code is already in the dictionary
                if id_code not in jobdict.keys():
                    duration = data[6].getText()
                    starttime = duration[:5]
                    endtime = duration[-5:]
                    #New job posting dictionary
                    dur = round((float(endtime[:2])+float(endtime[3:5])/60)-(float(starttime[:2])+float(starttime[3:5])/60),1)
                    if dur >4:
                        start = data[1].getText()
                        end = data[2].getText()
                        subject = data[3].getText()
                        role = data[4].getText()
                        location = data[5].getText()
                        district = board.name
                        newjobdict[id_code] = [start,end,subject,role,location,duration,district,board.jobboardweb]
                        #adds new job to job posting history
                    jobdict[id_code] = ['']
        except:
            pass
        exampleFile.close()
    if newjobdict != {}: # New Job Listing Found
        print(f'New Job Found!')
        message = f''
        cellmessage = f''
        for num in list(newjobdict):
            message = message + f'\nDate: {newjobdict[num][0]} to {newjobdict[num][1]}\nTime: {newjobdict[num][5]}\nSubject: {newjobdict[num][2]}\n{newjobdict[num][4]}\nDistrict: {newjobdict[num][6]}\nJob ID: {num}\nLink: {newjobdict[num][7]}\n'
            cellmessage = cellmessage + f'{newjobdict[num][0]}: {newjobdict[num][5]} at {newjobdict[num][4]}. {newjobdict[num][7]}\n'
        postings = len(list(newjobdict)) 
        if postings>1:
            ezgmail.send(recipient,f'{postings} New Job Listings',message,cc=myemail)
            ezgmail.send(cellnumber,f'{postings} New Jobs',cellmessage)
        else:
            ezgmail.send(recipient,'New Job Listing',message,cc=myemail)
            ezgmail.send(cellnumber,'New Job',cellmessage)
        print(f'Email sent to {recipient}')
    else:
        pass # No new jobs

currenttime = time.ctime()        
print(f'Runs Completed at {currenttime}')
