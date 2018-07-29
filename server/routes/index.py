from server import app
from flask import render_template,request



@app.route('/')
def hello_world():
    return app.send_static_file('chart_form.html')

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')

@app.route('/form', methods=['POST', 'GET'])
def chart_form():
    print("chart_form logic")
    if request.method == 'POST':
        CountryCode = [request.form['country-1'], request.form['country-2'], request.form['country-3']]
        indicator1 = request.form['indicator-1']
        indicator2 = request.form['indicator-2']
        country1 =  request.form['country-1']
        country2 = request.form['country-2']
        country3 = request.form['country-3']
        startY = request.form['start-year']
        endY = request.form['end-year']
        cleanedList = [x for x in CountryCode if str(x) != 'NaN']
        if(startY == endY and country1 == 'NaN'and country2 == 'NaN'and country3 == 'NaN'and indicator2 == 'NaN'and indicator1 !='NaN'):
            return pyecharts(indicator1,startY,endY)
        elif(startY == endY and country1 == 'NaN'and country2 == 'NaN'and country3 == 'NaN'and indicator2 != 'NaN'and indicator1 !='NaN'):
            return  chart3(indicator1, indicator2,startY,endY)
        elif ((int(endY) - int(startY)) > 5 and indicator1 != 'NaN' and indicator2 == 'NaN' and (
                country1 != 'NaN' or country2 != 'NaN' or country3 != 'NaN')):
            return chart2(indicator1, cleanedList, startY, endY)
        elif(startY <= endY and indicator1 != 'NaN'and(country1 != 'NaN'or country2 != 'NaN'or country3 != 'NaN')):
            return chart1(indicator1,cleanedList,startY,endY)

    return app.send_static_file('chart_form.html')


def chart1(indicator1, countryCode, startY, endY):
    import matplotlib
    from io import BytesIO
    import base64
    import pandas as pd
    from pandas_datareader import wb
    import matplotlib.pyplot as plt

    # mathces = wb.search('gdp.*capita.*const')

    dat = wb.download(indicator= indicator1, country=countryCode, start=startY, end=endY)

    data = dat.unstack()
    print(data)
    data.plot(kind='bar')


    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    html = '''
       <html>
           <body>
               <img src="data:image/png;base64,{}" />
           </body>
        <html>
    '''
    picture =  "data:image/png;base64,"+data
    #print(picture)
    plt.close()
    #return html.format(data)
    return render_template("home.html",picture = picture)


def chart2(indicator1, countryCode, startY, endY):
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

    id = indicator1
    ct = countryCode
    st = startY
    ed = endY
    df = wb.download(indicator=id, country=ct, start=st, end=ed)

    # df is "pivoted", pandas' unstack fucntion helps reshape it into something plottable
    dfu = df.unstack(level=0)

    # a simple matplotlib plot with legend, labels and a title
    dfu.plot();
    plt.legend(loc='best');
    plt.title("Result");
    plt.xlabel('Date');
    plt.ylabel('Indicator1');


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
    picture = "data:image/png;base64," + data
    # print(picture)
    plt.close()
    # return html.format(data)
    return render_template("home.html", picture=picture)



def chart3(indicator1,indicator2, startY, endY):
    import matplotlib
    from io import BytesIO
    import base64
    import pandas as pd
    from pandas_datareader import wb
    import matplotlib.pyplot as plt
    import numpy as np
    import statsmodels.formula.api as smf


    ind = [indicator1, indicator2]
    ct = 'all'
    st = startY
    ed = endY
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
    picture = "data:image/png;base64," + data
    # print(picture)
    plt.close()
    # return html.format(data)
    return render_template("home.html", picture=picture)




def pyecharts(indicator1, startY, endY):
    from pyecharts import Map
    import pandas as pd
    from pandas_datareader import wb
    import matplotlib.pyplot as plt


    # mathces = wb.search('gdp.*capita.*const')

    startYear = startY
    endYear = endY
    countryCode = 'all'
    indicatorCode = indicator1

    dat = wb.download(indicator=indicatorCode,
                      country=countryCode, start=startYear, end=endYear)

    data = dat.unstack()

    index = data.index

    districts = index
    print(districts)
    areas = data.values[:, 0]
    print(areas)
    map_1 = Map(indicator1, width=1200, height=600)
    map_1.add("", districts, areas, maptype='world', is_visualmap=True, visual_range=[min(areas), max(areas)],
              visual_text_color='#000', is_map_symbol_show=False, is_label_show=False)
    ret_html=render_template('pyecharts.html',myechart=map_1.render_embed(),mytitle=u"HeatMap",
                           host=' http://chfw.github.io/jupyter-echarts/echarts',
                           script_list=map_1.get_js_dependencies())
    return ret_html


