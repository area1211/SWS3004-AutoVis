from server import app
from flask import render_template

@app.route('/')
def hello_world():
    return app.send_static_file('index.html')

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')

@app.route("/chart1")
def chart1():
    import matplotlib
    from io import BytesIO
    import base64
    import pandas as pd
    from pandas_datareader import wb
    import matplotlib.pyplot as plt

    # mathces = wb.search('gdp.*capita.*const')

    id = 'NY.GDP.PCAP.KD'
    ct = ['CN','US']
    st = 2015
    ed = 2017

    dat = wb.download(indicator= id, country=ct, start=st, end=ed)

    data = dat.unstack()
    print(data)
    data.plot(kind='bar')

    # 转成图片的步骤
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    print(data)
    html = '''
       <html>
           <body>
               <img src="data:image/png;base64,{}" />
           </body>
        <html>
    '''
    plt.close()
    # 记得关闭，不然画出来的图是重复的
    return html.format(data)
    #format的作用是将data填入{}

@app.route("/chart2")
def chart2():
    import matplotlib
    from io import BytesIO
    import base64
    import pandas as pd
    from pandas_datareader import wb
    import matplotlib.pyplot as plt

    # mathces = wb.search('gdp.*capita.*const')

    # import wbdata

    mathces = wb.search('gni.*capita.*const')

    # set up the countries I want
    # countries = ['US', 'CA', 'MX']

    # set up the indicator I want (just build up the dict if you want more than one)
    # indicators = {'NY.GNP.PCAP.CD':'GNI per Capita'}

    # grab indicators above for countires above and load into data frame

    id = 'NY.GNP.PCAP.CD'
    ct = ['CL', 'UY', 'HU']
    st = 1990
    ed = 2010
    df = wb.download(indicator=id, country=ct, start=st, end=ed)

    # df is "pivoted", pandas' unstack fucntion helps reshape it into something plottable
    dfu = df.unstack(level=0)

    # a simple matplotlib plot with legend, labels and a title
    dfu.plot();
    plt.legend(loc='best');
    plt.title("GNI Per Capita ($USD, Atlas Method)");
    plt.xlabel('Date');
    plt.ylabel('GNI Per Capita ($USD, Atlas Method');

    # 转成图片的步骤
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    print(data)
    html = '''
       <html>
           <body>
               <img src="data:image/png;base64,{}" />
           </body>
        <html>
    '''
    plt.close()
    # 记得关闭，不然画出来的图是重复的
    return html.format(data)
    #format的作用是将data填入{}

@app.route("/chart3")
def chart3():
    import matplotlib
    from io import BytesIO
    import base64
    import pandas as pd
    from pandas_datareader import wb
    import matplotlib.pyplot as plt
    import numpy as np
    import statsmodels.formula.api as smf


    ind = ['NY.GDP.PCAP.KD', 'IT.MOB.COV.ZS']
    ct = 'all'
    st = 2011
    ed = 2011
    dat = wb.download(indicator=ind, country=ct, start=st, end=ed).dropna()
    dat.columns = ['gdp', 'cellphone']
    data = dat.unstack()
    print(data)
    x = data.values[:, 0]
    x = np.log(x)
    y = data.values[:, 1]
    # x = dat.value[:,0]
    # print(x)
    mod = smf.ols('cellphone ~ np.log(gdp)', dat).fit()
    y_fitted = mod.fittedvalues
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x, y, 'o', label='data')
    ax.plot(x, y_fitted, 'r--.', label='OLS')


    # 转成图片的步骤
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    print(data)
    html = '''
       <html>
           <body>
               <img src="data:image/png;base64,{}" />
           </body>
        <html>
    '''
    plt.close()
    # 记得关闭，不然画出来的图是重复的
    return html.format(data)
    #format的作用是将data填入{}


@app.route("/pyecharts")
def pyecharts():
    from pyecharts import Map
    import pandas as pd
    from pandas_datareader import wb
    import matplotlib.pyplot as plt


    # mathces = wb.search('gdp.*capita.*const')

    startYear = 2015
    endYear = 2017
    countryCode = 'all'
    indicatorCode = 'NY.GDP.PCAP.KD'

    dat = wb.download(indicator=indicatorCode,
                      country=countryCode, start=startYear, end=endYear)

    data = dat.unstack()

    index = data.index

    districts = index
    print(districts)
    areas = data.values[:, 0]
    print(areas)
    map_1 = Map("Test", width=1200, height=600)
    map_1.add("", districts, areas, maptype='world', is_visualmap=True, visual_range=[min(areas), max(areas)],
              visual_text_color='#000', is_map_symbol_show=False, is_label_show=False)
    ret_html=render_template('pyecharts.html',myechart=map_1.render_embed(),mytitle=u"数据演示",
                           host=' http://chfw.github.io/jupyter-echarts/echarts',
                           script_list=map_1.get_js_dependencies())
    return ret_html


