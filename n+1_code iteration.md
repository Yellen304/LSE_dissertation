## 3_Get location data
**version3.1.0**
```Python
# 逻辑是先用selenium和soup得到网页，用crawl获取网页内容，parse解析需要的部分，main进行循环

# import 需要用到的库和函数
from bs4 import BeautifulSoup
import time
from selenium import webdriver

# selenium 函数读取网页
    # 定义函数
def city_geographic_selenium(url:str):
    # 打开浏览器（需要定义使用哪个浏览器的类）
    driver=webdriver.Edge()
    driver.get(url)
    # 网页停留五秒
    time.sleep(2)
    # 获取源代码
    page_source=driver.page_source
    # 保存到soup里
    soup=BeautifulSoup(page_source,'html.parser')
    #################################需要关闭浏览器
    driver.quit()
    return soup
# crawl 函数处理文件（此处是保存）
def crawl(website:str="https://blog.csdn.net/esa72ya/article/details/114642127")->float:
    # 通过上一个code block得到了源代码
    soup=city_geographic_selenium(website)
    # 把源代码保存到txt文件中（分成两步）
        ##################################把源代码变成字符串
    raw=str(soup.contents)
        ##################################生成文件
    ## with open(website[website.index('-')+1:]+".txt",'w',encoding='utf-8')as f:
        ##################################把字符串写进文件里
        ## f.write(raw)
    ######################################################################################31行代码出错，下面是chatgpt给改的策略
    file_name = website.split('/')[-1] + ".txt"
    # 把字符串写进文件里
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(raw)

    return 0
# parse 函数解析文件得到想要的内容
def parse(fileName:str)->float:
    # 调用txt文件
    ###############################################这里太复杂了，没看懂
    with open(fileName,'r',encoding='utf-8') as f:
        raw=f.read()
    #############################使用if函数让循环可以跑
    if '汕头' not in raw:
            return -1
    else:
    # 对文件内容进行解析
        # 找到想要的内容“汕头”，只留下汕头到字符串结尾
        raw=raw[raw.index("汕头"):]
        # 找到第一个tr，留下汕头到tr
        raw=raw[:raw.index("</tr>")]
        # 通过td把结果分割开
        raw=raw.split('</td>') 
        # 需要第二块和第三块的内容
        raw=raw[1]
        # 从>开始的字符串
        raw=raw[raw.index('>')+1:] 
        # 返回浮点数
        return float(raw)
if __name__=='__main__':
    answer=""  # 初始化一个空字符来保存结果

### 猜想导出结果的代码是
# longitude=crawl("https://blog.csdn.net/esa72ya/article/details/114642127")
# longitude=parse(str(1)+".txt")
# print("%03d %.2f"%(1,longitude))

#####################################################################ChatGPT给出的结果
crawl("https://blog.csdn.net/esa72ya/article/details/114642127")
longitude = parse("114642127.txt")
if longitude != -1:
        print("%03d %.2f" % (1, longitude))
else:
        print("Failed to parse the longitude")
```

