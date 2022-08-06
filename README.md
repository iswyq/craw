# Python_Craw

Python爬虫相关的项目内容

> 说明：
>
> 1. 这是一个持续更新的内容，在origin分支当中会包含具体编写代码过程中的测试代码；在master分支中是干净直接使用的代码
> 2. 涉及的爬虫内容比较多，自己日常感兴趣的爬虫项目在此更新
>
> 涉及技术点：
>
> 1. requests库发送简单请求
>
>    [requests官网]: https://requests.readthedocs.io/en/latest/	"requests"
>
> 2. 使用Selenium库调用浏览器进行页面访问 
>
>    [Selenium官网]: https://www.selenium.dev/	"Selenium"
>
> 3. 使用re库进行匹配正则表达式
>
> 4. 使用lxml库进行xpath进行HTML文档DOM节点提取
>
>    [lxml官网]: https://lxml.de/
>
> 环境：
>
> 1. requests  2.27.1
> 2. Python   3.7.11
> 3. selenium   4.1.5
> 4. lxml    4.8.0

补充文档：

[requests库官方文档](https://requests.readthedocs.io/en/latest/)

[Selenium官方文档](https://www.selenium.dev/documentation/)

[Re库官方文档](https://docs.python.org/3.7/library/re.html#regular-expression-objects)

[lxml库使用](https://www.w3cschool.cn/lxml/_lxml-3gp23fjt.html)



# 小说爬取内容

### 内容规划
- [x] 纵横小说

#### 纵横小说

- 进度

  - 内容搜索  :white_check_mark:

  - 小说下载  :white_check_mark:
  - master分支更新


- 说明：
  - 能够根据小说查询符合的结果，并对搜索的小说结果进行内容下载。基本完成要求。
  - 存在问题
    - 性能问题。使用Selenium进行内容爬取，打开网页的过程会消耗整个程序运行的大量时间；而且在小说章节较多情况下，会出现浏览器窗口一直闪烁(因为需要一直进行翻页)，干扰其他任务的运行。
    - 在运行过程中，会出现`NoSuchElementException`和`stale element reference`异常提示，该问题的出现主要是因为浏览器页面没有加载完成或运行其他程序，致使当前的打开的浏览器任务被CPU暂停后无法找到对应网页中的元素。

  - 优化方向  :o:
    - 根据小说网站的特点，换用不同的实现方式。如：纵横小说网站的验证要求不高，可以使用request库的方法发送请求，然后对内容通过xpath或正则表达式的方式进行内容提取。这样可以保证程序在后台执行，不干扰其他任务并且将减少程序的等待加载时间。

- 收获
  - xpath相关语法。使用的最多的是通过标签的属性确定具体的标签
  - 正则表达式。在使用Selenium进行小说内容爬取过程中，用到了一定量的正则表达式。做到了对正则表达式本身语法的熟悉以及Python对正则表达式的具体实现。在后续过程中，加大对正则表达式的使用。
  - Selenium。本案例主要是使用Selenium自动化测试模块进行请求发送和数据提取。在使用的过程中，熟悉了其操作流程和使用规范。虽然纵横小说的具体内容并非使用JS渲染而得(使用JS渲染则无法使用请求获得内容，因为requests库没有执行JS的能力)，但这是对问题解决的另一种尝试。
  - 在其他方面的体悟主要是，“行大于言”。虽然只是一个简单的Python爬虫，但是涉及到的内容还是较多；流程逻辑虽不复杂，但是实现的细节问题只要真正去做了才知道。后续多多练习，好好加油:fire::fire::fire:


