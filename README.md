#用微博抓取微软小冰的回复

1. 安装依赖包，需要python3.6
```
pip install requests
pip install bs4
pip install lxml
```
2. 打开微博微软小冰的界面，手动输入一个问题（之前需要领养），按 F12，打开调试窗口，copy Request Headers的到headers.txt
![image](https://github.com/fredfeng0326/XiaoBingWb/blob/master/pc.png)
3. 运行test.py 改变自己需要的问题
