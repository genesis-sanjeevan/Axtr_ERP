from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, date
from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import sqlite3
import pandas as pd
import math
import csv
import numpy as np
import os

app = Flask(__name__)

# dash_app = Dash(__name__, server= app, url_base_pathname='/empdashboard/', external_stylesheets=[dbc.themes.ZEPHYR])
app.secret_key = "thisisasecretkeydabros"

connection = sqlite3.connect('employee.db', check_same_thread=False)
cursor = connection.cursor()

_today = date.today()
datestr = _today.strftime('%Y-%m-%d')
days_ago = _today - timedelta(days=7)
days_ago = days_ago.strftime('%Y-%m-%d')


@app.route('/',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username  
        query = "SELECT * FROM EMPLOYEE_DATA"
        cursor.execute(query)
        results = cursor.fetchall()
        _x_=0
        for i in results:
            if username in i[2]:
                _x_+=1
                if check_password_hash(i[3],password):
                    if i[4] == 0:
                        return redirect(url_for('emp_profile'))
                    else:
                        return redirect(url_for('admin_dls'))
                else:
                    flash("Invalid Password, Please try again")
        if _x_==0:
            flash("User does not exist!")
        
    return render_template('login.html')

@app.route('/adduser', methods = ['POST','GET'])
def add_user():
    # FETCHING DATA FROM DATABASE#
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')

    cursor.execute("SELECT * FROM EMPLOYEE_DATA")

    if request.method == "POST":
            psnum = request.form.get('psnum').upper()
            name = request.form.get('name').upper().replace(' ','_')
            username = request.form.get('username')
            password = request.form.get('password')
            access = 0
            rows = cursor.fetchall()
            # print(rows)
                
            data_list = [psnum,name,username,generate_password_hash(password), access]

            try:
                command = """INSERT INTO EMPLOYEE_DATA
                        (PS_NUMBER, NAME, USERNAME, PASSWORD, ADMIN_ACCESS)
                        VALUES(?,?,?,?,?);"""
        
                cursor.executemany(command, [data_list])
                connection.commit()
                print('Data inserted successfully!')
                flash('Registered Successfully!', category='success')
                connection.close()
        
            except sqlite3.Error as error:
                    flash('Credentials already in use!', category= 'inputerror')

    return render_template("adduser.html", Emp_ID = Emp_ID, Emp_Name=name)

@app.route('/addproject', methods = ['POST','GET'])
def add_project():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')

    cursor.execute("SELECT * FROM PROJECT_DATA")
    result = cursor.fetchall()
    table2_data=[]
    for i in result:
        if i[4] == 'Completed':
            pass
        else:
            table2_data.append(i)

    if request.method == 'POST':
        project_id = request.form.get('project_id')
        project_name = request.form.get('projectname')
        start_date = request.form.get('startdate')
        target_date = request.form.get('targetdate')
        status = request.form.get('Status')

        project_data_list = [project_id,project_name,start_date,target_date,status,'']

        try:
            command = """INSERT INTO PROJECT_DATA
                        (PROJ_ID, PROJ_NAME, START_DATE, TARGET_DATE, STATUS, COMPLETION_DATE)
                        VALUES(?,?,?,?,?);"""
        
            cursor.executemany(command, [project_data_list])
            connection.commit()
            print('Data inserted successfully!')
            flash('Project Added to Database Successfully!', category='success')
            connection.close()
        
        except sqlite3.Error as error:
            flash('Entered Credentials are already in use!', category= 'inputerror')

    # if request.method == 'GET':
    #     project_idd = request.form.getlist('project_name')
    #     print(project_idd)
    #     flash('Project marked as Completed Successfully!', category='success')
            # try:
            #     command = """UPDATE PROJECT_DATA
            #             SET STATUS='Completed', COMPLETION_DATE={completion_date}
            #         WHERE PROJ_ID={project_id}""".format(completion_date,project_id)
        
            #     cursor.executemany(command, [project_data_list])
            #     connection.commit()
            #     print('Data inserted successfully!')
            #     flash('Project Added to Database Successfully!', category='success')
            #     connection.close()
        
            # except sqlite3.Error as error:
            #     flash('Error occured while Updating the Database! Please Try Again!', category= 'inputerror')
    return render_template('project.html',table2_data=table2_data,  Emp_ID = Emp_ID, Emp_Name=name)

@app.route('/admindls')
def admin_dls():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')

     #SETTING FORM DROPDOWN OPTIONS FROM PROJECT_TYPES CSV FILE#
    formval = pd.read_csv('Dataset\Master\Project_Types.csv')
    cols = formval.columns.values
    fulllist =[] 
    for i in cols:
        if "Unnamed" in i:
            pass
        else:
            l=[]
            for j in formval[i]:
                if type(j) is not str:
                    if math.isnan(j):
                        pass
                    else:
                        l.append(j)
                else:
                    l.append(j)
            fulllist.append(l)

    print(fulllist)

    return render_template('admin_dls.html',project = fulllist[1], fieldowork = fulllist[2], section = fulllist[3], dailyactivity = fulllist[4], progresses = fulllist[5],
                           Emp_ID = Emp_ID, Emp_Name=name)

@app.route('/adminleave')
def admin_leave():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')

    return render_template('admin_leave.html', Emp_ID = Emp_ID, Emp_Name=name)

@app.route('/adminpermission')
def admin_permission():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')

    return render_template('admin_permission.html', Emp_ID = Emp_ID, Emp_Name=name)

@app.route('/adminactualreport')
def admin_actual_report():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')

    return render_template('admin_actual_report.html', Emp_ID = Emp_ID, Emp_Name=name)

@app.route('/adminplandatalog', methods = ['POST','GET'])
def admin_plan():

    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')
    cursor.execute("SELECT * FROM EMPLOYEE_DATA")
    data_table1 = cursor.fetchall()

    formval = pd.read_csv('Dataset\Master\Project_Types.csv')
    cols = formval.columns.values
    fulllist =[] 
    for i in cols:
        if "Unnamed" in i:
            pass
        else:
            l=[]
            for j in formval[i]:
                if type(j) is not str:
                    if math.isnan(j):
                        pass
                    else:
                        l.append(j)
                else:
                    l.append(j)
            fulllist.append(l)

    if request.method == 'POST':
        due_date = request.form.get('calender')
        project_name = request.form.get('project')
        fieldowork_name = request.form.get('workfield')
        section_name = request.form.get('section')
        assigned_man_hours = request.form.get('manhours')
        assigned_employee = request.form.getlist('selected-employee-list')
        comments = request.form.get('Comments')

        for i in assigned_employee:
            q='''INSERT INTO ADMIN_PLAN(DUE_DATE,PROJECT,FIELD_OF_WORK,SECTION,ASSIGNED_MANHOURS,ASSIGNED_TO,STATUS,COMMENTS,ASSIGNED_BY) VALUES(?,?,?,?,?,?,?,?,?)'''
            
            data_list = [due_date,project_name,fieldowork_name,section_name,int(assigned_man_hours),i,"In Progress",comments,Emp_ID]

            cursor.execute(q,data_list)
            connection.commit()

        flash("Task Assigned Successfully!")
           
        # print(due_date,project_name,fieldowork_name,section_name,assigned_man_hours,assigned_employee,comments)



    return render_template('planform_admin.html', Emp_ID = Emp_ID, Emp_Name=name,table1_data=data_table1, project = fulllist[1], fieldowork = fulllist[2], section = fulllist[3])

@app.route('/view_assigned_tasks')
def view_assigned_task():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')

    q = 'SELECT * FROM ADMIN_PLAN'
    cursor.execute(q)
    data_table1 = cursor.fetchall()
    # print(data_table1)

    plan_list =[]
    final_plan_list=[]

    for i in data_table1:
        if i[0] < datestr:
            update_query ='''UPDATE ADMIN_PLAN SET STATUS = ?  WHERE 
                            PROJECT = ? AND FIELD_OF_WORK = ? AND SECTION = ? AND ASSIGNED_MANHOURS = ? AND 
                            ASSIGNED_TO = ? AND ASSIGNED_BY = ?'''
            update_query_support_list = ["OverDue",i[1],i[2],i[3],i[4],i[5],i[8]]
            cursor.execute(update_query,update_query_support_list)
            connection.commit()

    cursor.execute('SELECT * FROM ADMIN_PLAN')
    data_table1 = cursor.fetchall()
    for i in data_table1:
        if i[8] == Emp_ID:
            plan_list=[i[0],i[1],i[2],i[3],i[7],i[5],i[6]]
            final_plan_list.append(plan_list)
        else:
            pass
        

    return render_template('assigned_tasks_admin.html', Emp_ID = Emp_ID, Emp_Name=name, table1_data = final_plan_list)


@app.route('/adminplanreport')
def admin_plan_report():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')
    print(Emp_ID)

    cursor.execute('SELECT * FROM ADMIN_PLAN WHERE ASSIGNED_TO = ?',(Emp_ID,))
    table = cursor.fetchall()
    print(table)
    
    return render_template('plan_report.html', Emp_ID = Emp_ID, Emp_Name=name,)

@app.route('/employeeplan',methods = ['POST','GET'])
def employee_plan():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')

    cursor.execute('SELECT * FROM ADMIN_PLAN WHERE ASSIGNED_TO = ?',(Emp_ID,))
    table = cursor.fetchall()
    print(table)

    plan_list = []
    final_list = []

    for i in table:
        r = 'SELECT NAME FROM EMPLOYEE_DATA WHERE PS_NUMBER = ?'
        cursor.execute(r,(i[8],))
        s = cursor.fetchone()
        admin_name = s[0]
        admin_name = admin_name.replace('_',' ')
        plan_list = [i[0],i[1],i[2],i[3],i[4],admin_name,i[6],i[7]]
        final_list.append(plan_list)
    
    if request.method == ['POST']:
        table_data_scraped = request.form.getlist('plan')

        print(table_data_scraped)


    return render_template('employee_plan_report.html', Emp_ID = Emp_ID, Emp_Name=name, table_data = final_list )


# @app.route('/updated_employee_plan')
# def update_employee_plan():




@app.route('/adminreport')
def admin_report():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')

    query0 = 'SELECT * FROM EMPLOYEE_DATA'
    cursor.execute(query0)
    emp_results = cursor.fetchall()

    cursor.execute('SELECT * FROM PROJECT_DATA')
    proj_result = cursor.fetchall()

    # print(emp_results)
    # print(proj_result)

    return render_template('admin_report.html', Emp_ID = Emp_ID, Emp_Name=name,table1_data=emp_results, table2_data=proj_result)



@app.route('/profile', methods = ["POST","GET"])
# @login_required
def emp_profile():
    #FETCHING DATA FROM DATABASE#
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')

    #SETTING FORM DROPDOWN OPTIONS FROM PROJECT_TYPES CSV FILE#
    formval = pd.read_csv('Dataset\Master\Project_Types.csv')
    cols = formval.columns.values
    fulllist =[] 
    for i in cols:
        if "Unnamed" in i:
            pass
        else:
            l=[]
            for j in formval[i]:
                if type(j) is not str:
                    if math.isnan(j):
                        pass
                    else:
                        l.append(j)
                else:
                    l.append(j)
            fulllist.append(l)

    #SELECTING CSV FILE FROM LOG SHEET FOLDER#
    path = "Dataset/Log Sheets"
    files = []
    file = 0
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and Emp_ID in i:
            files.append(i)
            file = file+1
            print(i)
    if file == 0:
        print("No Log Sheet Of User Found")
    fileloc = path+"/"+files[0]
    session['fileloc'] = fileloc

    #CAPTURING FORM DATA FROM DLS#
    if request.method == "POST":
        date_ = request.form.get("calender")
        project = request.form.get("project")
        fieldowork = request.form.get("workfield")
        dlssection = request.form.get("section")
        dlsdailyactivity = request.form.get("dailyactivity")
        manhours = request.form.get("manhours")
        progress = request.form.get("progress")
        comments = request.form.get("Comments")
        if project.startswith("HOLIDAY"):
            completelist = [date_, project, project, project, project, manhours, progress, comments]
        else:
            completelist = [date_, project, fieldowork, dlssection, dlsdailyactivity, manhours, progress, comments]
        print(completelist)
        #WRITING IN THE CSV FILE#
        with open(fileloc,"a") as ls:
            data = csv.writer(ls)
            data.writerow(completelist)

        ls = pd.read_csv(fileloc, usecols=['DATE','MAN_HOURS'])

        dates=ls['DATE'].tolist()
        man_hours=ls['MAN_HOURS'].tolist()

        x=zip(dates,man_hours)
        l=list(x)
        d=dict()
        for i in l:
            if i[0] is not np.nan:
                d[i[0]]=0
        for j in l:
            if j[1] is not np.nan and j[0] is not np.nan:
                d[j[0]]+=j[1]
        now = date.today()
        date_string = now.strftime('%Y-%m-%d')
        for key, value in d.items():
            if key == date_string:
                b = {value}
                for i in b:
                    if i < 8:
                        a = 8-i
                        msg = "Remaining {a} hour(s) of log is need to be filled!".format(a=a)
                        flash(msg, category='error')    
                    elif i >= 8 :
                        msg1 = "Today's log entered successfully ({ab}) ({hours} hours)".format(ab=now.strftime('%d-%m-%Y'), hours=i)
                        flash(msg1, category='success')
        
        flash("Log Submitted Successfully!", category='success')

    return render_template('dls.html', project = fulllist[1], fieldowork = fulllist[2], section = fulllist[3], dailyactivity = fulllist[4], progresses = fulllist[5],
                            Emp_ID = Emp_ID, Emp_Name = name, datestr = datestr, 
                            days_ago = days_ago
                            )   

@app.route('/leave', methods = ["GET","POST"])
# @login_required
def leaveform():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')
    if request.method == "POST":
        date = request.form.get('leavecalender')
        leavehours = request.form.get('number')
        leavelist = [date,"LEAVE","LEAVE","LEAVE","LEAVE",leavehours]
        print(leavelist)
        fileloc = session.get('fileloc')
        with open(fileloc,"a") as ls:
            data = csv.writer(ls)
            data.writerow(leavelist)
        flash('Leave log Submitted successfully!', category='success')
    else:
        print("Nooo brooo")
    return render_template('leave.html', Emp_ID = Emp_ID, Emp_Name = name, datestr = datestr, 
    days_ago = days_ago
    )

@app.route('/permission', methods = ["GET","POST"])
# @login_required
def permissionform():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')
    if request.method == "POST":
        date = request.form.get('calender')
        permissionhours = request.form.get('number')
        permissionlist = [date,'PERMISSION','PERMISSION','PERMISSION','PERMISSION',permissionhours]
        print(permissionlist)
        fileloc = session.get('fileloc')
        with open(fileloc,"a") as ls:
            data = csv.writer(ls)
            data.writerow(permissionlist)
        flash('Permission Log submitted succesfully!')
    return render_template('permission.html', Emp_ID = Emp_ID, Emp_Name = name, datestr = datestr, 
    days_ago = days_ago
    )

@app.route('/actualreportform', methods = ["GET","POST"])
# @login_required
def actualreportform():
    eusername = session.get('username')
    query = "SELECT * FROM EMPLOYEE_DATA WHERE username = ?"
    cursor.execute(query, (eusername,))
    record = cursor.fetchone()
    Emp_ID = record[0]
    name = record[1].replace('_',' ')

    if request.method == "POST":
        astartreportdate = request.form.get("stdate")
        aendreportdate = request.form.get("enddate")
        # print(astartreportdate , aendreportdate)
        fromdate = datetime.strptime(astartreportdate,'%Y-%m-%d').strftime('%m/%d/%Y')
        todate = datetime.strptime(aendreportdate,'%Y-%m-%d').strftime('%m/%d/%Y')

        if min(fromdate, todate) == todate:
            flash('Please Enter a valid date range.', category='error')
        else:
            print(fromdate, todate)
            session['frmdate'] = fromdate
            session['todate'] = todate
            return redirect(url_for('empdashboard'))

    return render_template('actualreportform.html',Emp_ID = Emp_ID, Emp_Name = name, datestr = datestr)



@app.route('/empdashboard/')
def empdashboard():
    # global layout
    fileloc = session.get('fileloc')
    fromdate = session.get('frmdate')
    todate = session.get('todate')
    ls = pd.read_csv(fileloc, skip_blank_lines=True)
    x = datetime.strptime(fromdate,"%d%m%Y")
    y = datetime.strptime(todate,"%d%m%Y")
    d1 = datetime.strptime(x,"%m/%d/%Y")
    d2 = datetime.strptime(y,"%m/%d/%Y")
    delta=d2-d1
    # print(delta)
    dates=[]
    for i in range(delta.days+1):
        day=(d1+timedelta(days=i)).strftime("%m/%d/%Y")
        dates.append(day)
    print(dates)
    a=[]
    for i in range(len(ls)):
        print(ls.loc[i,"DATE"])
        date=(datetime.strptime(ls.loc[i,str("DATE")],"%m/%d/%y")).strftime("%m/%d/%Y")
        if date in dates:
            a.append((ls.loc[i]).tolist())
    print(a)
    df=pd.DataFrame(a,columns=['DATE','PROJECT','FIELD_OF_WORK','SECTION','DAILY_ACTIVITY','MAN_HOURS','PROGRESS','COMMENTS'])
    dfs = df['MAN_HOURS'].sum()
    print(df)
    print(dfs)
    proj_pie = px.pie(data_frame=df, names='PROJECT', values='MAN_HOURS', title='PROJECTS WORKED',)
    proj_pie.update_traces(textposition = 'outside', textinfo = 'percent+label', rotation = 180)
    proj_pie.update_layout(showlegend = True, plot_bgcolor='rgb(217, 222, 221)')

    fldow_pie = px.pie(data_frame=df, names='FIELD_OF_WORK', values='MAN_HOURS', title='FIELD OF WORK CONCENTRTED', labels='FIELD_OF_WORK', template='plotly_white')
    fldow_pie.update_traces(textposition = 'outside', textinfo = 'percent+label', rotation = 180)
    # fldow_pie.update_layout(showlegend = False)

    sec_pie = px.pie(data_frame=df, names='SECTION', values='MAN_HOURS', title='SECTIONS WORKED', template='plotly_white')
    sec_pie.update_traces(textposition = 'outside', textinfo = 'percent+label', rotation = 180)
    # sec_pie.update_layout(showlegend = False)

    daila_pie = px.pie(data_frame=df, names='DAILY_ACTIVITY', values='MAN_HOURS', title='DAILY ACTIVITY WORKED', template='plotly_white')
    daila_pie.update_traces(textposition = 'outside', textinfo = 'percent+label', rotation = 180)
    # daila_pie.update_layout(showlegend = False)

    proj_bar = px.bar(data_frame=df, x='PROJECT', y='MAN_HOURS', title='Most worked Project', color='PROJECT')
    proj_bar.update_traces()
    # proj_bar.update_layout(showlegend = False)

    dr_card = dbc.Card([
            dbc.CardBody([
                html.H1(x+' - '+y,style={'text-align':'center',
                # 'font-size':'28pt'
                }),
                html.H3('Selected Date Range', style={'text-align':'center', 'color':'#003f72'})])
                ], color='light', style={'height':'125px','width':'auto'})
    mhcrd = dbc.Card([
            dbc.CardBody([
            html.H1(dfs,style={'text-align':'center','font-weight':'bold'}),
            html.H3('Man Hour(s)',style={'text-align':'center', 'color':'#003f72'})])
            ], color='light', style={'height':'125px','width':'auto'})
    efficiency = dbc.Card([
            dbc.CardBody([
            html.H1("0%", style={'text-align':'center', 'font-weight':'bold'}),
            html.H3("Efficiency", style={'text-align':'center', 'color':'#003f72'})
        ])
        ], color='light', style={'height':'125px','width':'auto'})

    rows = [dbc.Row([
            dbc.Col(dr_card, width=6),
            dbc.Col(mhcrd, width=3),
            dbc.Col(efficiency, width=3)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dcc.Graph(id='project_pie', figure=proj_pie)
                    ], color='light')
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dcc.Graph(id='field_o_work', figure=fldow_pie)
                ], color='light')
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dcc.Graph(id='sec_pie', figure=sec_pie)
                ], color='light')
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dcc.Graph(id='daila_pie', figure=daila_pie)
                ], color='light')
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dcc.Graph(id='project_bar', figure=proj_bar)
                ], color='light')
            ], width=12)
        ])]

    # layout = dash_app.layout 
    layout = html.Div(dbc.Container(rows))

    return render_template('dashboard.html',)



if __name__ == '__main__':
    app.run(debug=True)
