from flask import Flask, render_template, request, session, redirect, url_for
import os

import database
import form_processor


app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/')
def home():
    if 'login' not in session:
        return login()
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
    return login()

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'login' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        action = request.form.get('action')
        login, password, role, name, surname, description, email, phone, photo = database.get_user(session['login'])
        problem_list = database.get_problems(login=login, role=role)

        if action == 'appoint_':
            executor = request.form.get('executor')
            database.set_executor()
        executors = database.get_executors()
        return render_template('profile.html', name=name, surname=surname, role=role, description=description,
                               email=email,
                               phone=phone, photo=photo, executors=executors, problems=problem_list)
    login, password, role, name, surname, description, email, phone, photo = database.get_user(session['login'])
    problem_list = database.get_problems(login=login, role=role)
    return render_template('profile.html', name=name, surname=surname, role=role, description=description,
                           email=email,
                           phone=phone, photo=photo, problems=problem_list)

@app.route('/start_analyse')
def start_analyse():
    if 'login' not in session:
        return login()
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

        problems = database.get_problems()

        if action == 'analyse':
            rows, back_disable, forward_disable, max_stage = form_processor.get_analyse(login, date_from, date_to, payment_systems, company)
            return render_template('analyse.html', rows=rows, back_disable=back_disable, forward_disable=forward_disable,
                                   hide_navigation=False, current_stage=max_stage, max_stage=max_stage,
                                   analyse_active=True, history_active=False, problems=problems)
        if action == 'back' or action == 'forward':
            rows, back_disable, forward_disable, current_stage, max_stage = form_processor.get_stage(login, date_from,
                                                                                       date_to, payment_systems,
                                                                                       company, action)
            return render_template('analyse.html', rows=rows, back_disable=back_disable, forward_disable=forward_disable,
                                   hide_navigation=False, current_stage=current_stage, max_stage=max_stage,
                                   analyse_active=True, history_active=False, problems=problems)
        if action == 'export':
            return form_processor.get_excel(login, date_from, date_to)
        if action == 'history':
            company = request.form.get('company_history')
            key = request.form.get('key')
            value = request.form.get('value')
            rows = form_processor.get_history(key, value, company)
            return render_template('analyse.html', rows=rows, hide_navigation=True,
                                   analyse_active=False, history_active=True, problems=problems)
        if request.form.get('appoint') is not None:
            order_id = request.form.get('appoint')
            database.update_problems_table(order_id, login, '', '0')

            problems = database.get_problems()

            rows, back_disable, forward_disable, max_stage = form_processor.get_analyse(login, date_from, date_to,
                                                                                        payment_systems, company,
                                                                                        previous=True)
            return render_template('analyse.html', rows=rows, back_disable=back_disable,
                                   forward_disable=forward_disable,
                                   hide_navigation=False, current_stage=max_stage, max_stage=max_stage,
                                   analyse_active=True, history_active=False, problems=problems)



if __name__ == '__main__':
    app.run()
