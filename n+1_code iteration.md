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


```Python
现在达成的目标：得到了经纬度数据并导入到CSV中
需要改进的部分（ver3.1.2）
- 把程序和和我的excel文件结合起来。excel里面第一列是城市名称，我需要把这些名称依次读取出来和网站进行匹配，返回经度和维度到第二列和第三列中，改如何写代码
- 把parse1和parse2合并起来
- 根据经度范围中间的波浪号拆分到两列（optional）
- 在excel中计算城市的中心点(optional)
过程中遇到的问题：
- 找不到文件夹：因为xlsx和xls的文件格式不一样
- 没有安装openxyl库
- 中途更换路径
- 缺少xlrd库
```

**version3.1.2**
```Python
# 逻辑是先用selenium和soup得到网页，用crawl获取网页内容，parse解析需要的部分，main进行循环

# import 需要用到的库和函数
import pandas as pd # type: ignore
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
def parse(fileName:str,city:str,index:int)->str:
    # 调用txt文件
    # 用只读模式打开文件，赋值给变量f，读取全部内容储存到变量raw中
    with open(fileName,'r',encoding='utf-8') as f:
        # 此处的read（）里不能有东西，
        raw=f.read()
    # 使用if函数让循环可以跑
    if city not in raw:
            return -1
    ## parse函数合并：使用index来定位第一部分还是第二部分
    else:
    # 对文件内容进行解析
        # 找到想要的内容“汕头”，只留下汕头到字符串结尾
        raw=raw[raw.index(city):]
        # 找到第一个tr，留下汕头到tr
        raw=raw[:raw.index("</tr>")]
        # 通过td把结果分割开
        raw=raw.split('</td>') 
        if len(raw) > index:
            raw = raw[index]
            raw = raw[raw.index('>') + 1:]
            return str(raw)
        else:
            return -1

def update_excel_with_coordinates(excel_file:str='4_city list.xlsx',txt_file = '114642127.txt',output_excel_file:str='cities_with_coordinates.xlsx'):
     # 用pandas读取Excel文件，并将其存储在DataFrame对象“df”中
    df = pd.read_excel(excel_file)
     # 初始化空列表用于储存经纬度信息
    coordinates= []
    # 遍历DataFrame中的每个城市
    for city in df['city_Chinese']:
        longitude = parse(txt_file, city, 1)  # 获取经度
        latitude = parse(txt_file, city, 2)  # 获取纬度
        if longitude != -1 and latitude != -1:
            coordinates.append((longitude, latitude))
        else:
            coordinates.append(("Not Found", "Not Found"))
    df['longitude'] = [coord[0] for coord in coordinates]
    df['latitude'] = [coord[1] for coord in coordinates]
    df.to_excel(output_excel_file, index=False)    
    

# 使用示例

    website = "https://blog.csdn.net/esa72ya/article/details/114642127"
    excel_file = r'C:\Users\Yalin\Desktop\4_city_list.xls'
    output_excel_file = 'cities_with_coordinates.xlsx'
    update_excel_with_coordinates(excel_file, txt_file, output_excel_file)

if __name__ == '__main__':
    excel_file = r'C:\Users\Yalin\Desktop\4_city_list.xls'
    output_excel_file = 'cities_with_coordinates.xlsx'
    txt_file = '114642127.txt'
    update_excel_with_coordinates(excel_file, txt_file, output_excel_file)
    print(f"Updated Excel file saved as {output_excel_file}")
```

