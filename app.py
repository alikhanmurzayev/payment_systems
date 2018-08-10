from flask import Flask, render_template, request, send_from_directory, session
import os


import config
import database
import form_processor
import gmail

app = Flask(__name__)
app.secret_key = os.urandom(12)


def get_analyse(login, date_from, date_to, payment_systems, company):
    gmail.load(company)
    report_table_name = form_processor.get_report_table_name(login, company)
    current_stage, max_stage = form_processor.make_report(date_from, date_to, report_table_name, payment_systems,
                                                          company, latest=True)
    database.update_working_table(login, max_stage, max_stage, report_table_name)
    rows = database.get_report_table_rows(report_table_name)
    back_disable = True if max_stage < 2 else False
    forward_disable = True
    return rows, back_disable, forward_disable, max_stage

def get_stage(login, date_from, date_to, payment_systems, company, action):
    current_stage, max_stage, report_table_name = database.get_working_table(login)
    database.drop_table(report_table_name)
    if action == 'back':
        current_stage, max_stage = form_processor.make_report(date_from, date_to,
                                                              report_table_name, payment_systems, company,
                                                              latest=False, stage=current_stage - 1)
    elif action == 'forward':
        current_stage, max_stage = form_processor.make_report(date_from, date_to,
                                                              report_table_name, payment_systems, company,
                                                              latest=False, stage=current_stage + 1)
    database.update_working_table(login, current_stage, max_stage, report_table_name)
    rows = database.get_report_table_rows(report_table_name)
    previous_disable = True if current_stage < 2 else False
    next_disable = True if current_stage >= max_stage else False
    return rows, previous_disable, next_disable, current_stage, max_stage

def get_excel(login, date_from, date_to):
    current_stage, max_stage, report_table_name = database.get_working_table(login)
    file_name = database.export_to_excel(report_table_name)
    file_path = config.reports_dir
    report_name = str(current_stage) + '_' + report_table_name + '_' + str(date_from).replace('-', '.') + '-' + str(date_to).replace('-', '.') + '.xlsx'
    return send_from_directory(file_path + '/', file_name, as_attachment=True, attachment_filename=report_name)

def get_history(key, value, company):
    history_table_name = form_processor.make_history_table(key, value, company)
    rows = database.get_report_table_rows(history_table_name)
    return rows




@app.route('/')
def home():
    if 'login' not in session:
        return render_template('login.html')
    else:
        return render_template('profile.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        if database.check_user(login, password):
            session['logged_in'] = True
            session['login'] = login
            return home()
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('login', None)
    session['logged_in'] = False
    return home()

@app.route('/start_analyse')
def start():
    return render_template('Choco.html', hide_navigation=True, analyse_active=True, history_active=False)

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
            rows, back_disable, forward_disable, max_stage = get_analyse(login, date_from, date_to, payment_systems, company)
            return render_template('Choco.html', rows=rows, back_disable=back_disable, forward_disable=forward_disable,
                                   hide_navigation=False, current_stage=max_stage, max_stage=max_stage,
                                   analyse_active=True, history_active=False)
        if action == 'back' or action == 'forward':
            rows, back_disable, forward_disable, current_stage, max_stage = get_stage(login, date_from,
                                                                                       date_to, payment_systems,
                                                                                       company, action)
            return render_template('Choco.html', rows=rows, back_disable=back_disable, forward_disable=forward_disable,
                                   hide_navigation=False, current_stage=current_stage, max_stage=max_stage,
                                   analyse_active=True, history_active=False)
        if action == 'export':
            return get_excel(login, date_from, date_to)
        if action == 'history':
            company = request.form.get('company_history')
            key = request.form.get('key')
            value = request.form.get('value')
            rows = get_history(key, value, company)
            return render_template('Choco.html', rows=rows, hide_navigation=True,
                                   analyse_active=False, history_active=True)



if __name__ == '__main__':
    app.run()
