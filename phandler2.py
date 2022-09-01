import uuid
import os
from uuid import uuid4
from random import randint
import time
"""

=> loads all proxy files in proxyFolder
=> loads burnt
=> removes all found from burnt.txt
=> generates dict
    => {"ip:port":{"proxy":"ip:port", "tested":0, "alive":0 , "dead":0}
"""

class doFileDir():
    def __init__(self):
        file_array = ['input_files/burnt.txt']
        dir_array = ["proxyFolder/", "proxyFolderBurnt/", "loot", "input_files/", "data/"]
        self.checkDirExist(dir_array)
        self.checkFilesExsist(file_array)

        self.pstubs = {}

    def checkFilesExsist(self,file_array):
        for file in file_array:
            try:
                with open(file,"r") as f:
                    f.close()
            except Exception as e:
                print (e)
                print ("Creating..." , file)
                with open(file,"w") as f:
                    f.close()


    def checkDirExist(self,dir_array):
        for d in dir_array:
            try:
                os.mkdir(d)
            except:
                pass



    def loadBurnt(self):
        with open('input_files/burnt.txt',"r") as f:
            burnt = [x.strip() for x in f.readlines()]
        return burnt

    def writeBurnt(self,proxies):
        with open("input_files/burnt.txt","a") as f:
            for x in proxies:
                f.write(x+"\n")
            f.flush()
            f.close()



    def write_loot(self,proxies):
        print ("ratatata WRITE LOOT UWO")
        #rng = str(randint(0,9000))
        fname = 'data/' + str(uuid.uuid4()) + '.txt'
        print ("rng name => ", fname)
        with open(fname, "w") as f:
            for x in proxies:
                f.write(x + "\n")
            f.flush()
            f.close()

    def flush_loot(self):
        files = os.listdir("data")
        stack = set()
        for file in files:
            with open("data/" + file,"r") as f:
                temp = [x.strip() for x in f.readlines()]
            for x in temp:
                stack.add(x)

        with open("loot/" + "working" + ".txt","w") as f:
            for x in stack:
                f.write(x+"\n")
            f.flush()
            f.close()
        # ("ADD REMOVE FILES FROM DATA FOLDER LATER")

    def loadProxies(self):
        return os.listdir("proxyFolder")

    def display_table(self):
        print (self.pstubs)

    def fetch_x(self,x):
        'returns list of proxies'
        x_stack = []
        for proxy in self.pstubs:
            if not self.pstubs[proxy]['inuse']:
                self.pstubs[proxy]['inuse'] = 1
                x_stack.append(self.pstubs[proxy]['proxy'])
            #print (proxy,self.pstubs[proxy])
            if len(x_stack) >= x:
                break
        return x_stack

    def genStubs(self):
        '''
        Loads all proxies/burnt
        removes all previously burnt proxies

        Creates a dict of proxy stubs
        {
            {"ip:port":{"proxy":"ip:port", "tested":0, "alive":0 , "dead":0},
            {"ip:port":{"proxy":"ip:port", "tested":0, "alive":0 , "dead":0}
        }


        :return:
        '''

        stack = set()
        self.pstubs = {}
        proxy_files = self.loadProxies()
        burnt = self.loadBurnt()
        for file in proxy_files:
            with open("proxyFolder/" +  file,"r") as f:
                proxies = [x.strip() for x in f.readlines()]

            for proxy in proxies:
                if not proxy in burnt:
                    stack.add(proxy)
        for proxy in stack:
            self.pstubs[proxy] = {"proxy":proxy,"inuse":0}

        return self.pstubs









