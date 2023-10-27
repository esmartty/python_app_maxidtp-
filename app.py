class EndDateLessStartDate(Exception):
    def __init__(self, update_from, update_to):
        Exception.__init__(self)
        self.message = "Error. Bad input. End date " + str(update_to) + " is less than start date " + str(update_from) +"."

from flask import Flask, render_template, redirect, request, url_for
#from flask_basicauth import BasicAuth
from datetime import date, datetime
import nbu_exchange_rate
import upload_google_sheet

app = Flask(__name__)

#HTTP basic access authentication by Flask-BasicAuth. - is not maintained by Pythonanyehere hosting, last Python 3.10 version
##app.config['BASIC_AUTH_USERNAME'] = 'Test User'
##app.config['BASIC_AUTH_PASSWORD'] = '1234'

#basic_auth = BasicAuth(app)

@app.route('/')
#@basic_auth.required
def enter_data():
    return render_template('index.html', update_from = date.today(), update_to = date.today())

@app.route('/processing', methods = ['GET', 'POST'])
def processing():
    if request.method == 'POST':
        try:
            update_from_str = request.form.get('update_from')
            update_to_str = request.form.get('update_to')

            if update_from_str:
                update_from = datetime.strptime(update_from_str, '%Y-%m-%d').date()
            else:
                update_from = date.today()

            if update_to_str:
                update_to = datetime.strptime(update_to_str, '%Y-%m-%d').date()
            else:
                update_to = date.today()

            if update_to < update_from:
                raise EndDateLessStartDate(update_from, update_to)

            exchange_rate = nbu_exchange_rate.get_from_api(update_from, update_to)

            upload_google_sheet.upload(exchange_rate)

            return redirect(url_for('result'))
        except EndDateLessStartDate as err:
            # return error page with 400 error code (Bad Request)
            return (render_template('error.html', message = err.message), 400)
        except Exception:
            # return error page with 500 error code (Internal server error)
            return (render_template('error.html', message = "Internal server error."), 500)

    return redirect(url_for('enter_data'))

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug = True)