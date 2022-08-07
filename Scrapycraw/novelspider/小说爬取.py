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
                f.write(content + "\n")
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


if __name__ == '__main__':
    res = find_novel("斗破苍穹")
    novel_list_download(res)
