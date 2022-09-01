# proxychecker
Simple to use proxy checker written in python 3.8


checks/loads proxyFolder for all .txt files containing proxies format is (ip:port)
next tests each proxy using this url https://jesuit1771.pythonanywhere.com
(Simple flask relay server i have setup that displays ip addr)

Saves all working proxies into the data/ folder
Saves all burnt proxies into input_files/burnt.txt
On script exit will read all files in data/ and save proxies to loot/working.txt

note:
>(Script doesn't delete files in data/ folder)




Requires termcolor

>pip install termcolor 

Must set self.my_ip variable to your ip (script checks https://jesuit1771.pythonanywhere.com to see if your local ip is NOT within the html)
