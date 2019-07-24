# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 10:04:14 2019

@author: DE103806
"""


import pandas
from selenium import webdriver
import time
from datetime import datetime

def main():
    
    Scraper = Scrappo()
    userInput = Scraper.getUserInput()
    Scraper.scrape(userInput)
    
    
    
class Scrappo:
    
    def checkGUI(self, driver_overview):
        try:
            driver_overview.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/a")
            print("Website hasn't changed! :)")
            return False
        except Exception:
            print("Website has changed! :(")
            return True
    
    def getUserInput(self):
         allReports = 'https://battlefieldtracker.com/bfv/profile/origin/'
         
         username = input("Enter your username: ")
         userReports = allReports + username + '/gamereports'
         
         noOfMatches = input("Enter Number of Matches: ")
         
         mode = input("Do you want to start at a specific date? [yes/no] ")
         
         if mode == "yes":
             inputQ = int(input("How many days back? "))-1
         else: 
             inputQ = 0
         return [userReports, noOfMatches, username, inputQ]
     
    def scrape(self, userInput):
        Scrape = Scrappo()
        now = datetime.now()
        
        linktooverview = userInput[0]
        noOfMatches = int(userInput[1])
        userName = userInput[2]
        inputQ = userInput[3]
        
        driver_overview = webdriver.Chrome()
        driver_overview.maximize_window()
        driver_overview.get(linktooverview) #öffnet overview aller matches
        time.sleep(0.5)
        driver_overview.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[2]/a[2]").click() #cookies message
        driver = webdriver.Chrome() #öffnet einen zweiten Driver zum Auslesen von Matches
        driver.maximize_window()
#        driver.get('chrome://settings/')
#        driver.execute_script('chrome.settingsPrivate.setDefaultZoom(0.9);')
        time.sleep(2)
             
        if Scrape.checkGUI(driver_overview):
            driver_overview.quit()
            driver.quit()
            return()
        
        
        
        dfMatchData = Scrape.createDF()
        scrapedMatches = 0
        
        line = 16
        day = 1 + inputQ
        Scrape.scrolldown(driver_overview, inputQ)
        
        while scrapedMatches < noOfMatches:
            
            #print("line vor Aufruf: " + str(line))
            #print("day vor Aufruf: " + str(day))
            
            temp = Scrape.selectNextFSMatch(driver_overview, driver, line, day)
            line = temp[0]
            day = temp[1]
                        
            if Scrape.matchValidation(driver):
                tempList = Scrape.createTempList()
                tempList = Scrape.getGeneralData(driver, tempList)
                position = Scrape.findUserName(driver, userName)
                tempList = Scrape.getWin(driver, tempList, position)
                playerNo = 1
                tempList = Scrape.readUserData(driver, position, playerNo, tempList)
                
                if tempList != None:

                    tempList = Scrape.findOtherPlayers(driver, position, tempList)
                    dfMatchData = Scrape.list2df(tempList, dfMatchData)
                    
                    scrapedMatches = scrapedMatches + 1
                    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    print(str(scrapedMatches) + " of " + str(noOfMatches))
                    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                    
                    Scrape.excelWriter(dfMatchData, userName, now)
                
                else:
                    print("match with position line: " + line+1 + " and day: " + day + " is unreadable")
  
            
            driver_overview.execute_script("window.scrollBy(0, 200)") 
            time.sleep(0.5)
            
        driver.quit()
        driver_overview.quit()
        print(" ^oo^")
        print(" (..)")
        print("()  ()")
        print("()__()")
        
    def createDF(self):
        dfMatchData = pandas.DataFrame(columns = ['date', 'time', 'win', 'durationTotal',
                                                'playerName1', 'timePlayed1', 'score1', 'scorepermin1', 'kd1', 'kills1', 'deaths1', 'killspermin1', 'damage1', 'headshots1', 'shotsTaken1', 'shotsHit1', 'accuracy1', 'revives1', 'revivesReceived1',
                                                'playerName2', 'timePlayed2', 'score2', 'scorepermin2', 'kd2', 'kills2', 'deaths2', 'killspermin2', 'damage2', 'headshots2', 'shotsTaken2', 'shotsHit2', 'accuracy2', 'revives2', 'revivesReceived2',
                                                'playerName3', 'timePlayed3', 'score3', 'scorepermin3', 'kd3', 'kills3', 'deaths3', 'killspermin3', 'damage3', 'headshots3', 'shotsTaken3', 'shotsHit3', 'accuracy3', 'revives3', 'revivesReceived3',
                                                'playerName4', 'timePlayed4', 'score4', 'scorepermin4', 'kd4', 'kills4', 'deaths4', 'killspermin4', 'damage4', 'headshots4', 'shotsTaken4', 'shotsHit4', 'accuracy4', 'revives4', 'revivesReceived4', 
                                                'Number of Players'])        
        return dfMatchData
        
    def list2df(self, tempList, dfMatchData):
        finalMatchData = dfMatchData.append({'date' : tempList[0], 'time' : tempList[1], 'win' : tempList[2], 'durationTotal' : tempList[3],
                                             'playerName1' : tempList[4], 'timePlayed1' : tempList[5], 'score1' : tempList[6], 'scorepermin1' : tempList[7], 'kd1' : tempList[8], 'kills1' : tempList[9], 'deaths1' : tempList[10], 'killspermin1' : tempList[11], 'damage1' : tempList[12], 'headshots1' : tempList[13], 'shotsTaken1' : tempList[14], 'shotsHit1' : tempList[15], 'accuracy1' : tempList[16], 'revives1' : tempList[17], 'revivesReceived1' : tempList[18],
                                             'playerName2' : tempList[19], 'timePlayed2' : tempList[20], 'score2' : tempList[21], 'scorepermin2' : tempList[22], 'kd2' : tempList[23], 'kills2' : tempList[24], 'deaths2' : tempList[25], 'killspermin2' : tempList[26], 'damage2' : tempList[27], 'headshots2' : tempList[28], 'shotsTaken2' : tempList[29], 'shotsHit2' : tempList[30], 'accuracy2' : tempList[31], 'revives2' : tempList[32], 'revivesReceived2' : tempList[33],
                                             'playerName3' : tempList[34], 'timePlayed3' : tempList[35], 'score3' : tempList[36], 'scorepermin3' : tempList[37], 'kd3' : tempList[38], 'kills3' : tempList[39], 'deaths3' : tempList[40], 'killspermin3' : tempList[41], 'damage3' : tempList[42], 'headshots3' : tempList[43], 'shotsTaken3' : tempList[44], 'shotsHit3' : tempList[45], 'accuracy3' : tempList[46], 'revives3' : tempList[47], 'revivesReceived3' : tempList[48],
                                             'playerName4' : tempList[49], 'timePlayed4' : tempList[50], 'score4' : tempList[51], 'scorepermin4' : tempList[52], 'kd4' : tempList[53], 'kills4' : tempList[54], 'deaths4' : tempList[55], 'killspermin4' : tempList[56], 'damage4' : tempList[57], 'headshots4' : tempList[58], 'shotsTaken4' : tempList[59], 'shotsHit4' : tempList[60], 'accuracy4' : tempList[61], 'revives4' : tempList[62], 'revivesReceived4' : tempList[63], 
                                             'Number of Players' : tempList[64]}, ignore_index = True)    
        return finalMatchData
    
    def excelWriter(self, df, username, now):
        # Create a Pandas Excel writer 
        # object using XlsxWriter as the engine. 
        #now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        dt_string = dt_string.replace('/', '').replace(':', '').replace(' ', '_')
        writer = pandas.ExcelWriter(username + '_' + dt_string + '_v1.xlsx', engine = 'xlsxwriter')

        # Write a dataframe to the worksheet. 
        df.to_excel(writer, sheet_name ='FinalMatchData') 
          
        # Close the Pandas Excel writer 
        # object and output the Excel file. 
        writer.save() 
        
    def selectNextFSMatch(self, driver_overview, driver, r, q): 
        r = r+1
        suchRadius = 100
        #matchNo = 0
        
        while r<= suchRadius:
            try:
                matchPath =                              "//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[2]/div[2]/div[" + str(q) + "]/div/div[" + str(r) + "]/a"
                matchtype = driver_overview.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[2]/div[2]/div[" + str(q) + "]/div/div[" + str(r) + "]/div/div[1]/span[1]").text
                                                          
                if matchtype.startswith("Firestorm Squads"):
                    #matchNo= matchNo+1
                    
                    linktomatch = driver_overview.find_element_by_xpath(matchPath).get_attribute('href')
                    
                    #print(linktomatch)
                    
                    driver.get(linktomatch)
                    time.sleep(0.2)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.5)
                    driver.execute_script("window.scrollTo(0, 0);")
                    
                    #driver.execute_script("document.body.style.zoom='50%'")
                    time.sleep(0.5)
#                    
#                    driver_overview.execute_script("window.scrollBy(0, -1080)") 
#                    time.sleep(0.25)
                    
                    try:                       
                        driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[2]/a[2]").click() #cookies
                        time.sleep(0.5)
                        return [r, q]
                    except Exception:
                        time.sleep(0.5)
                    #driver.find_element_by_xpath("/html/body/div[2]/div[1]/div/div/div[2]/a[2]").click()
                    #time.sleep(0.25)
                    
                        return [r, q]
                    
                else:
                    print("kein FSmatch an Stelle " + str(r) )
                    r = r+1
                    
            except Exception:
                q = q+1 
                r = 1
                
    def scrolldown(self, driver_overview, inputQ):
        i = 0
        while i <= inputQ:
            driver_overview.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            i = i+1
        return
    
    def matchValidation(self, driver):
        time.sleep(0.5)
        try:
            duration = driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/aside/header/div/div/div/div[1]/div[2]").text
            duration = duration.split('m')
            if int(duration[0]) > 5:
                print("match valid")
                return True
            else:
                print("match invalid")
                return False
        except Exception:
            print("Match not checkable: Skipping match.")
            return False
            
    def createTempList(self):
        tempList = []
        for l in range (65):
            tempList.append(0)
        
        return tempList   
    
    def getGeneralData(self, driver, tempList):
        #date and time:
        date_and_time = driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/aside/header/div/div/h2/span[2]").text
        a = date_and_time.split('@')
        date = a[0]
        timematch = a[1].strip()
        tempList[0] = date
        tempList[1] = timematch
        
        #duration:
        tempList[3] = driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/aside/header/div/div/div/div[1]/div[2]").text
        
        return tempList
        
    def getWin(self, driver, tempList, position):
        q = position[0]
        try:
            driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[1]/h2/div")
            win = 1
            tempList[2] = win
        except Exception:
            win = 0
            tempList[2] = win
            pass
        
        return tempList
    
        
    def findUserName(self, driver, userName):
        q=1
        r=1
        
        while q <= 10: 
            try:
                if driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[1]/a").text == userName:
                    print(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[1]/a").text)                
                    
                    position = [q,r]
                    return position               
                else:
                    r = r+1 #nächster Spieler im Team für input namen vergleichen
            except Exception: #nächstes Team für input namen vergleichen
                q = q+1
                r = 1
        print("No Player found in match")
        
        
        
    def findOtherPlayers(self, driver, position, matchData):
        Scrape = Scrappo()
        q = position[0]
        r = position[1] 
        offset = 1
        PlayerNumber=1
        while offset <=3:
            try: 
                print(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r+offset) + "]/div[1]/div[1]/a").text)
                PlayerNumber = PlayerNumber + 1 
                tempr = r+offset
                matchData = Scrape.readUserData(driver, [q,tempr], PlayerNumber, matchData)
                if matchData == None:
                    return matchData
                
                offset = offset + 1
            except Exception:
                offset = -1
                while offset >= -4:
                    try:
                        
                        print (driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r+offset) + "]/div[1]/div[1]/a").text)
                        PlayerNumber = PlayerNumber + 1
                        tempr = r+offset
                        matchData = Scrape.readUserData(driver, [q,tempr], PlayerNumber, matchData)
                        if matchData == None:
                            return matchData
                    
                        offset = offset - 1
                    except Exception:
                        matchData[64] = PlayerNumber
                        return(matchData)
        matchData[64] = PlayerNumber               
        return matchData
        
    def readUserData(self, driver, position, playerNo, matchData):
        q = position[0]
        r = position[1] 
        #username:
        matchData[4 + (playerNo-1)*15] = driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[1]/a").text
        #time played:
        matchData[5 + (playerNo-1)*15]  = driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[1]/span").text
        #score:
        matchData[6 + (playerNo-1)*15] = int(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[2]/div").text.replace(',', ''))
        #score per min:
        matchData[7 + (playerNo-1)*15] = float(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[3]/div").text.replace(',', ''))
        #kd:
        matchData[8 + (playerNo-1)*15] = float(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[4]/div").text)
        #kills:
        matchData[9 + (playerNo-1)*15] = int(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[5]/div").text)
        #death:
        matchData[10 + (playerNo-1)*15] = int(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[6]/div").text)
        
        try:
            #open drop down menu
            driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[7]/span").click()
            time.sleep(0.2)
                    
        except Exception:
            print("try again")
            driver.get(driver.current_url)
            time.sleep(0.2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, 0);")
            
            try:
                driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[7]/span").click()
            except Exception:
                matchData = None
                return matchData
                
            
            
        
        #killspermin
        matchData[11 + (playerNo-1)*15] = float(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[2]/div[1]/div[2]/div[4]/span[2]").text)
        #damage
        matchData[12 + (playerNo-1)*15] = int(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[2]/div[1]/div[2]/div[5]/span[2]").text.replace(',', ''))
        #headshots
        matchData[13 + (playerNo-1)*15] = int(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[2]/div[1]/div[2]/div[6]/span[2]").text)
        #schots taken
        matchData[14 + (playerNo-1)*15] = int(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[2]/div[1]/div[2]/div[10]/span[2]").text.replace(',', ''))
        #shots hit
        matchData[15 + (playerNo-1)*15] = int(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[2]/div[1]/div[2]/div[11]/span[2]").text.replace(',', ''))
        #accuracy
        matchData[16 + (playerNo-1)*15] = float(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[2]/div[1]/div[2]/div[12]/span[2]").text.strip('%'))
        #revives
        matchData[17 + (playerNo-1)*15] = int(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[2]/div[2]/div[2]/div[2]/span[2]").text)
        #revives received
        matchData[18 + (playerNo-1)*15] = int(driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[2]/div[2]/div[2]/div[3]/span[2]").text)
        
        #close drop down menu
        driver.find_element_by_xpath("//*[@id='app']/div[3]/div[1]/div/main/div[2]/div/div[2]/div[" + str(q) + "]/div[3]/div[" + str(r) + "]/div[1]/div[7]/span").click()
        time.sleep(0.2)

        print(matchData)       
        return matchData
        
if __name__ == "__main__": main()