from flask import Flask,request,render_template,redirect,session,url_for
import sqlite3

app = Flask(__name__)

app.secret_key = 'your_secret_key'
user_accounts = {
    'arun': '123'
}

con = sqlite3.connect("user.db", timeout=10, check_same_thread=False) ##############

con.execute("create table if not exists mydata(id integer primary key autoincrement,name text,username text unique,mailid text unique, mobile_no integer,password text)")
cur = con.cursor() ###############

 # Login and Signup page
    
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":  
        global luname
        luname = request.form['luname'] 
        lpass = request.form['lpass']
        cur.execute("select * from mydata order by username asc")
        a = cur.fetchall()
        for i in a:
            if luname == i[2]:
                if lpass == i[5]:         
                    return redirect("/home")
                else:
                    return render_template("login.html", message="Invalid password")
        else:
            return render_template("login.html", message="Invalid Username or Password")
    else:
        return render_template("login.html")
    
@app.route("/" or "/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"] 
        username = request.form["u_name"]
        emailid = request.form["mailid"]
        mobile_no = request.form["m_no"]
        password = request.form["pass"]
        confirm_password = request.form["c_pass"]
        if password == confirm_password:
            cur.execute("select mailid from mydata")
            mail_id = cur.fetchall()
            cur.execute("select username from mydata")
            user_name = cur.fetchall()
            if tuple(username) not in user_name:
                if tuple(emailid) not in mail_id:
                    con.execute("insert into mydata (name,username,mailid,mobile_no,password) values (?,?,?,?,?) ",(name,username,emailid,mobile_no,password))
                    con.commit()
                    return redirect("/login")
                else:
                    return render_template("signup.html", email_in_use = True)
            else:
                return render_template("signup.html", username_in_use = True)
        else:
            return render_template("signup.html")
    return render_template("signup.html")

@app.route("/forget", methods=["GET", "POST"])
def forget():
    if request.method == "POST":
        import random
        global otp,email_id

        otp = str(random.randint(10000,99999))
        email_id = request.form['emailid']

        import smtplib
        sender_email = "arunkumarkp9697@gmail.com"
        password = "axipmejcqnluiwgt"
        to_email = email_id
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email,to_email,otp)
        server.quit()
        return render_template("otp.html",to_email = to_email)
    
    else:
        return render_template("forget.html")
    
@app.route("/send_otp",methods = ["GET","POST"])
def send_otp():
    if request.method == "POST":
        u_otp = request.form["otp"]
        if u_otp == otp:
            global details
            cur.execute("select * from mydata where mailid = ?",(email_id,))
            details = cur.fetchone()
            if details:
                return render_template("show_profile.html",d_name = details[1], d_username = details[2], d_mailid = details[3], d_mobile_no = details[4], d_password = details[5])
            else:
                 return render_template("forget.html", message = "This email was not login in this site. Please try with a login emailid!")
        else:
            return render_template("otp.html", message = "Invalid OTP! PLease check and enter correct OTP")
    else:
        return render_template("otp.html")
    
@app.route("/update_profile",methods=["GET","POST"])
def update_profile():
    if request.method == "POST":
        name = request.form['lname']
        username = request.form['luname']
        emailid = request.form['lemail']
        mobile_no = request.form['lmobile']
        password = request.form['lpass']
        con.execute("update mydata set name=?, username=?, mailid=?, mobile_no=?, password=? where mailid = ?",(name,username,emailid,mobile_no,password,emailid))
        con.commit()
        return redirect("login")
    else:
        return render_template("update_profile.html", d_name = details[1], d_username = details[2], d_mailid = details[3], d_mobile_no = details[4], d_password = details[5])
    
@app.route("/login_for_admin",methods=["GET","POST"])
def login_for_admin():
    if request.method == "POST":
        username = request.form['luname']
        password = request.form['lpass']
        if username in user_accounts and user_accounts[username] == password:
            session['username'] = username
            return redirect(url_for('rooms_admin'))
        else:
            return render_template("login_for_admin.html",message="invalid username or password")
    else:
        return render_template("login_for_admin.html")

