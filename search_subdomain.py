__author__="laker"
import gevent
from gevent import monkey;monkey.patch_all()
import optparse,requests,re,sys


headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
results = []
page_num = 0
ack = 0
alive_list = []

def baidu(url):
    try:
        global results
        #https://www.baidu.com/s?wd=swust.edu.cn&pn=10
        res = requests.get(url,headers=headers,timeout=5).text
        #print (res)
        re_ = re.compile(r'style="text-decoration:none;">(.*?)<b>.*?</b>')
        res = re_.findall(res)
        #print(res)
        results.extend(res)
    except Exception as e:
        pass


#线程启动函数
def bing(url):
    try:
        global results
        # https://cn.bing.com/search?q=swust.edu.cn&first=%d
        res = requests.get(url, headers=headers,timeout=5).text
        #print (res)
        re_ = re.compile(r'<cite>(.*?)<strong>.*?</strong></cite>')
        res = re_.findall(res)
        #print(res)
        results.extend(res)
    except Exception as e:
        pass


def _360(url):
    try:
        global results
        # https://cn.bing.com/search?q=swust.edu.cn&first=%d
        res = requests.get(url, headers=headers,timeout=5).text
        re_ = re.compile(r'<cite>(.*?)<b>.*?</b>>')
        res = re_.findall (res)
        #print (res)
        results.extend (res)
    except Exception as e:
        pass


def run(domain):
    global page_num
    gevent_list = []
    for i in range(0, 75):
        url = 'https://www.baidu.com/s?wd=%s&pn=%d' % (domain, i*10)
        g = gevent.spawn(baidu, url)
        gevent_list.append(g)
    print('baidu')
    for i in range(0, 30):
        url = 'https://cn.bing.com/search?q=%s&first=%d' % (domain, i * 10)
        g = gevent.spawn(bing, url)
        gevent_list.append(g)
    print ('bing')
    for i in range(0, 65):
        url = 'https://www.so.com/s?q=%s&pn=%d' % (domain, i)
        g = gevent.spawn(_360, url)
        gevent_list.append(g)
    print('360')
    gevent.joinall(gevent_list)


def main():
    #定义接受的参数
    opt = optparse.OptionParser()
    opt.add_option('--domain', action='store', dest="domain", type="string", help="父域名！")
    (options, args) = opt.parse_args()
    # if (len(sys.argv) < 2):
    #     print('[+] e.g:python search_subdomain.py baidu.com')
    #     sys.exit()
    options.domain = 'baidu.com'
    run(options.domain)
    with open("%s.txt" % options.domain, "w+") as file:
        print('file')
        print(results)
        for i in results:
            url = i + options.domain
            url = url.replace('http://','').replace('https://','')
            file.write(url + "\n")
    print("[+] 任务已经完成！\n[+] 结果已经保存在当前目录下的域名.txt了。")


if __name__ == '__main__':
    main()