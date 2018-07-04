import requests
import time
from bs4 import BeautifulSoup

class XBApi():
    
    def __init__(self):
        self.headers = {}
        self.loadheaders()

    def loadheaders(self):
        '''
            导入headers
        '''
        with open("./headers.txt") as headers:
            line = headers.readline().strip()
            while line:
                key = line.split(":")[0]
                self.headers[key] = line[len(key)+1:].strip()
                line = headers.readline().strip()            

    def chat(self, input_strs):
        '''
            args (str):   
                input_strs  问题  
            return (dict):  
                status      状态  
                text        内容        
        '''
        if not self.headers:
            return self.dicts("error", "请打开浏览器 复制并将headers放入headers.txt中")
        data = {
            'location':'msgdialog',
            'module':'msgissue',
            'style_id':1,
            'text':input_strs,
            'uid':5175429989,
            'tovfids':'',
            'fids':'',
            'el':'[object HTMLDivElement]',
            '_t':0,
        }
        
        try:
            url = 'https://weibo.com/aj/message/add?ajwvr=6'
            page = requests.post(url, data=data, headers=self.headers)
            self.savePage(page.text, "./tmp/postpage.txt")
            if page.json()['code'] == '100000':
                code, text, res_type = self.loop(input_strs)
                return self.dicts(code, res_type, text)
            else:
                return self.dicts("500", "failed", page.json()['msg'])
        except Exception as e:
            return self.dicts("500", "error", e)
    
    def dicts(self, status, res_type, text):
        return {"status":status, "type":res_type, "text":text}

    def loop(self, input_strs):
        times = 1
        while times <= 20:
            times += 1
            response = requests.get("https://weibo.com/aj/message/getbyid?ajwvr=6&mid=4258117048671773&uid=5175429989&count=1&_t=0" , headers={"Cookie":self.headers["Cookie"]})
            self.savePage(response.text, "./tmp/response.txt")
            soup = BeautifulSoup(response.json()['data']['html'], "lxml")           
            text = soup.find("p", class_='page')
            if text:
                if text.text == input_strs:
                    time.sleep(0.3)
                    continue
            return 200, text.text, "text"
        text = "错误： 已达到最大重试次数"
        return 500, text, "failed"
            
    def savePage(self, text, file):
        with open(file, "w") as f:
            f.write(text)
