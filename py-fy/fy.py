# -*- coding: utf-8 -*-
import json 
import win32clipboard as wc  #读取剪切板数据
from pymouse import PyMouse  #获得当前鼠标信息
import tkinter               #自带的GUI库，生成文本框
import time          
import operator
import urllib.request
import urllib.parse
import urllib
import json
import os
import sys
import codecs
import requests


LOGO = '''
                                   .-.                
                                  /    \              
   .-..    ___  ___               | .`. ;   ___  ___  
  /    \  (   )(   )              | |(___) (   )(   ) 
 ' .-,  ;  | |  | |    .------.   | |_      | |  | |  
 | |  . |  | |  | |   (________) (   __)    | |  | |  
 | |  | |  | '  | |               | |       | '  | |  
 | |  | |  '  `-' |               | |       '  `-' |  
 | |  ' |   `.__. |               | |        `.__. |  
 | `-'  '   ___ | |               | |        ___ | |  
 | \__.'   (   )' |              (___)      (   )' |  
 | |        ; `-' '                          ; `-' '  
(___)        .__.'                            .__.'   
'''
currentData='' 
ScriptsPath = os.path.sep.join([sys.base_prefix, "Scripts"])


def transMousePosition(): #PyMouse得到的是2维字符串，但是tkinter生成窗体时需要的是类似（100*100+x+y）的字符串，100*100是窗口大小，xy是坐标点。
    m = PyMouse()
    return "100x100+"+str(m.position()[0])+"+"+str(m.position()[1])
  
def getCopyText(): #获得剪切板数据  
    wc.OpenClipboard()
    copy_text = wc.GetClipboardData()
    wc.CloseClipboard()
    return copy_text

def newCopyData(): #返会是否有新的复制数据
    return currentData == getCopyText()
    
def multi_translate(content):
    '''
    使用有道字典翻译词组、句子
    :param content 待翻译的内容，str类型
    '''
    url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=http://fanyi.youdao.com/' #有道翻译查询入口
    data = {  #表单数据
      'i': content,
      'from': 'AUTO',
      'to': 'AUTO',
      'smartresult': 'dict',
      'client': 'fanyideskweb',
      'doctype': 'json',
      'version': '2.1',
      'keyfrom': 'fanyi.web',
      'action': 'FY_BY_CLICKBUTTION',
      'typoResult': 'false'
     }
    r = requests.post(url, data)
    result = r.json()['translateResult'][0][0]['tgt']                         
    print("%s" % result)         
    return result 


def youdao_translate(content):
    '''
    :param content 待翻译的内容，str类型
    '''
    if " " in content or content.isascii() is False :# 输入为中文或多行时用multi_translate处理
        result = multi_translate(content) 
    else:
        url = 'http://fanyi.youdao.com/openapi.do?keyfrom=huacicha&key=199079426&type=data&doctype=json&version=1.1&q=' + content
        r = requests.get(url)
        data = r.json()
        try:
            print(u'翻译：%s' % data['translation'][0])
            print(u'美式发音：/%s/' % data['basic']['us-phonetic'])
            print(u'英式发音：/%s/' % data['basic']['uk-phonetic'])
            explains = data['basic']['explains']
            print('-' * 25 + u'基本释义' + '-' * 25)
            for i in explains:
                print(u'%s' % i)

            web = data['web']
            print('-' * 25 + u'网络释义' + '-' * 25)
            for i in web:
                print('%s: %s' % (i['key'], ','.join(i['value'])))

            result = "[" + data['basic']['us-phonetic'] + "]  " + data['translation'][0]
        except Exception as e:
            result = multi_translate(content)

    return result


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "-install":
            print("start install py-fy")
            fileName = os.path.basename(sys.argv[0])
            os.system("pyinstaller -F %s" % fileName)
            import shutil
            exeName = fileName.split(".")[0] + ".exe"
            shutil.copyfile(os.sep.join(['dist', exeName]), os.sep.join([ScriptsPath, exeName]))
            print("install py-fy successful!")
        else:
            inputList = sys.argv[1:]
            inputLine = ' '.join(inputList)
            result = youdao_translate(inputLine)
    else:
        print(LOGO)
        currentData = ""
        while 1:
            if currentData != getCopyText():
                currentData = getCopyText()
                inputLine = currentData
                result = youdao_translate(inputLine)
                position=transMousePosition()       # 取得当前鼠标位置
                top = tkinter.Tk()                  # 窗口初始化
                top.wm_attributes('-topmost',1)     # 置顶窗口
                top.geometry(position)              # 指定定位生成指定大小窗口
                text = tkinter.Text()               # 生成文本框部件
                text.insert(1.0, result)            # 插入数据
                text.pack()                         # 将部件打包进窗口
                top.mainloop()                      # 进入消息循环
            time.sleep(1)
       