from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import requests
from lxml import etree
import re


class Novel:
    def __init__(self, name, href, count=0):
        self.name = name
        self.count = count
        self.href = href


def novel_download(name, url, count):
    """
        小说下载
    :param name:小说的名字
    :param url: 小说的阅读地址
    :return:
    """
    driver = webdriver.Chrome()
    driver.get(url)
    start = driver.find_element_by_xpath("/html/body/div[2]/div[5]/div[1]/div[1]/div[1]/div[2]/div[5]/a")
    # 'http://book.zongheng.com/chapter/744186/41101971.html'
    book = start.get_attribute("href")
    # 获取到小说的内容
    driver.get(book)
    time.sleep(0.5)
    with open(name + ".txt", encoding="utf-8", mode="a+") as f:
        for i in range(count):
            try:
                chapter = driver.find_element_by_xpath("//div[@class='title_txtbox']").text
                # 涉及到访问权限，后续章节需要开通VIP才可查看。
                content = driver.find_element_by_xpath("//div[@class='content']").text
                next_page_button = driver.find_element_by_xpath("//div[@class='chap_btnbox']/a[3]")
                f.write(chapter)
                f.write(content+"\n")
                driver.execute_script("arguments[0].click()", next_page_button)
                time.sleep(0.3)
                # 找出新窗口：
                new_window = driver.window_handles[-1]  # '-1'代表打开的最后一个窗口
                # 切换到新窗口：
                driver.switch_to.window(new_window)
                """
                    如何关闭旧窗口
                """
            except NoSuchElementException:
                # 当无法找到下一章按钮时，结束循环
                print(NoSuchElementException.msg)
                break
        f.close()
    print(name, "--下载完成")
    driver.quit()


def novel_list_download(novels):
    for novel in novels:
        novel_download(novel.name, novel.href, novel.count)


def find_novel(name):
    """
        TODO 使用request库进行小说查询

    :param name:
    :return:
    """
    novel = []
    novel_name_list = []
    novel_href_list = []
    novel_chaptercount_list = []
    driver = webdriver.Chrome()
    driver.get("http://betawww.zongheng.com/")
    # 等待页面加载完成
    time.sleep(0.5)
    # 查询结果 这里获得的是单个结果
    search_text = driver.find_element_by_xpath("//form[@id='commSearch']/div/input[@name='keyword']")
    submit_button = driver.find_element_by_xpath("//form[@id='commSearch']/div/input[@type='submit']")
    search_text.send_keys(name)
    driver.execute_script("arguments[0].click()", submit_button)
    # 小说查询结果
    time.sleep(0.5)
    # 找出新窗口：
    new_window = driver.window_handles[-1]  # '-1'代表打开的最后一个窗口
    # 切换到新窗口：
    driver.switch_to.window(new_window)
    # 获得多个结果
    res_names = driver.find_elements_by_xpath("//div[@class='fl se-result-infos']/h2")
    # 小说的名字
    for res_name in res_names:
        novel_name_list.append(res_name.text)
    res_hrefs = driver.find_elements_by_xpath("//div[@class='fl se-result-infos']/h2/a")
    # 小说的阅读链接
    for res_href in res_hrefs:
        # 'http://book.zongheng.com/book/744186.html'
        novel_href_list.append(res_href.get_attribute("href"))
        # 小说的章节
        # 匹配章节的正则
        """
            这里使用正则不方便对url中的第二个book进行替换。因为：
            1.regex的sub方法只能对匹配的项进行替换，可以指定的参数是替换多少次
            2.regex的search方法只能查找返回第一个匹配的项；可以通过首先编译regex获得pattern对象,执行search方法时指定开始位置.
                返回的结果是一个绝对位置。即在整个字符串中的位置。
                for example：
                string："http://book.zongheng.com/book/744186.html"
                re.compile(r'book').search(string,pos=12)
                返回的结果是25,29(即第二个book)所在位置。25是在string当中的绝对位置
            解决思路：
            1.通过在小说页面内容中获取到对应的目录链接
            2.根据小说的页面链接，并进行目录链接组装
        """
        showchapter = "http://book.zongheng.com/showchapter/" + res_href.get_attribute("href").split("/")[-1]
        # request 小说目录
        r = requests.get(showchapter)
        # 网页内容转换为html，使用xpath捕获记录总章节数的标签
        # 共12章
        em_count = etree.HTML(r.text).xpath("/html/body/div[3]/div[2]/div[2]/div/div/em[2]")
        if len(em_count) != 0:
            count_str = em_count[0].text
            count = re.search(r'\d+', count_str)
            novel_chaptercount_list.append(int(count.group()))
        else:
            novel_chaptercount_list.append(0)
            continue
    # 存储小说的列表
    for i in range(len(novel_name_list)):
        novel.append(Novel(novel_name_list[i], novel_href_list[i], count=novel_chaptercount_list[i]))
    driver.quit()
    return novel


def finders():
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    driver = webdriver.Chrome()

    # Navigate to Url
    driver.get("https://www.example.com")

    # Get all the elements available with tag name 'p'
    elements = driver.find_elements(By.TAG_NAME, 'p')

    for e in elements:
        print(e.text)