```Python
现在达成的目标：返回了一个值
需要改进的部分（ver3.1.1）：
- crawl部分没太明白逻辑
- 识别两部分的数据：经度和纬度
- 得到的数据是一个范围，因此不是float，如何打印这类文件
- 如何导入到csv文件中
```
**version3.1.1**
```Python
# 逻辑是先用selenium和soup得到网页，用crawl获取网页内容，parse解析需要的部分，main进行循环

# import 需要用到的库和函数
from bs4 import BeautifulSoup
import time
from selenium import webdriver

# selenium 函数读取网页 （输入url，提到driver里，提到page.source里，提到soup里，最终返回的是一个方便解析的解析树版本）
    # 定义函数
def city_geographic_selenium(url:str):
    # 打开浏览器（需要定义使用哪个浏览器的类）
    driver=webdriver.Edge()
    driver.get(url)
    # 网页停留五秒
    time.sleep(2)
    # 获取源代码
    page_source=driver.page_source
    # 保存到soup里
    soup=BeautifulSoup(page_source,'html.parser')
    # 需要关闭浏览器
    driver.quit()
    return soup
# crawl 函数处理文件（此处是保存）(输入的是website，然后套用上一个block得到了soup，提到raw里，创建文件名filename，通过`f`把raw的内容提到filename里，)
def crawl(website:str="https://blog.csdn.net/esa72ya/article/details/114642127")->float:
    # 通过上一个code block得到了源代码
    soup=city_geographic_selenium(website)
    # 把源代码保存到txt文件中（分成两步）
        ##把源代码变成字符串，使用soup里的contents这个属性
    raw=str(soup.contents)
    # website.split('/'): 将 website 字符串按照 / 进行分割，返回一个列表。[-1]: 取分割后列表的最后一个元素，即 website 字符串中最后一个 / 后面的部分，通常是文件名或资源名
    file_name = website.split('/')[-1] + ".txt"
    # 把字符串写进文件里：open(file_name, 'w', encoding='utf-8'): 打开一个文件 file_name，以写入模式 ('w'，即写入新文件或覆盖已有文件) 打开，指定编码为 UTF-8。讲打开的文件对象赋值给变量f，关闭文件，将变量raw的内容写入f中
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(raw)

    return 0
# parse 函数解析文件得到想要的内容（经度） （输入的是filename，提到raw里，开始进行匹配，匹配成功的话返回希望找到的数据raw）
def parse(fileName:str)->str:
    # 调用txt文件
    # 用只读模式打开文件，赋值给变量f，读取全部内容储存到变量raw中
    with open(fileName,'r',encoding='utf-8') as f:
        # 此处的read（）里不能有东西，
        raw=f.read()
    # 使用if函数让循环可以跑
    if '汕头' not in raw:
            return -1
    else:
    # 对文件内容进行解析
        # 找到想要的内容“汕头”，只留下汕头到字符串结尾
        raw=raw[raw.index("汕头"):]
        # 找到第一个tr，留下汕头到tr
        raw=raw[:raw.index("</tr>")]
        # 通过td把结果分割开
        raw=raw.split('</td>') 
        # 需要第二块的内容
        raw=raw[1]
        # 从>开始的字符串
        raw=raw[raw.index('>')+1:] 
        # 返回浮点数
        return str(raw)
# 用parse读取纬度
def parse2(fileName:str)->str:
    # 调用txt文件
    # 用只读模式打开文件，赋值给变量f，读取全部内容储存到变量raw中
    with open(fileName,'r',encoding='utf-8') as f:
        # 此处的read（）里不能有东西，
        war=f.read()
    # 使用if函数让循环可以跑
    if '汕头' not in war:
            return -1
    else:
    # 对文件内容进行解析
        # 找到想要的内容“汕头”，只留下汕头到字符串结尾
        war=war[war.index("汕头"):]
        # 找到第一个tr，留下汕头到tr
        war=war[:war.index("</tr>")]
        # 通过td把结果分割开
        war=war.split('</td>') 
        # 需要第三块的内容
        war=war[2]
        # 从>开始的字符串
        war=war[war.index('>')+1:] 
        # 返回浮点数
        return str(war)


if __name__=='__main__':
    answer=""  # 初始化一个空字符来保存结果

### 猜想导出结果的代码是
# longitude=crawl("https://blog.csdn.net/esa72ya/article/details/114642127")
# longitude=parse(str(1)+".txt")
# print("%03d %.2f"%(1,longitude))
### 

#####################################################################ChatGPT给出的结果
# crawl输入一个网站，经过了selenium那个block得到soup然后存起来，再用parse和parse2找到想要的结果（一个是raw，一个是war）
crawl("https://blog.csdn.net/esa72ya/article/details/114642127")
longitude = parse("114642127.txt")
latitude = parse2("114642127.txt")
answer_long=""
answer_lat=""
if longitude != "-1":
        print("Longitude:%s" % longitude)
        answer_long += "%d,%s\n" % (1,longitude)
        with open('data_1.csv','a')as f:
         f.write(answer_long)
else:
        print("Failed to parse the longitude")
       

if longitude != "-1":
        print("Latitude:%s" % latitude)
        answer_lat += "%d,%s\n" % (1,latitude)
        with open('data_1.csv','a')as f:
            f.write(answer_lat)
else:
        print("Failed to parse the longitude")
        
```



