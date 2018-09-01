# -*- coding:utf-8 -*-
import gevent
from gevent import monkey;monkey.patch_all()
import requests
import time
import re
start_time = time.time()
domain = ''
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
results = []



def define_rex(domain):
    baidu_rex.append(re.compile(r'style="text-decoration:none;">(.*?)' + domain + '(?:\w+){0-1}/&nbsp;</a>'))
    baidu_rex.append(re.compile(r'style="text-decoration:none;">(.*?)<b>' + domain + '</b>/&nbsp;</a>'))
    baidu_rex.append(re.compile(r'style="text-decoration:none;">(.*?)' + domain + '/&nbsp;'))

    bing_rex.append(re.compile(r'<cite>(.*?)<strong>.*?</strong></cite>'))
    bing_rex.append(re.compile(r'<a href=".*?://(.*?)' + domain + '/"'))

    _360_rex.append(re.compile(r'<cite>(.*?)<b>.*?</b>>'))
    _360_rex.append(re.compile(r'<cite>(.*?)' + domain + '</cite>'))
    _360_rex.append(re.compile(r'data-url=".*?://(.*?)' + domain + '.*?"'))


def baidu(url):
    try:
        global results
        response = requests.get(url,headers=headers,timeout=5).text
        res = re.findall(r'style="text-decoration:none;">(.*?)' + domain , response)
        res.extend(re.findall(r'style="text-decoration:none;">(.*?)<b>' + domain, response))
        res.extend(re.findall(r'style="text-decoration:none;">(.*?)' + domain, response))
        results.extend(res)
        print(url,'共获得%d个子域名'%len(res))
    except Exception as e:
        print('baidu,url:',url,e)


def bing(url):
    try:
        global results
        response = requests.get(url, headers=headers, timeout=5).text
        res = re.findall(r'<cite>(.*?)<strong>.*?</strong></cite>', response)
        res.extend(re.findall(r'<a href=".*?://(.*?)' + domain, response))
        results.extend(res)
        print(url, '共获得%d个子域名' % len (res))
    except Exception as e:
        print('bing,url:',url, e)
        pass


def _360(url):
    try:
        global results
        response = requests.get(url, headers=headers, timeout=5).text
        res = re.findall (r'<cite>(.*?)<b>.*?</b>', response)
        res.extend (re.findall (r'<cite>(.*?)' + domain, response))
        res.extend (re.findall (r'data-url=".*?://(.*?)' + domain, response))
        results.extend(res)
        print(url, '共获得%d个子域名' % len (res))
    except Exception as e:
        print('360,url:', url, e)


def spawn(domain):
    gevent_list = []
    for i in range(0, 30):
        url = 'https://www.baidu.com/s?wd=site:%s&pn=%d' % (domain, i*10)
        g = gevent.spawn(baidu, url)
        gevent_list.append(g)
    for i in range(0, 30):
        url = 'https://cn.bing.com/search?q=site:%s&first=%d' % (domain, i * 10)
        g = gevent.spawn(bing, url)
        gevent_list.append(g)
    # for i in range(0, 30):
    #     url = 'https://www.so.com/s?q=site:%s&pn=%d' % (domain, i)
    #     g = gevent.spawn(_360, url)
    #     gevent_list.append(g)
    gevent.joinall(gevent_list)
    gevent_list = []
    for i in range(30, 75):
        url = 'https://www.baidu.com/s?wd=site:%s&pn=%d' % (domain, i*10)
        g = gevent.spawn(baidu, url)
        gevent_list.append(g)
    # for i in range(30, 65):
    #     url = 'https://www.so.com/s?q=site:%s&pn=%d' % (domain, i)
    #     g = gevent.spawn(_360, url)
    #     gevent_list.append(g)
    gevent.joinall(gevent_list)


def main(one):
    global domain
    domain = one
    spawn(domain)
    all = []
    for i in results:
        i = i.replace('http://', '').replace('https://', '').strip()
        if len(i) > 9:
            continue
        i = i + domain
        if i not in all:
            all.append(i)
    end_time = time.time()
    print('[+]搜集到',len(all),'个%s的子域名'%domain,'耗时：%r秒'%(end_time-start_time))
    return all

if __name__ == '__main__':
    with open('domains.txt','r') as f:
        for i in f.readlines():
            i = i.replace('http://','').replace('https://','').strip()
            all = main(i)
            print('[+]  -->本次获取的domain：%s,获得的subdomain有：'%i,all)
            print('[+]        -->为其添加awvs任务')
            # for i in all:
            #     try:
            #         requests.get(url='http://127.0.0.1:9999/awvs/%s' % i)
            #     except Exception as e:
            #         print(e)
            results = []
            start_time = time.time()