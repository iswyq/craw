import urllib.request
import urllib.error
import urllib.parse
import http.cookiejar

url = ""


class Test:
    pass


def craw01_urllib():
    """
        urllib库的基本使用
        request：
            urlopen:返回一个HTTPResponse对象
                url:直接访问指定url
                timeout:设置超时
            urlretrieve:直接将指定地址的内容进行保存
                url:
                filename:
            quote：进行编码，主要用于特殊字符和汉字等
            uquote:进行解码

    :return:
    """
    file = urllib.request.urlopen("https://www.baidu.com")
    # print(file)
    # read方法通过继承得来
    data = file.read()
    # io.BufferedWriter
    fhandle = open("./pages/baidu.html", "wb")
    fhandle.write(data)
    # print(data)


def craw01_urllib_headers():
    """
        增加header
        1.使用build_opener实现
            为opener对象的属性addheader赋值
        2.使用add_header()实现
            通过request对象
                add_header
    :return:
    """
    # 使用方法一
    url = "https://www.baidu.com"
    headers = ()
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    data = opener.open(url).read()
    # 使用方法二
    req = urllib.request.Request(url)
    req.add_header("")
    data1 = urllib.request.urlopen(req).read()


def craw01_urllib_post():
    """
    进行post方式发送请求
        1.使用parse下的urlencode进行编码
        2.编码完成以后，构建Request对象
        3.使用urlopen发送请求
    :return:
    """
    url = "https://www.baidu.com"
    # 待发送的数据进行编码
    postdata = urllib.parse.urlencode({
        "username": "",
        "password": ""
    }).encode("utf-8")
    req = urllib.request.Request(url, postdata)
    data = urllib.request.urlopen(req).read()


def craw01_urllib_proxy():
    """
    增加代理ip

    :return:
    """
    proxy_addr = "127.0.0.1:8080"
    url = "https://www.baidu.com"
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    # 根据传入的handler创建一个opener
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    # 将opener作为全局对象
    urllib.request.install_opener(opener)
    # urlopen通过全局opener已经得到一个合适的opener
    data = urllib.request.urlopen(url).read()


def craw01_urllib_debuglog():
    """
    显示debug信息

    :return:
    """
    # 将http和https的的debug都开启
    httphd = urllib.request.HTTPHandler(debuglevel=1)
    httpshd = urllib.request.HTTPSHandler(debuglevel=1)
    opener = urllib.request.build_opener(httphd, httpshd)
    # 将opener作为全局的opener
    urllib.request.install_opener(opener)
    url = "https://www.baidu.com"
    data = urllib.request.urlopen(url).read()


def craw01_urllib_httperror_and_urlerror():
    """
    使用httpError和urlError处理程序错误
        urlError是httpError的父类
        urlError：
            reason：
        httpError：
            code：错误码
    :return:
    """
    url = "https://www.baidu.com"
    try:
        urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


if __name__ == '__main__':
    craw01_urllib()
