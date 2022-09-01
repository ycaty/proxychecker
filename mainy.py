import queue
import threading
import time
from random import randint
import requests
from termcolor import colored
from phandler2 import doFileDir

'''
Will read all .txt files located in proxyFolder

Load all proxies found and test them
(saves working ones into data folder)




'''

class proxy_checker():
    def __init__(self):
        self.thread_stack = []
        self.q = queue.Queue()
        self.total_threads = 15
        self.test_X_per_thread = 50
        self.my_ip = "YOUR IP HERE"# "200.85.183.99"

        if not "." in self.my_ip:
            print ("Plz set self.my_ip variable..exiting")
            time.sleep(10)
            exit(17)

    def check_callback(self,html, myip):
        if "#n8tv" in html:
            if not myip in html:
                return True
        return False

    def proxySplix(self,proxy):
        splix = proxy.split(':')
        hax_proxy = {'https': 'http://' + splix[0] + ':' + splix[1],
                     'http': 'http://' + splix[0] + ':' + splix[1]
                     }

        return hax_proxy

    def rng_color(self):
        colors = ['grey', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
        rng = randint(0, len(colors) - 1)
        return colors[rng]

    def thready(self,tdata,q):
        ret = {"hit":0,"alive":[],"dead":[]}

        #print ('Hi from thready =>',tdata[0])

        for raw_proxy in tdata:
            #print("Testing proxy => ", raw_proxy)

            try:
                pdata = self.proxySplix(raw_proxy)
                s = requests.Session()
                s.proxies = pdata
                r = s.get('https://jesuit1771.pythonanywhere.com', timeout=3)
                html = (r.text.split("<!DOCTYPE html>")[0])
                check = self.check_callback(html, self.my_ip)
                if check:
                    color = self.rng_color()
                    str_  = "working=> " + raw_proxy
                    print(colored(str_, color))

                    ret['alive'].append(raw_proxy)
                else:
                    str_ = "dead=> "+ raw_proxy
                    print(colored(str_, "red"))
                    ret['dead'].append(raw_proxy)
            except Exception as e:
                #print(e)
                str_ = "dead=> " + raw_proxy
                print(colored(str_, "red"))
                ret['dead'].append(raw_proxy)
            ret['hit']+=1

        q.put(ret)
        time.sleep(2)
        return 1





    def loopy(self):
        'main loop function'

        hit = 0
        alive = 0
        dead = 0

        death = 0
        fTool = doFileDir()
        pstubs = fTool.genStubs()

        #total = (len(pstubs))
        print ("total loaded => ", len(pstubs))


        while True:
            if len(self.thread_stack) < self.total_threads and not death:
                tdata = fTool.fetch_x(self.test_X_per_thread)
                if not tdata:
                    death+=1
                    print ('DEATH += 1')
                else:
                    t = threading.Thread(target=self.thready,args=[tdata,self.q])
                    t.start()
                    self.thread_stack.append(t)
            else:

                print ("TOTAL_+_STATS ^_^ alive=> ",alive, " | hit => ",hit," dead => ",dead)
                time.sleep(10)



            retData = []
            temp = []

            for thread in self.thread_stack:
                boo = thread.is_alive()
                if boo:
                    temp.append(thread)
                #print ("this is boo => ", boo)
            if len(temp) != len(self.thread_stack):
                while True:
                    try:

                        retData = self.q.get_nowait()
                        if not retData:
                            print ("no ret data breaki")
                            break
                        #print ("ret data => ", retData)
                        #print ("type ret",type(retData))
                        alive+=len(retData['alive'])
                        dead+=len(retData['dead'])
                        hit+=retData['hit']
                        if retData['alive']:
                            fTool.write_loot(retData['alive'])
                            fTool.writeBurnt(retData['alive'])
                        if retData['dead']:
                            fTool.writeBurnt(retData['dead'])


                    except Exception as e:
                        #print (e)
                        break

            self.thread_stack = temp
            print (len(self.thread_stack))
            if not self.thread_stack and death:
                print ("no proxies left exiting!")
                break
            if death:
                print ("death True")
                time.sleep(10)

        fTool.flush_loot()


pchecker = proxy_checker()
pchecker.loopy()