```Python
现在达成的目标：得到了EXCEL中每一个城市的经纬度数据
需要改进的部分（ver3.1.3）
- 读取每个城市的经纬度信息嵌入到API读取信息中
- 使用API接到CDS toolbox，输入经纬度信息，返回需要的温度（需要决定什么数据）
- 调用EXCEL文件中的city_english，生成地区的xlsx文件名
- 将一个地区的数据导入到EXCEL文件中
遇到的问题


```
**一个充满错误，自己写的version3.1.3（wrong）版本，看你是否能察觉出来错误**
```Python
# 步骤是：提取出来一个城市经纬度，打开CDS，输入经纬度，需要的温度信息
# toolbox的网址是https://cds.climate.copernicus.eu/toolbox-editor/320203/01-retrieve-data

# 下载该city的数据
# import the CDS Toolbox library
import cdsapi

# 创建一个 CDS API 客户端
c = cdsapi.Client()

def create_city_temperature(geo_excel:str='cities_with_coordinates.xlsx',out_excel:str):
#获取该city的经纬度数据
# 用pandas读取Excel文件，并将其存储在DataFrame对象“df”中
    df = pd.read_excel(geo_excel)

    # 遍历DataFrame中的每个城市
    for city in df['city_Chinese']:
       
        # 发起数据请求
        c.retrieve(
            'reanalysis-era5-single-levels',  # 数据集名称
            {
                'product_type': 'reanalysis',  # 产品类型
                'variable': '2m_temperature',  # 变量名称
                'year': ['2018', '2020'], # 年份
                'month': ['06', '07', '08'], # 月份
                'day': [
                '01', '02', '03', '04', '05', '06',
                '07', '08', '09', '10', '11', '12',
                '13', '14', '15', '16', '17', '18',
                '19', '20', '21', '22', '23', '24',
                '25', '26', '27', '28', '29', '30',
                '31'],  # 日期
                'time': '12:00',  # 时间
                'format': 'netcdf',  # 数据格式
                ## 提取
                'area': [df['north'], df['west'], df['south'], df['east']],  # 地理区域 (北纬, 西经, 南纬, 东经)			

            },

            df['city_eng']+".nc"  # 输出文件名
            print("数据下载完成，文件名为  df['city_eng']+".nc" )
        )
        #把nc文件改为csv文件
        import xarray as xr
        import pandas as pd

        # 使用 xarray 打开 NetCDF 文件
        data = xr.open_dataset(df['city_eng']+".nc")

        # 将 NetCDF 数据转换为 Pandas DataFrame
        # 假设我们只关心温度数据
        temperature_data = data['t2m'].to_dataframe().reset_index()

        # 将 DataFrame 保存为 CSV 文件
        temperature_data.to_csv(df[city_eng]+'.csv', index=False)

        print("数据已保存为 'df[city_eng]+'.csv'')
    return "已完成"

```
```Python
问题在于：
- 缺少必要的导入语句。
- 在读取地理区域的经纬度数据时，应该根据城市动态获取。
- c.retrieve 是一个阻塞操作，应该在一个循环中逐个处理城市的数据请求。
- 缺少正确的文件名格式。
- print 语句位置错误。
- 文件名和列名的引用需要用格式化字符串或字符串拼接
- 后面加入try来调试的原因
- 为什么也没有报错也没有任何显示：因为没有调用函数！！
```
**version3.1.3**
```Python
# 步骤是：提取出来一个城市经纬度，打开CDS，输入经纬度，需要的温度信息
# toolbox的网址是https://cds.climate.copernicus.eu/toolbox-editor/320203/01-retrieve-data

# 下载该city的数据
# import the CDS Toolbox library
import cdsapi
# 用于导成CSV文件
import xarray as xr
import pandas as pd
 # 用于文件夹路径操作
import os 
# 用于文件清理
import glob  

# 创建一个 CDS API 客户端
c = cdsapi.Client()


def create_city_temperature(geo_excel:str='cities_with_coordinates.xlsx'):
#获取该city的经纬度数据
# 用pandas读取Excel文件，并将其存储在DataFrame对象“df”中
    df = pd.read_excel(geo_excel)
    print(f"开始处理 {geo_excel} 文件中的城市数据...")
   
    for i, row in df.iterrows():
        # 先遍历所有需要的信息：
        city_chinese = row['city_Chinese']
        city_eng = row['city_eng']
        longitude=row['longitude']
        latitude=row['latitude']

        

        # 发起数据请求
        c.retrieve(
            'reanalysis-era5-single-levels',  # 数据集名称
            {
                'product_type': 'reanalysis',  # 产品类型
                'variable': '2m_temperature',  # 变量名称
                'year': ['2018', '2020'], # 年份
                'month': ['06', '07', '08'], # 月份
                'day': [str(d).zfill(2) for d in range(1, 32)], # 日期
                'time': '12:00',  # 时间
                'format': 'netcdf',  # 数据格式
                ## 提取
                'area': [latitude,longitude,latitude+0.0001,longitude+0.0001],  # 地理区域 (北纬, 西经, 南纬, 东经)			

            },
            f"{city_eng}.nc"  # 输出文件名
        )
        ## 
        print(f"数据下载完成，文件名为  {city_eng}.nc" )
        #把nc文件改为csv文件

        # 使用 xarray 打开 NetCDF 文件
        data = xr.open_dataset(f"{city_eng}.nc")

        # 将 NetCDF 数据转换为 Pandas DataFrame
        # 假设我们只关心温度数据
        temperature_data = data['t2m'].to_dataframe().reset_index()

        # 将 DataFrame 保存为 CSV 文件
        temperature_data.to_csv(f"{city_eng}.csv", index=False)

        print(f"数据已保存为 {city_eng}.csv")   
    return "已完成"

# 调用函数
create_city_temperature()
```


