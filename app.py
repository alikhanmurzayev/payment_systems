from flask import Flask, render_template, request, send_from_directory


import config
import database
import form_processor
import load_attachments

app = Flask(__name__)


def get_analyse(user_ip, date_from, date_to, payment_systems):
    load_attachments.load()
    report_table_name = 'report'
    current_stage, max_stage = form_processor.make_report(date_from, date_to, report_table_name, payment_systems, latest=True)
    database.update_users_table(user_ip, max_stage, max_stage, report_table_name)
    rows = database.get_report_table_rows(report_table_name, payment_systems)
    previous_disable = True if max_stage < 2 else False
    next_disable = True
    print(current_stage, max_stage)
    return rows, previous_disable, next_disable, max_stage

def get_stage(user_ip, date_from, date_to, payment_systems, action):
    current_stage, max_stage, report_table_name = database.get_users_table(user_ip)
    database.drop_table(report_table_name)
    if action == 'previous':
        current_stage, max_stage = form_processor.make_report(date_from, date_to,
                                                              report_table_name, payment_systems,
                                                              latest=False, stage=current_stage - 1)
    elif action == 'next':
        current_stage, max_stage = form_processor.make_report(date_from, date_to,
                                                              report_table_name, payment_systems,
                                                              latest=False, stage=current_stage + 1)
    database.update_users_table(user_ip, current_stage, max_stage, report_table_name)
    rows = database.get_report_table_rows(report_table_name, payment_systems)
    previous_disable = True if current_stage < 2 else False
    next_disable = True if current_stage >= max_stage else False
    return rows, previous_disable, next_disable, current_stage, max_stage

def get_excel(user_ip, date_from, date_to):
    current_stage, max_stage, report_table_name = database.get_users_table(user_ip)
    file_name = database.export_to_excel(report_table_name)
    file_path = config.reports_dir
    report_name = report_table_name + '_' + str(date_from).replace('-', '.') + '-' + str(date_to).replace('-', '.') + '.xlsx'
    return send_from_directory(file_path + '/', file_name, as_attachment=True, attachment_filename=report_name)




@app.route('/')
def home():
    return render_template("Choco.html", hide_navigation=True)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        user_ip = request.remote_addr
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')

        # checkboxes
        payment_systems = list()
        if request.form.get('kaspi') != None:
            payment_systems.append(config.kaspi_name)
        if request.form.get('processing') != None:
            payment_systems.append(config.processing_name)

        # one of four actions: analyse, previous, next, export
        action = request.form.get('action')
        if action == 'analyse':
            rows, previous_disable, next_disable, max_stage = get_analyse(user_ip, date_from, date_to, payment_systems)
            return render_template('Choco.html', rows=rows, previous_disable=previous_disable, next_disable=next_disable,
                                   hide_navigation=False, current_stage=max_stage, max_stage=max_stage)
        if action == 'previous' or action == 'next':
            rows, previous_disable, next_disable, current_stage, max_stage = get_stage(user_ip, date_from,
                                                                                       date_to, payment_systems,
                                                                                       action)
            return render_template('Choco.html', rows=rows, previous_disable=previous_disable, next_disable=next_disable,
                                   hide_navigation=False, current_stage=current_stage, max_stage=max_stage)
        if action == 'export':
            return get_excel(user_ip, date_from, date_to)




if __name__ == '__main__':
    app.run()
