import time
from datetime import datetime as d

temp_host="hosts"
real_host="C:\Windows\System32\drivers\etc"
sites=["www.buzzfeed.com","www.yahoo.com","www.codeacademy.com"]
redir="127.0.0.1"

while True:
    if 10<=d.now().hour<13:
        print("adding")
        with open(real_host,'r+') as file:
            cont=file.read()
            for site in sites:
                if site not in cont:
                    file.write(redir+" "+site+"\n")
        time.sleep(3600)
    else:
        #remove sites
        with open(real_host,'r+') as file:
            print("deleting")
            lines=file.readlines()
            file.seek(0)
            for l in lines:
                #w=True
                #for s in sites:
                    #if s in l:
                    #    w=False
                    #    break
                #if w:
                if not any(s in l for s in sites):
                    file.write(l)
            file.truncate()
        time.sleep(3600)