```Python
现在达成的成就：该代码可以把所要求的所有数据都下载下来了(但因为被网站限流了，所以失败，可以采用解决办法)
下一步：
- 继续探索如何下载到一个单独的文件夹中（optional）
- 想要得到的数据：该样本受访所在月的平均气温和最高气温超过32度的天数，如果能找到日数据就是前七天的平均气温
- 如何把这边的EXCEL数据和STATA的数据进行匹配
遇到的问题：
- 下载到第五个就一直保持queue的状态，正常情况下应该1-5分钟一个：
    - 问题：单个用户单次只能下载四个，解决办法[https://blog.csdn.net/junlong750/article/details/113605759]
    - 解决办法1：把任务拆分成多个小块或多线程处理[https://blog.csdn.net/VictoriaLy/article/details/112912419]
    - 解决办法2：使用selenium函数模拟鼠标在网页直接进行操作（注意：一定要sleep！）
    - 解决办法3：网页手动下载

补救措施
- 一些可能可以使用的数据
    - 需要登陆的数字开放平台提供NOAA数据：https://blog.csdn.net/qq_41325092/article/details/135342604
    - NOAA数据库：https://blog.csdn.net/qq_39855224/article/details/112149945
    - 收费的空气污染数据：https://bbs.pinggu.org/thread-11169689-1-1.html
    - 收费的气温与空气污染数据：https://bbs.pinggu.org/thread-10557572-1-1.html
- 使用VPN修改地址
    - https://vpn.nsspirt-cashf2.com/zh-cn/best-vpns-for-uk/#index_id10

```
**Version3.1.3.(2)**
```Python
# 前一步是在生成的cities_with_corrdinates里生成东西南北和经纬度的数值信息（此步可以用代码完成）
# 还有一步是手动补齐了缺失的信息
# 步骤是：提取出来一个城市经纬度，打开CDS，输入经纬度，需要的温度信息
# toolbox的网址是https://cds.climate.copernicus.eu/toolbox-editor/320203/01-retrieve-data

# 下载该city的数据
# import the CDS Toolbox library
import cdsapi
import time
# 用于导成CSV文件
import xarray as xr
import pandas as pd
 # 用于文件夹路径操作
import os 
# 用于文件清理
import glob  

# 创建一个 CDS API 客户端
c = cdsapi.Client()


def create_city_temperature(geo_excel:str='cities_with_coordinates_1.xlsx'):
#获取该city的经纬度数据
# 用pandas读取Excel文件，并将其存储在DataFrame对象“df”中
    df = pd.read_excel(geo_excel)
    print(f"开始处理 {geo_excel} 文件中的城市数据...")
   
    for i, row in df.iterrows():
        # 先遍历所有需要的信息：
        city_chinese = row['city_Chinese']
        city_eng = row['city_eng']
        longitude=row['longitude']
        latitude=row['latitude']
        # print(i,city_eng,longitude,latitude)
        if os.path.exists(city_eng+'.nc'):
            print(f"下载过了  {city_eng}.nc" )
            continue
        

        # # 发起数据请求
        c.retrieve(
            'reanalysis-era5-single-levels',  # 数据集名称
            {
                'product_type': 'reanalysis',  # 产品类型
                'variable': '2m_temperature',  # 变量名称
                'year': ['2018', '2020'], # 年份
                'month': ['06', '07', '08'], # 月份
                'day': [str(d).zfill(2) for d in range(1, 32)], # 日期
                'time': ['6:00','12:00', '18:00'], # 时间
                'format': 'netcdf',  # 数据格式
                ## 提取
                'area': [latitude,longitude,latitude+0.0001,longitude+0.0001],  # 地理区域 (北纬, 西经, 南纬, 东经)			

            },
            f"{city_eng}.nc"  # 输出文件名
        )
        ## 
        print(f"数据下载完成，文件名为  {city_eng}.nc" )
        
        time.sleep(5)
        #把nc文件改为csv文件

        # # 使用 xarray 打开 NetCDF 文件
        # data = xr.open_dataset(f"{city_eng}.nc")

        # # 将 NetCDF 数据转换为 Pandas DataFrame
        # # 假设我们只关心温度数据
        # temperature_data = data['t2m'].to_dataframe().reset_index()

        # # 将 DataFrame 保存为 CSV 文件
        # temperature_data.to_csv(f"{city_eng}.csv", index=False)

        # print(f"数据已保存为 {city_eng}.csv")   
    return "已完成"

# 调用函数
create_city_temperature()

```

