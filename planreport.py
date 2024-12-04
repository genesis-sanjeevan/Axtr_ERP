from flask import *

app = Flask(__name__)

@app.route('/')
def planform():

    name = 'ADMIN'
    id = '10001'
    
    return render_template('planform_admin.html',Emp_Name = name, Emp_ID = id)

if __name__ == '__main__':
    app.run(debug=True, port=6878)