def mobile_novel_download(url):
    driver = webdriver.Chrome()
    driver.get(url)
    # 等待浏览器页面加载完成
    time.sleep(0.5)
    # 计算原字符串的hash
    origin = ""
    with open(file="content.txt", mode="a+", encoding="utf-8") as f:
        for i in range(15):
            chapter_title = driver.find_element_by_xpath("//div[@class='title']").text
            # 对标题进行处理
            chapter_title = chapter_title[0:len(chapter_title) - 3]
            # 获得hash值不一样，说明章节标题不一样
            if origin != chapter_title:
                origin = chapter_title
                # 针对字符串进行截取[去掉最后三个字符]  第一章   喜鹊报春，好事将近(1)
                f.write(chapter_title + "\n\n")
            """
             TODO 针对每一章的标题进行对比，如果不一样则进行标题的写入
            """
            content = driver.find_element_by_xpath("//div[@class='text']").text
            content_text = content.replace("《\n", "")
            content_text = content_text.replace("那座孤城有个记忆\n", "")
            content_text = content_text.replace("》\n", "")
            content_text = content_text.replace("全本免费看\n", "")
            # 写入内容到文件当中
            f.write(content_text + '\n\n')
            # 翻页
            next_page = driver.find_element_by_xpath("//div[@class='navigator']/div[3]")
            driver.execute_script('arguments[0].click()', next_page)
        f.close()
    driver.quit()


def novel_zongheng():
    driver = webdriver.Chrome()
    driver.get("https://m.zongheng.com/h5/chapter?bookid=1194663&cid=67802533&fpage=36&fmodule=23&_st=33_308-1_1194663")
    body = driver.find_element(by=By.CLASS_NAME, value="body")
    with open(file="content.txt", mode="a", encoding="utf-8") as f:
        chapter_title = body.find_element_by_xpath("./div[@class='title']")
        # 针对元素隐藏的 https://blog.csdn.net/qq_22200671/article/details/108646469
        # str1 = chapter_title.get_attribute("innerText")
        time.sleep(0.5)
        f.write(chapter_title.text + "\n")
        # 使用的是异步请求，只需要在第一次进入浏览器时等待一定时间即可。
        for i in range(10):
            # xpath 节点排除 https://www.jianshu.com/p/2b525a238371
            text_content = body.find_element_by_xpath("./div[@class='text']")
            # 针对原网页中的div标签进行除去
            str1 = text_content.text.replace("《\n", "")
            str1 = str1.replace("那座孤城有个记忆\n", "")
            str1 = str1.replace("》\n", "")
            str1 = str1.replace("全本免费看\n", "")
            f.write(str1 + "\n\n")
            # 点击下一页 next_page这个按钮存在元素重叠现象
            """
                针对有其他元素遮挡，如进度条等。直接使用JavaScript脚本即可
                https://blog.csdn.net/seattle2009/article/details/124230956
            """
            next_page = driver.find_element_by_xpath("//div[@class='navigator']/div[3]")
            # 翻页
            driver.execute_script('arguments[0].click()', next_page)
        f.close()
    driver.quit()


def test():
    driver = webdriver.Chrome()
    driver.get("http://book.zongheng.com/showchapter/1183681.html")
    time.sleep(0.5)
    a = driver.find_elements_by_xpath("//li[@class='col-4']")
    print(a)
    # title = driver.title
    # search_box = driver.find_element(by=By.ID, value="kw")
    # search_button = driver.find_element(by=By.ID, value="su")
    #
    # # driver.find_element(by=)
    # print(title)
    # search_box.send_keys("Selenium")
    # search_button.click()
    # driver.implicitly_wait(10)
    # print(driver.get_cookies())
    driver.quit()


def baidu_clik():
    driver = webdriver.Chrome()
    driver.get("https://www.baidu.com")
    input_text = driver.find_element_by_xpath("//input[@id='kw']")
    search_button = driver.find_element_by_xpath("//input[@id='su']")
    input_text.send_keys("南京")
    search_button.click()
    hotpot = driver.find_element_by_xpath("//div[@class='toplist1-tr_4kE4D']")
    for e in hotpot:
        print(e.text)
    driver.close()


def test_re():
    """
        需要将http://book.zongheng.com/book/744186.html转换成
            'http://book.zongheng.com/showchapter/744186.html'
    :return:
    """
    pattern = re.compile(r"book")
    content_url = "http://book.zongheng.com/showchapter/744186.html"
    text_url = "https://book.zongheng.com/chapter/744186/41101971.html"
    res = pattern.sub("showchapter", "http://book.zongheng.com/book/744186.html")
    res = re.subn(r'oo', "你好", "http://book.zongheng.com/book/744186.html", 2)
    """
        search方法只能返回第一个匹配的结果，但是可以通过指定开始的位置来进行调整
    """
    res1 = re.search(r'book', "http://book.zongheng.com/book/744186.html")
    res = pattern.search("http://book.zongheng.com/book/744186.html", pos=11)
    print(res)
    print("http://book.zongheng.com/book/744186.html"[25:29])
    '''print(res.group(0))  # 表示匹配的结果
    print(res.span())  # 匹配成功的位置
    print(res.start())  # 匹配的开始位置
    print(res.end())  # 匹配的结束位置
    '''


if __name__ == '__main__':
    # test_re()
    # novel_zongheng()
    # finders()
    # baidu_clik()
    # novel_download("https://m.zongheng.com/h5/chapter?bookid=1194663&cid=67802533&fpage=36&fmodule=23&_st=33_308-1_1194663")
    res = find_novel("斗破苍穹")
    novel_list_download(res)
