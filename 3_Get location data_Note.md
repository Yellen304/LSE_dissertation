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
  - 如果使用英文匹配，如何区别台州（浙江）和泰州（江苏），玉林（广西）与榆林（陕西），宿州（安徽）与苏州（江西），滨州（山东）和郴州（湖南）

3. 通过Python自动在CDS Toolbox中循环获取需要的天气数据


Link for Python dictionary:[https://subsequent-drop-695.notion.site/Python-Dictionary-853b7175d8c04402adcb426ea0d50637]
Mentioned commend:

reference

(1)Python获取城市的经纬度：https://geek-docs.com/python/python-ask-answer/t_how-to-get-the-longitude-and-latitude-of-a-city-using-python.html
