from flask import Flask,render_template,request,session,redirect,url_for
import sqlite3 as sql

app=Flask(__name__)

app.secret_key="ajay"

 
@app.route('/')
def home():
    conn=sql.connect("youtube.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("Select * from display where name=?",(session["username"],))
    data=cur.fetchall()
    return render_template("index.html",thumbnaillist1=data)


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        conn=sql.connect("youtube.db")
        conn.row_factory=sql.Row
        cur=conn.cursor()
        cur.execute("Select * from login where name=?",(name,))
        data=cur.fetchone()
        if data:
            if str(data["name"])==name and str(data["email"])==email and str(data["password"])==password:
                session["username"]= data["name"]
                # session["username"]=mobile
                # return "Login as"+" "+session["username"]
              
        return redirect(url_for('home'))     
    return render_template("login.html")

@app.route("/add_user",methods=["POST","GET"])
def add_user():
   if request.method=="POST":
      name=request.form.get("name")
      email=request.form.get("email")
      password=request.form.get("password")
      conn=sql.connect("youtube.db")
      conn.row_factory=sql.Row
      cur=conn.cursor()
      cur.execute("Insert into login(name,email,password) values(?,?,?)",(name,email,password))
      conn.commit()
      return redirect(url_for('home'))
   return render_template("add_user.html")

@app.route("/logout")
def logout():
    session.pop("username",None)
    return redirect(url_for("login"))
    


    

if __name__=="__main__":
    app.run(debug=True)