@app.route('/logout_for_admin')
def logout_for_admin():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route("/logout_user")
def logout_user():
    return render_template("login.html")

 # User page

@app.route("/home")
def home():
    cur.execute("select * from hostel order by room_no asc")
    details = cur.fetchall()
    return render_template("home.html",details=details)

@app.route("/rooms")
def rooms():
    cur.execute("select * from hostel")
    details = cur.fetchall()
    return render_template("rooms.html",details=details)

@app.route("/contact")
def contact():
    cur.execute("select * from contact where id=1")
    details = cur.fetchall()
    return render_template("contact.html",details=details)

@app.route("/your_profile",methods=["GET","POST"])
def your_profile():
    if request.method == "POST":
        cur.execute("select * from mydata where username = ?",(luname,))
        details = cur.fetchone()
        return render_template("update_profile_2.html", d_name = details[1], d_username = details[2], d_mailid = details[3], d_mobile_no = details[4], d_password = details[5])
    else:
        cur.execute("select * from mydata where username = ?",(luname,))
        details = cur.fetchone()
        return render_template("your_profile.html",d_name = details[1], d_username = details[2], d_mailid = details[3], d_mobile_no = details[4], d_password = details[5])

@app.route("/update_profile_2",methods=["GET","POST"])
def update_profile_2():
    if request.method == "POST":
        name = request.form['lname']
        username = request.form['luname']
        emailid = request.form['lemail']
        mobile_no = request.form['lmobile']
        password = request.form['lpass']
        con.execute("update mydata set name=?, username=?, mailid=?, mobile_no=?, password=? where mailid = ?",(name,username,emailid,mobile_no,password,emailid))
        con.commit()
        global luname
        luname = username
        return redirect("/your_profile")
    else:
        return redirect("/your_profile")

 # Admin page

con.execute("create table if not exists hostel (id integer primary key autoincrement, Room_no integer, Bet_no integer, Berth_or_not text, Rent_per_Month integer, Available_or_not text)")
cur = con.cursor()

@app.route("/rooms_admin",methods=["GET","POST"])
def rooms_admin():
    if 'username' in session:
        if request.method == "POST":
            Room_no = request.form['Room no']
            Bed_no = request.form['Bed no']
            Berth_or_Not = request.form['Berth or Not']
            Rent_per_Month = request.form['Rent per Month']
            Available_or_Not = request.form['Available or Not']
            con.execute("insert into hostel(Room_no, Bet_no, Berth_or_not, Rent_per_Month, Available_or_not) values (?,?,?,?,?)",(Room_no, Bed_no, Berth_or_Not, Rent_per_Month, Available_or_Not))
            con.commit()
            return redirect("/rooms_admin")
        elif request.method == "GET":
            cur.execute("select * from hostel order by room_no asc,bet_no asc")
            details = cur.fetchall()
            return render_template ("rooms_admin.html",details=details)
    else:
        return redirect(url_for('login_for_admin'))
    
@app.route("/update_room_1/<int:id>",methods=["POST"])
def update_room_1(id):
    if request.method == "POST":
        id = id
        cur.execute("select * from hostel where id=?",(id,))
        detail = cur.fetchall()
        return render_template("update_room.html",detail=detail)
    
@app.route("/update_room_2",methods=["POST"])
def update_room_2():
    if request.method == "POST":
        id = request.form['id']
        Room_no = request.form['room_no']
        Bed_no = request.form['bed_no']
        Berth_or_Not = request.form['berth_or_not']
        Rent_per_Month = request.form['rent_per_month']
        Available_or_Not = request.form['available_or_not']
        con.execute("update hostel set Room_no=?, Bet_no=?, Berth_or_not=?, Rent_per_Month=?, Available_or_not=? where id=?",(Room_no, Bed_no, Berth_or_Not, Rent_per_Month, Available_or_Not, id))
        con.commit()
        return redirect('/rooms_admin')
    
@app.route("/delete_row/<int:id>",methods=["POST"])
def delete_row(id):
    if request.method == "POST":
        id = id
        con.execute("delete from hostel where id=?",(id,))
        con.commit()
        return redirect("/rooms_admin")
    
