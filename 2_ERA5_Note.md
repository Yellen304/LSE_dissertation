### ERA5 data
Approach 1: download .nc document

Approach 2: Use CDS Toolbox

### Approach 2: Use CDS Toolbox
1. 界面介绍
Toolbox最左边是已经写好的代码，自己创建的数据集。中间是代码编写区，最右边是结果输出的地方
2. 进入写代码的界面
[左边retrieve data]-[load]-[copy]
3. 用CDS toolbox 提取某个经纬度的时序数据
举个例子，下面是用CDS toolbox提取经纬度为（75，43）的2008-2017每天三个时段的数据。只需要在代码中修改你需要的时间地点
```
import cdstoolbox as ct

@ct.application(title='Extract point')
@ct.output.download()
@ct.input.text('lon', label='Longitude', type=float, default=75., description='Decimal degrees')
@ct.input.text('lat', label='Latitude', type=float, default=43., description='Decimal degrees')
 
def extract_time_series(lon, lat):
    """
    Application main steps:

    - set the application layout with 3 columns for the input and output at the bottom
    - retrieve a variable over a defined time range
    - select a location, defined by longitude and latitude coordinates

    """
    data = ct.catalogue.retrieve(
        'reanalysis-era5-single-levels',
        {
            'variable': '2m_temperature',
            'product_type': 'reanalysis',
            'year': [
                '2008', '2009', '2010',
                '2011', '2012', '2013',
                '2014', '2015', '2016',
                '2017'
            ],
            'month': [
                '01', '02', '03', '04', '05', '06',
                '07', '08', '09', '10', '11', '12'
            ],
            'day': [
                '01', '02', '03', '04', '05', '06',
                '07', '08', '09', '10', '11', '12',
                '13', '14', '15', '16', '17', '18',
                '19', '20', '21', '22', '23', '24',
                '25', '26', '27', '28', '29', '30',
                '31'
            ],
            'time': ['00:00', '06:00', '12:00', '18:00'],
        }
    )

    # Location selection

    # Extract the closest point to selected lon/lat (no interpolation).
    # If wrong number is set for latitude, the closest available one is chosen:
    # e.g. if lat = 4000 -> lat = 90.
    # If wrong number is set for longitude, first a wrap in [-180, 180] is made,
    # then the closest one present is chosen:
    # e.g. if lon = 200 -> lat = -160.
    data_sel = ct.geo.extract_point(data, lon=lon, lat=lat)
    csv_data=ct.cdm.to_csv(data_sel)

    return csv_data
```
4. 得到csv文件，进行分析

Reference
(1)https://cloud.tencent.com/developer/article/2185400
