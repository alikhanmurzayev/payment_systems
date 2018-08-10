from flask import Flask, render_template, request, session
import os

import database
import form_processor


app = Flask(__name__)
app.secret_key = os.urandom(12)





@app.route('/')
def home():
    if 'login' not in session:
        return login()
    else:
        return profile()



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        if database.check_user(login, password):
            session['logged_in'] = True
            session['login'] = login
            return home()
        return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('login', None)
    session['logged_in'] = False
    return home()

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/start_analyse')
def start_analyse():
    return render_template('analyse.html', hide_navigation=True, analyse_active=True, history_active=False)

@app.route('/analyse', methods=['GET', 'POST'])
def analyse():
    if request.method == 'POST':
        login = session['login']
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        payment_systems = request.form.getlist('payment_systems')
        company = request.form.get('company')
        action = request.form.get('action')
        if action == 'analyse':
            rows, back_disable, forward_disable, max_stage = form_processor.get_analyse(login, date_from, date_to, payment_systems, company)
            return render_template('analyse.html', rows=rows, back_disable=back_disable, forward_disable=forward_disable,
                                   hide_navigation=False, current_stage=max_stage, max_stage=max_stage,
                                   analyse_active=True, history_active=False)
        if action == 'back' or action == 'forward':
            rows, back_disable, forward_disable, current_stage, max_stage = form_processor.get_stage(login, date_from,
                                                                                       date_to, payment_systems,
                                                                                       company, action)
            return render_template('analyse.html', rows=rows, back_disable=back_disable, forward_disable=forward_disable,
                                   hide_navigation=False, current_stage=current_stage, max_stage=max_stage,
                                   analyse_active=True, history_active=False)
        if action == 'export':
            return form_processor.get_excel(login, date_from, date_to)
        if action == 'history':
            company = request.form.get('company_history')
            key = request.form.get('key')
            value = request.form.get('value')
            rows = form_processor.get_history(key, value, company)
            return render_template('analyse.html', rows=rows, hide_navigation=True,
                                   analyse_active=False, history_active=True)
        if request.form.get('appoint') is not None:
            primary_id = request.form.get('appoint')
            print(primary_id)
            rows, back_disable, forward_disable, max_stage = form_processor.get_analyse(login, date_from, date_to,
                                                                                        payment_systems, company,
                                                                                        previous=True)
            return render_template('analyse.html', rows=rows, back_disable=back_disable,
                                   forward_disable=forward_disable,
                                   hide_navigation=False, current_stage=max_stage, max_stage=max_stage,
                                   analyse_active=True, history_active=False)



if __name__ == '__main__':
    app.run()