@app.route("/click_button/<int:id>",methods=["GET","POST"])
def click_button(id):
    if request.method == "POST":
        id = id
        cur.execute("select Room_no,Bet_no from hostel where id=?",(id,))
        a = cur.fetchall()
        room_no = a[0][0]
        bed_no = a[0][1]
        cur.execute("select * from hostelers where room_no=? and bed_no=?",(room_no,bed_no))
        detail = cur.fetchone()
        print(detail)
        return render_template('click_button.html',detail=detail)
    else:
        return redirect("/rooms_admin")
    
con.execute("create table if not exists hostelers(id integer primary key autoincrement,room_no integer,bed_no integer,name text,adhaar_no number,mobile_no number,rent integer,paid_or_not text)")
con.commit()

@app.route("/hostelers_admin",methods=["GET","POST"])
def hostelers_admin():
    if request.method == "POST":
        room_no = request.form['room_no']
        bed_no = request.form['bed_no']
        name = request.form['name']
        adhaar_no = request.form['adhaar_no']
        mobile_no = request.form['mobile_no']
        rent = request.form['rent']
        paid_or_not = request.form['paid_or_not']
        cur.execute("insert into hostelers (room_no,bed_no,name,adhaar_no,mobile_no,rent,paid_or_not) values(?,?,?,?,?,?,?)",(room_no,bed_no,name,adhaar_no,mobile_no,rent,paid_or_not))
        con.commit()
        return redirect("/hostelers_admin")
    else:
        cur.execute("select * from hostelers order by room_no asc,bed_no asc")
        details = cur.fetchall()
        return render_template ("hostelers_admin.html",details=details)
    
@app.route("/update_hosteler_1/<int:id>",methods=["POST"])
def update_hosteler_1(id):
    id = id
    cur.execute("select * from hostelers where id=?",(id,))
    detail = cur.fetchall()
    return render_template("update_hosteler.html",detail=detail[0])

@app.route("/update_hosteler_2/<int:id>",methods=["POST"])
def update_hosteler_2(id):
    if request.method == "POST":
        id = id
        room_no = request.form['room_no']
        bed_no = request.form['bed_no']
        name = request.form['name']
        adhaar_no = request.form['adhaar_no']
        mobile_no = request.form['mobile_no']
        rent = request.form['rent']
        paid_or_not = request.form['paid_or_not']
        cur.execute("update hostelers set room_no=?,bed_no=?,name=?,adhaar_no=?,mobile_no=?,rent=?,paid_or_not=? where id=?",(room_no,bed_no,name,adhaar_no,mobile_no,rent,paid_or_not,id))
        con.commit()
        return redirect("/hostelers_admin")

@app.route("/delete_hosteler/<int:id>",methods=["GET","POST"])
def delete_hosteler(id):    
    if request.method == "POST":
        id = id
        print(id)
        con.execute("delete from hostelers where id = ?",(id,))
        con.commit()
        return redirect('/hostelers_admin')
        
con.execute("create table if not exists contact(id integer primary key autoincrement,staff text, name text, mobile_no integer, email_id text)")
con.commit()

@app.route("/contact_admin_1",methods=["GET","POST"])
def contact_admin_1():
    if request.method == "POST":
        cur.execute("select * from contact where id=1")
        detail = cur.fetchall()
        return render_template("update_contact.html",detail=detail[0])
    else:
        cur.execute("select * from contact where id=1")
        detail = cur.fetchall()
        return render_template("contact_admin.html",detail=detail[0])

@app.route("/contact_admin_2",methods=["POST"])
def contact_admin_2():
    if request.method == "POST":
        staff = request.form['staff']
        name = request.form['name']
        mobile_no = request.form['mobile_no']
        email_id = request.form['email_id']
        con.execute("update contact set staff=?, name=?, mobile_no=?, email_id=? where id=1",(staff,name,mobile_no,email_id))
        con.commit()
        return redirect("/contact_admin_1")

@app.route("/rent_admin")
def rent_admin():
    cur.execute("select * from hostelers")
    details = cur.fetchall()
    return render_template ("rent_admin.html",details=details)

if __name__ == '__main__':
    app.run(debug=True)