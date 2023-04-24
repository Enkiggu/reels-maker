import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from time import sleep
import os
import requests
import pyautogui
import pickle
from pinterestVideoDownload import pinterestVideoDownloader
from pinToReels import pinToReels
import datetime

def pinterestVideo(query,scrollNum,sleepTime,videoTime):
    pinterestVideoUrl = 'https://tr.pinterest.com/search/videos/?q={}'.format(query) + "&rs=filter"

    with open("pinterest_cookies.pkl", "rb") as f:
        cookies = pickle.load(f)
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--auto-open-devtools-for-tabs")
    options.add_argument("--disable-notifications")
    driver = uc.Chrome(options=options)
    driver.get("https://tr.pinterest.com")
    driver.maximize_window()
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    driver.get(pinterestVideoUrl)

    sleep(3)

    # Scroll down for make sure
    for i in range(1, scrollNum):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(sleepTime)

    driver.execute_script("document.body.style.zoom='25%'")
    sleep(3)
    pyautogui.moveTo(1127, 358,duration=1)
    pyautogui.mouseDown()
    sleep(1)
    pyautogui.moveRel(1200, 358,duration=1)
    pyautogui.mouseUp()
    sleep(10)
    # Find values in html
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs = soup.find_all("div", {"class": "Yl- MIw Hb7"})
    driver.quit()

    print("="*50)
    i = 0
    videoLinks = []
    for div in divs:
        try:
            aPin = div.find("a", href=True)
            timeDiv = div.find("div", {"class": "FNs zI7 iyn Hsu"})
            if aPin and aPin["href"].startswith("/pin/") and int(timeDiv.text.split(":")[1]) > videoTime:
                href = aPin["href"]
                videoLinks.append(href)
                print(f"{i}-) https://tr.pinterest.com{href}" ," ==>", timeDiv.text)
                i += 1
        except:
            pass

    print("="*50)
    videoSelection = int(input("Choose a video number: "))
    print(videoLinks[videoSelection])
    pinId = pinterestVideoDownloader(videoLinks[videoSelection])
    return pinId

    #Version 1
    """soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.findAll('a', attrs={'href': lambda href: href and '/pin/' in href})
    times = soup.findAll('div', {'class': 'FNs zI7 iyn Hsu'})
    #driver.quit()
    # Removes duplicate links
    uniqueLinks = []
    for link in links:
        link = link.get('href')
        if link not in uniqueLinks:
            uniqueLinks.append(link)
    # Get time after 0:
    timesText = [time.text.split(":")[1] for time in times]
    # Print out the videos
    print("=" * 50)
    i = 0
    availableLinks = []
    for link, time in zip(uniqueLinks, timesText):
        print("TEST-"+link," ",time)
        if int(time) >= videoTime:
            availableLinks.append(link)
            print(f"{i}-) https://tr.pinterest.com{link}  -->  {time}")
            i += 1
    print("=" * 50)

    videoSelection = int(input("Choose a video number: "))
    pinId = pinterestVideoDownloader(availableLinks[videoSelection])
    return pinId"""

#pinterestVideo("aestetic sky",4,2,21)

def pinterestPin(query,scrollNum,sleepTime,musicName,model,bulkImage=False,reels=True):
    pinterestPinUrl = 'https://www.pinterest.com/search/pins/?q={}'.format(query)
    with open("pinterest_cookies.pkl", "rb") as f:
        cookies = pickle.load(f)
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--auto-open-devtools-for-tabs")
    options.add_argument("--disable-notifications")
    driver = uc.Chrome(options=options)
    driver.get("https://tr.pinterest.com")
    driver.maximize_window()
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    driver.get(pinterestPinUrl)

    sleep(3)

    # Scroll down for make sure
    for i in range(1, scrollNum):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(sleepTime)

    driver.execute_script("document.body.style.zoom='25%'")
    sleep(3)
    pyautogui.moveTo(1127, 358, duration=1)
    pyautogui.mouseDown()
    sleep(1)
    pyautogui.moveRel(1200, 358, duration=1)
    pyautogui.mouseUp()
    sleep(7)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    imageLinkToDownload = []
    i = 0
    if bulkImage:
        for image in soup.findAll('img'):
            try:
                link = image.get('srcset')
                imageName = image.get('srcset').split(', ')[-1].split(' ')[0].strip('https://i.pinimg.com/originals/6a/f7/b2/.jpg')
                url = link.split(', ')[-1].split(' ')[0]
                with open("Pinterest/Images/"+imageName.replace('/','')+".png", "wb") as f:
                    f.write(requests.get(url).content)
            except:
                pass
    else:
        print("="*50)
        for image in soup.findAll('img'):
            try:
                link = image.get('srcset')
                imageName = image.get('srcset').split(', ')[-1].split(' ')[0].strip('https://i.pinimg.com/originals/6a/f7/b2/.jpg')
                url = link.split(', ')[-1].split(' ')[0]
                print(f"{i} -) {url}")
                imageLinkToDownload.append(url)
                i += 1
            except:
                pass
        print("=" * 50)
        imageSelection = str(input("Choose a image number to download: "))
        imageNames = []
        now = datetime.datetime.now()
        for j in imageSelection.split(","):
            if int(j) > len(imageLinkToDownload)-1:
                print("Wrong number!")
            else:
                imageNames.append("Pinterest/Images/" + j + f"{now.hour}{now.minute}{now.year}.png")
                with open("Pinterest/Images/" + j + f"{now.hour}{now.minute}{now.year}.png", "wb") as f:
                    f.write(requests.get(imageLinkToDownload[int(j)]).content)
        print("All images downloaded successfully!")
        if reels:
            pinToReels(imageNames,musicName,model)


#pinterestPin("aestetic sky",4,2,bulkImage=False)
