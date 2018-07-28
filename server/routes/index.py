from server import app
from flask import render_template, request

@app.route('/index')
def hello_world():
    return app.send_static_file('index.html')

@app.route('/', methods=['POST', 'GET'])
def chart_form():
    print("chart_form logic")
    if request.method == 'POST':
        print("Seleted indicator : ", request.form['indicator-1'], request.form['indicator-2'])
        print("Seleted country : ", request.form['country-1'], request.form['country-2'], request.form['country-3'])

        print(request.form['start-year'], request.form['end-year']);
    return app.send_static_file('chart_form.html')

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return app.send_static_file('404.html')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return app.send_static_file('500.html')