```Python
现在达成的目标：下载了所有城市数据
下一步目标：
- 调用STATA已经清洗过的CHARLS数据库
- 获取每个样本的ID,地址，采访月份和年份
- 对每一个样本找到城市的excel，打开后计算该月份的平均温度和累计高温[平均气温与累计高温：使用早上中午晚上的平均气温作为当日的温度，再计算该星期或该月的平均气温。累积超阈值温度为早中晚任何一个时间超过阈值时间即定义为1]


```
**Version3.1.4**
```Python
#将每个样本与当月平均气温匹配
import pandas as pd

import os
## 高功能的计算器
import numpy as np


# 调用STATA已经清洗过的CHARLS数据库（把dta文件提到data，再选取一些提到sample）
# 直接读取绝对路径下的CHARLS文件
charls_data=pd.read_stata(r'C:\Users\Yalin\Desktop\Yellen Desktop\5 Personal research\1_data\1_data_clean\1_merge_data\CHARLS\CHARLS_ISO_2018.dta')

charls_samples=charls_data[['ID','year18','month18','city_eng18']]
# 这一步的作用是？
print(charls_samples.head())

# 将 year18 和 month18 转换为数值型
charls_samples['year18'] = pd.to_numeric(charls_samples['year18'], errors='coerce')
charls_samples['month18'] = pd.to_numeric(charls_samples['month18'], errors='coerce')


# 设定温度阈值
threshold=300
# 定义temperature文件的路径csv_holder
csv_folder=r'C:\Users\Yalin\Desktop\Yellen Desktop\2_Python\1_Environment_project\weather_data\temperature_data'

##定义一个函数来计算每个样本的平均温度
def calculate_temperature_metrics(city,month,year,csv_folder,threshold):
    # 将城市的文件夹路径和文件名路径结合在一起
    csv_file_path = os.path.join(csv_folder, f"{city}.csv")
    
    # 读取城市温度数据
    city_data = pd.read_csv(csv_file_path)


    # 提取日期中的年份和月份
    ## city_data['time']:内容：这是城市数据中的时间数据列。它可能包含字符串格式的日期和时间
    ## 利用pandas库中的函数，可以将字符串转换为日期对象
    city_data['Date'] = pd.to_datetime(city_data['time'])
    ## 从date列表中提取年份，储存在新的year中
    city_data['Year'] = city_data['Date'].dt.year
    city_data['Month'] = city_data['Date'].dt.month

     # 打印转换后的日期数据的类型和前几行数据
    print(f"\n转换后的'Date'列的类型: {city_data['Date'].dtype}")
    print(f"转换后的'Date'列的前几行数据:\n{city_data[['Date', 'Year', 'Month']].head()}")


    # 打印调试信息
    print(f"\nProcessing city: {city}, Year: {year}, Month: {month}")
    print(f"Data sample with Date, Year, Month, t2m:\n{city_data[['time', 'Date', 'Year', 'Month', 't2m']].head()}")
# 打印年份和月份的唯一值
    print(f"\nYear and Month values in city_data:\n{city_data[['Year', 'Month']].drop_duplicates()}")

    
    # 筛选出对应月份的数据
    city_data_filter = city_data[(city_data['Year'] == year) & (city_data['Month'] == month)]
    # 打印筛选后的数据样本
    print(f"\n筛选后数据样本(城市={city}, 年份={year}, 月份={month}):")
    print(f"筛选前的数据行数: {len(city_data)}")
    print(f"筛选后的数据行数: {len(city_data_filter)}")
    print(f"筛选后的数据样本:\n{city_data_filter[['Date', 'Year', 'Month', 't2m']].head()}")

    
    if city_data_filter.empty:
        print(f"没有找到对应的数据：城市={city}, 年份={year}, 月份={month}")
        return None, None
    
    # 计算每日平均气温
    ## axis用于确定沿着行（axis==0）进行还是沿着列进行（axis==1），计算新的气温并储存在新的列
    # city_data_filter['Daily_Avg_Temperature'] = city_data_filter[['t2m']].mean(axis=1)

    # 打印调试信息
    print(f"每日平均气温数据样本:\n{city_data_filter[['Date', ]].head()}")

    
    # 计算该月的平均气温
    avg_temp = city_data_filter['t2m'].mean()
    #打印调试信息
    print(f"平均气温为{avg_temp}")
    
    # 计算累计高温天数
    daily_max_temps = city_data_filter.groupby('Date')['t2m'].max()
    high_temp_days = (daily_max_temps > threshold).sum()
    
    return avg_temp, high_temp_days

# 步骤 2：计算每个样本的温度指标
## results.append() 将计算得到的每个样本的结果以元组的形式追加到列表中。
results = []

for index, row in charls_samples.iterrows():
    city = row['city_eng18']
    month = row['month18']
    year = row['year18']

    avg_temp, high_temp_days = calculate_temperature_metrics(city, month, year,csv_folder, threshold)
    # 将城市的文件夹路径和文件名路径结合在一起
    csv_file_path = os.path.join(csv_folder, f"{city}.csv")
    # 打印得到的数值
    print(f"ID: {row['ID']}, Avg Temp: {avg_temp}, High Temp Days: {high_temp_days}")
    

    if avg_temp is not None and high_temp_days is not None:
        results.append({'ID': row['ID'], 'avgtmp': avg_temp, 'cmltmp': high_temp_days})
    else:
        results.append({'ID': row['ID'], 'avgtmp': None, 'cmltmp': None})

results_df = pd.DataFrame(results)



# 将结果保存为 CSV 文件
results_df.to_csv('path_to_final_data.csv', index=False)


# 将计算结果合并到原始数据中
final_df = charls_data.merge(results_df, on='ID')

# 步骤 3：保存为新的dta文件
final_df.to_stata('path_to_final_data.dta', write_index=False)
```

```Python
现在达成的目标：完成数据的匹配，进行回归
下一步需要做的：
- 确认没有日度数据可以使用（找之前的研究联系作者，询问如何得到日度数据）
- 完成literature review的工作
- 用月度数据，确定想用的变量：月度平均，绝对howave还是相对hotwave（如何计算）
- 考虑加入气温的二次项来观察非线性的关系
- 寻找AQI 相关的数据（经管之家优先购买，寻找下载渠道其次）
- 使用FE和PSM初步探索模型的可行性（月度平均，绝对hotwave）

[注意事项] 3.1.4的数据匹配每次时间都比较久，所以有什么想要get到的数据请一次性整理好

```










