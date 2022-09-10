from flask import *
import random
import requests
import pymysql


db = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "students"
    )

cursor = db.cursor()


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
  
    return render_template("login.html")


@app.route("/admn",methods=["POST"])
def admn():
   return redirect(url_for('teach'))

@app.route("/teach")
def teach():
    cursor.execute("select id,name,physics,chemistry,maths,((physics+chemistry+maths)/3) as percentage from results")
    data = cursor.fetchall()
    return render_template("teach.html",userdata=data)
       
 
@app.route("/elements")
def elements():
    return render_template("elements.html")

@app.route("/generic")
def generic():
    return render_template("generic.html")

@app.route("/games")
def games():
    return render_template("games.html")

@app.route("/rock")
def rock():
    
    return render_template("rock.html")



@app.route("/choice",methods=["POST"])
def choice():
    
    user_action = request.form.get("user_input")
    possible_actions = ["rock", "paper", "scissors"]
    computer_action = random.choice(possible_actions)

    if user_action == computer_action:
        message = "Both players selected {}. It's a tie!".format(user_action)
        return render_template("choice.html", data = message, row = user_action)
    elif user_action == "rock":
        if computer_action == "scissors":
            message = "Rock smashes scissors! You win!"
            return render_template("choice.html", data = message, row = user_action)
            
        else:
            message= "Paper covers rock! You lose."
            return render_template("choice.html", data = message, row = user_action)
    elif user_action == "paper":
        if computer_action == "rock":
            message = "Paper covers rock! You win!"
            return render_template("choice.html", data = message, row = user_action)
        else:
            message = "Scissors cuts paper! You lose."
            return render_template("choice.html", data = message, row = user_action)
    elif user_action == "scissors":
        if computer_action == "paper":
            message = "Scissors cuts paper! You win!"
            return render_template("choice.html", data = message, row = user_action)
        else:
            message = "Rock smashes scissors! You lose."
            return render_template("choice.html", data = message, row = user_action)
    if user_action not in possible_actions:
        message = "Please Enter Valid Words"
        return render_template("choice.html", data = message, row = user_action)
        
        
        
        
        
@app.route("/allusers")
def allusers():
    cursor.execute("select id,name,physics,chemistry,maths,((physics+chemistry+maths)/3) as percentage from results")
    data = cursor.fetchall()
    return render_template("allusers.html",userdata=data)


@app.route("/percentage")
def percentage():
    cursor.execute("select ((physics+chemistry+maths)/3) from results")
    data = cursor.fetchall()
    return render_template("allusers", userdata = data)

@app.route("/create",methods=["POST"])
def create():
    name = request.form.get('name')
    physics = request.form.get('physics')
    chemistry = request.form.get('chemistry')
    maths = request.form.get('maths')
    insq = "insert into results(name,physics,chemistry,maths) values ('{}','{}','{}','{}')".format(name,physics,chemistry,maths)
    try:
        cursor.execute(insq)
        db.commit()
        return redirect(url_for('allusers')) 
    except:
        db.rollback()
        return "Error in query"

@app.route("/delete")
def delete():    
    id = request.args.get('id')    
    delq = "delete from results where id={}".format(id)
    
    try:
        cursor.execute(delq)
        
        db.commit()
        return redirect(url_for('allusers')) 
    except:
        db.rollback()
        return "Error in query"

@app.route("/edit")
def edit():
    id = request.args.get('id')
    selq ="select * from results where id={}".format(id) 
    cursor.execute(selq)
    data = cursor.fetchone()
    return render_template("edit.html",row=data)

@app.route("/update",methods=["POST"])
def update():
    uname = request.form.get('uname')
    pwd = request.form.get('pwd')
    contact = request.form.get('contact')
    uid = request.form.get('uid')
    
    updq ="update results set name='{}',password='{}',contact='{}' where id={}".format(uname,pwd,contact,uid)
    try:
        cursor.execute(updq)
        db.commit()
        return redirect(url_for('allusers')) 
    except:
        db.rollback()
        return "Error in query"

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/getdata",methods=["POST"])
def getdata():
    id = request.form.get('id')
    selq = "select name,physics,chemistry,maths,((physics+chemistry+maths)/3) as percentage from results where id = {}".format(id)
    
    cursor.execute(selq)
    data = cursor.fetchall()
  
    return render_template("search.html",row=data)



   
    

   
   







if __name__=="__main__":
    app.run(debug=True)