from flask import *

import pymysql

app = Flask(__name__)
# secret key
app.secret_key ='AW_r%@jN*HU4AW_r%@jN*HU4AW_r%@jN*HU4'

@app.route('/') 
def home():
    # connect database
    connection = pymysql.connect(host='localhost',user='root',password='',database='oryxdb')

    # create cursor which runs the sql query
    cursor = connection.cursor()

    # prepare the query
    smartphonesql = "select * from products where product_category = 'Smartphones'"
    # execute the query
    cursor.execute(smartphonesql)
    smartphones= cursor.fetchall()

    # sql query
    electronic_sql = "select * from products where product_category = 'Electronics'"        
    # execute the query
    cursor.execute(electronic_sql)
    # fetch the rows
    electronics = cursor.fetchall()

    # prepare the query
    appliancessql = "select * from products where product_category = 'Appliances'"
    # execute the query
    cursor.execute(appliancessql)
    appliances= cursor.fetchall()


        # render to front-end
    return render_template('home.html', smartphones=smartphones,electronics=electronics,appliances=appliances)

@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method =='POST':
        product_name = request.form['product_name']
        product_desc = request.form['product_desc']
        product_cost = request.form['product_cost']
        product_category = request.form['product_category']
        product_image_name = request.files['product_image_name']
        product_image_name.save('static/images/' + product_image_name.filename)

        # connect database
        connection = pymysql.connect(host='localhost',user='root',password='',database='oryxdb')

        # create cursor which runs the sql query
        cursor = connection.cursor()

        # prepare the data 
        data =(product_name,product_desc,product_cost,product_category,product_image_name.filename)

        # sql query
        sql = 'insert into products(product_name,product_desc,product_cost,product_category,product_image_name) VALUES (%s,%s,%s,%s,%s)'

        cursor.execute(sql,data)

        connection.commit()

        return render_template('upload.html', message='product added successfully')
    else:
        return render_template('upload.html')
    
@app.route('/single_item/<product_id>')
def single(product_id):
     # connect database
    connection = pymysql.connect(host='localhost',user='root',password='',database='oryxdb')

    # create cursor which runs the sql query
    cursor = connection.cursor()
    # sql query 
    product_sql ='select * from products where product_id =%s'
    # execute
    cursor.execute(product_sql,(product_id))
    # fetch 
    product = cursor.fetchone()
    return render_template('single.html',product=product)

# signup
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method =='POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password1 = request.form['password1']
        password2 = request.form['password2']
        # check password
        if len(password1)< 8:
            return render_template('signup.html', error='password must be more than 8 xters')
        elif password1 != password2 :
            return render_template('signup.html', error='Password do not match')
        else:
            # save the username , email, phone, password to the database
         # connect database
            connection = pymysql.connect(host='localhost',user='root',password='',database='oryxdb')

            # create cursor which runs the sql query
            cursor = connection.cursor()

            # prepare data 
            userdata =(username,password2,email,phone)
            # sql query 
            user_sql ='insert into users (username,password,email,phone) VALUES (%s,%s,%s,%s)'

            # execute the query
            cursor.execute(user_sql,(userdata))
            # commit
            connection.commit()
            # send sms
            import sms
            sms.send_sms(phone,'Thank you for Registering')
            # return message to user
            return render_template('signup.html', success='Registerd successfully')
    else:
        return render_template('signup.html')    

# sign in
@app.route('/signin', methods=['POST','GET'])
def signin():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        # connect database
        connection = pymysql.connect(host='localhost',user='root',password='',database='oryxdb')
        # create cursor which runs the sql query
        cursor = connection.cursor()
        # prepare data
        signindata = (username,password)
        # sql query
        signin_sql = 'select * from users where username = %s and password = %s'
        #execute
        cursor.execute(signin_sql,(signindata))
        # check
        if cursor.rowcount == 0 :
            return render_template('signin.html', error='Invalid Credentials')
        else:
            session['key'] = username #link key with the username
            return redirect('/')
    else:
        return render_template('signin.html')

# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/signin')
    
# payment
@app.route('/mpesa', methods=['POST'])
def mpesa():
    phone = request.form['phone']
    amount = request.form['amount']
    # import mpesa.py module
    import mpesa
    mpesa.stk_push(phone,amount)
    # show user message to complete payment in the phone
    return '<h3>Please Complete Payment in your phone and we will deliver in minutes</h3>'\
    '<a href="/">Back to products</a>'

if __name__ == '__main__':
    app.run(debug=True)