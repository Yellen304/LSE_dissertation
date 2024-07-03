本章的目的在于将CHARLS中匹配的城市从Stata中提取出来，通过Python自动获取100+城市的经纬度信息，通过Python自动在CDS Toolbox中循环获取需要的天气数据

1. `CHARLS中匹配的城市从Stata中提取出来`
- 将所需要的数据export成EXCEL
- [Excel 数据]-[删除重复值]

2. `通过Python自动获取100+城市的经纬度信息`
  - [将城市看作一个范围]https://blog.csdn.net/esa72ya/article/details/114642127 （不全）
  - [将城市简化为中心点]https://latitude.to/map/cn/china/cities/shantou#google_vignette

  需要做的步骤
  - 把检查页面打印并保存到txt
  - 把txt中的中文识别为英文
  - 从excel的第一排开始，找到相关的名字，然后读取附近的数字，再输出到excel的后面
  - 如果使用英文匹配，如何区别@台州（浙江）和泰州（江苏），@玉林（广西）与榆林（陕西），@宿州（安徽）与苏州（江苏），滨州（山东）和郴州（湖南）（无）
  - 计算城市中心

3. 通过Python自动在CDS Toolbox中循环获取需要的天气数据 （循环次数129）
  - 从Excel中读取第一个城市的经纬度信息
  - 在CDS Toolbox中输入，选择时间和所需要的所有天气数据，下载成为一个单独的excel表格
  - 重复直到100+城市的天气数据被下载完成

4. 通过Python调取stata文件中每一个人的采访时间数据，对Excel进行分析 （循环次数8000+）
   - 使用python调取第一列人的采访时间和居住地点（英文）
   - 调取地点excel，打开文件，根据时间提取当月的平均温度、累计高温
   - 返回温度信息到stata中


Link for Python dictionary:[https://subsequent-drop-695.notion.site/Python-Dictionary-853b7175d8c04402adcb426ea0d50637]
Mentioned commend:

reference

(1)Python获取城市的经纬度：https://geek-docs.com/python/python-ask-answer/t_how-to-get-the-longitude-and-latitude-of-a-city-using-python.html
