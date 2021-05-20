from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import config
import os
from static.views.views import Login, Barrister, Solicitor, Court, Admin, execute_command, select_record, sort_tuple, search_tuple, get_unfinished_cases

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')

app.config['MYSQL_HOST'] = config.DatabaseConfig.dbhost
app.config['MYSQL_USER'] = config.DatabaseConfig.dbuser
app.config['MYSQL_PASSWORD'] = config.DatabaseConfig.dbpassword
app.config['MYSQL_DB'] = config.DatabaseConfig.dbname
app.secret_key = os.urandom(16)

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  
        login = Login()
        url = login.handle_form_requests(mysql, request.form)      
        if url == '/':
            return render_template('login.html', incorrect="Incorrect Details!")        
        elif url == '//':
            return render_template('login.html', exists="Account already exists!")
        return redirect(url)              
    return render_template("login.html")


@app.route('/admin', methods=['GET','POST'])
def admin():  
    admin = Admin()  
    if request.method == 'POST' and "save" in request.form['submit']:
        admin.handle_form_post_requests(mysql, request.form) 
    barristers = sort_tuple(select_record(mysql, "SELECT * FROM barristers"), 0)
    courts = sort_tuple(select_record(mysql, "SELECT * FROM courts"), 1)
    solicitors = sort_tuple(select_record(mysql, "SELECT * FROM solicitors"), 0)
    cases = sort_tuple(select_record(mysql, "SELECT * FROM cases"), 0)
    addresses = sort_tuple(select_record(mysql, "SELECT * FROM addresses"), 4)
    clients = sort_tuple(select_record(mysql, "SELECT * FROM clients"), 2)

    if request.method == 'POST': 
        if request.form['submit'] == "search-barristers":
            barristers = (search_tuple(list(barristers), request.form['search-barrister'], 0),)
        elif request.form['submit'] == "search-solicitors":
            solicitors = (search_tuple(list(solicitors), request.form['search-solicitors'], 0),)
        elif request.form['submit'] == "search-courts":
            courts = (search_tuple(list(courts), request.form['search-courts'], 1),)
        elif request.form['submit'] == "search-addresses":
            addresses = (admin.search_addresses(addresses, request.form['search-addresses']),)
        elif request.form['submit'] == "search-cases":
            cases = (search_tuple(list(cases), request.form['search-cases'], 0),)
        elif request.form['submit'] == "search-clients":
            clients = (admin.search_clients(clients, request.form['search-clients']),)
            
    return render_template("adminDashboard.html", barristers=barristers, courts=courts, 
                            solicitors=solicitors, cases=cases, addresses=addresses, 
                            court_options=admin.court_options, clients=clients, layout="layout.html")

@app.route('/court/<string:id>', methods=['GET', 'POST'])
def court(id):
    court = Court()
    court_cases = sort_tuple(court.get_court_cases(mysql, id), 0)
    unfinished = get_unfinished_cases(court_cases)
    barristers = select_record(mysql, "SELECT * FROM barristers")
    solicitors = select_record(mysql, "SELECT * FROM solicitors")
    clients = select_record(mysql, "SELECT * FROM clients")
    all_cases = sort_tuple(court.get_all_cases(mysql), 2)

    if request.method == 'POST':           
        if request.form['submit'] == "search-assigned-cases":                  
            court_cases = (search_tuple(list(court_cases), request.form['search-case'], 0),)                     
        elif request.form['submit'] == "search-cases":
             all_cases = (search_tuple(list(all_cases), request.form['search-case'], 0),)        
        elif request.form['submit'] == "case-save":
            court.save_Case(mysql, request.form, id)
 
    return render_template("courtDashbaord.html", court_cases=court_cases, unfinished=unfinished, 
                            cases=all_cases, barristers=barristers, solicitors=solicitors, 
                            clients=clients, layout="layout.html")

@app.route('/barrister/<string:id>',  methods=['GET', 'POST'])
def barrister(id):
    barrister = Barrister()
    cases = sort_tuple(barrister.get_cases(mysql), 0)
    barrister_cases = sort_tuple(barrister.get_barrister_cases(mysql, id), 0)
    unfinished = get_unfinished_cases(barrister_cases)
    solicitors = select_record(mysql, "SELECT * FROM solicitors")
    clients = select_record(mysql, "SELECT * FROM clients")
    courts = select_record(mysql, "SELECT * FROM courts")
    
    if request.method == 'POST':
        if request.form['submit'] == "search-assigned-cases":
            barrister_cases = (search_tuple(list(barrister_cases), request.form['search-case'], 0),)        
        elif request.form['submit'] == "search-cases":
            cases = (search_tuple(list(cases), request.form['search-case'], 0),)
    return render_template("bar_sol_Dashboard.html", cases=cases, user_cases=barrister_cases, 
                            unfinished=unfinished, Dashboard_Type="Barrister Dashboard", 
                            solicitors=solicitors, clients=clients, courts=courts, layout="layout.html")

@app.route('/solicitor/<string:id>',  methods=['GET', 'POST'])
def solicitor(id):
    solicitor = Solicitor()
    solicitor_cases = solicitor.get_solicitor_cases(mysql, id)
    all_cases = select_record(mysql, "SELECT * FROM cases")
    unfinished=get_unfinished_cases(solicitor_cases)
    solicitors = select_record(mysql, "SELECT * FROM solicitors")
    clients = select_record(mysql, "SELECT * FROM clients")
    courts = select_record(mysql, "SELECT * FROM courts")

    if request.method == 'POST':
        if request.form['submit'] == "search-assigned-cases":
            index = search_tuple(list(solicitor_cases), request.form['search-case'], 0)
            if index != -1:
                solicitor_cases = (solicitor_cases[index], )
            else:
                solicitor_cases = ()
        elif request.form['submit'] == "search-cases":
            index = search_tuple(list(all_cases), request.form['search-case'], 0)
            if index != -1:
                all_cases = (all_cases[index], )
            else:
                all_cases = ()

    return render_template('bar_sol_Dashboard.html', cases=all_cases, user_cases=solicitor_cases, 
                            unfinished=unfinished, Dashboard_Type="Solicitor Dashboard", layout="layout.html",
                            solicitors=solicitors, courts=courts, clients=clients)


@app.errorhandler(400)
def error_400(e):
    return render_template('error_page.html', error=400, reason=e), 400

@app.errorhandler(404)
def error_404(e):
    return render_template('error_page.html', error=404, reason=e), 404

@app.errorhandler(500)
def error_500(e):
    return render_template('error_page.html', error=500, reason=e), 500

@app.errorhandler(505)
def error_505(e):
    return render_template('error_page.html', error=505, reason=e), 505


if __name__ == "__main__":
    app.run(config.Config.DEBUG, config.Config.PORT, config.Config.threaded) 