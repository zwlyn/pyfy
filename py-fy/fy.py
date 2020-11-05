# -*- coding: utf-8 -*-
import urllib #http连接需要用到
import json  #解析网页数据用
import win32clipboard as wc #读取剪切板数据
from pymouse import PyMouse #获得当前鼠标信息
import tkinter         #自带的GUI库，生成文本框
import time          #定时器，减少占用
import operator
import urllib.request
import urllib.parse
import urllib
import json
import os
import sys
import codecs


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

#PyMouse得到的是2维字符串，但是tkinter生成窗体时需要的是类似（100*100+x+y）的字符串，100*100是窗口大小，xy是坐标点。
def transMousePosition():
    m = PyMouse()
    return "100x100+"+str(m.position()[0])+"+"+str(m.position()[1])
#获得剪切板数据    
def getCopyText():
    wc.OpenClipboard()
    copy_text = wc.GetClipboardData()
    wc.CloseClipboard()
    return copy_text
#返会是否有新的复制数据
def newCopyData():
    return currentData == getCopyText()


def multi_translate(content):

    url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=http://fanyi.youdao.com/'
    #有道翻译查询入口
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
    data=urllib.parse.urlencode(data).encode('utf-8')
    #对POST数据进行编码
    response=urllib.request.urlopen(url,data)
    #发出POST请求并获取HTTP响应
    html=response.read().decode('utf-8')
    #获取网页内容，并进行解码解码
    target=json.loads(html)
    #json解析
    print("%s"%target['translateResult'][0][0]['tgt'])
    #输出翻译结果
    return target['translateResult'][0][0]['tgt']


def youdao_translate(content):

    #翻译内容
    if " " in content or content.isascii() is False :
        # 输入为中文或多行时用multi_translate处理
        result = multi_translate(content)
    else:

        url = 'http://fanyi.youdao.com/openapi.do?keyfrom=huacicha&key=199079426&type=data&doctype=json&version=1.1&q=' + content
        data = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
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



def isEnglish(sentence):
    for word in sentence.split(" "):
        if word.encode('utf-8').isalpha() is False:
            return False

    return True



def isValid(inputline, result):
    # one Chinese and one English is valid
    return isEnglish(inputline) ^ isEnglish(result)



# def record_translate(recordFile, inputline, result):
#     # 处理 中文输入和英文输入两种情况
#     English, Chinese = (inputline, result) if isEnglish(inputline) is True else (result, inputline)
#     if isValid(English, Chinese) is True:
#         if os.path.exists(recordFile):
#             with codecs.open(recordFile, 'r', encoding='utf-8') as f:
#                 recordDict = json.loads(f.read())
#                 recordDict.update({English: Chinese})
#                 with codecs.open(recordFile, 'w', encoding='utf-8') as f:
#                     f.write(json.dumps(recordDict, indent=4, ensure_ascii=False)) # ensure_ascii=False 使得中文不是乱码
#         else:
#             recordDict = {}
#             recordDict.update({English: Chinese})
#             with codecs.open(recordFile, 'w', encoding='utf-8') as f:
#                 f.write(json.dumps(recordDict, indent=4, ensure_ascii=False))



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
            # print(result)
            #record_translate(RecordFile, inputLine, result)
    else:
        print(LOGO)
        currentData = ""
        while 1:
            if currentData != getCopyText():
                currentData = getCopyText()
                # print("==========", currentData, "=========")

                # dirname = os.path.dirname(sys.argv[0])
                # RecordFile = os.sep.join([dirname, "record.json"])
                inputLine = currentData
                result = youdao_translate(inputLine)
                # print("=============result: ", result)
                # record_translate(RecordFile, inputLine, result)

                position=transMousePosition()#取得当前鼠标位置
                top = tkinter.Tk()#窗口初始化
                top.wm_attributes('-topmost',1)#置顶窗口
                top.geometry(position)#指定定位生成指定大小窗口
                text = tkinter.Text()#生成文本框部件
                text.insert(1.0, result)#插入数据
                text.pack()#将部件打包进窗口
                top.mainloop()# 进入消息循环
            time.sleep(1)
       