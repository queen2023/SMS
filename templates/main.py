from datetime import datetime, date
from pickletools import read_bytes1
from flask import Flask,request, render_template, redirect
import psycopg2
app = Flask(__name__)
conn = psycopg2 .connect(user="postgres", password="queen", host="localhost", port="5432", database="myduka")
cur =conn.cursor()


@app.route('/')
def hello_world():
    username = "queeny mutie"
    return render_template("index.html", name=username)

@app.route('/inventory', methods=["POST", "GET"])
def inventory():
    if request.method=="POST":
        name = request.form["name"]
        quantity = request.form["stock_quantity"]
        bp = request.form["buying_price"]
        sp = request.form["selling_price"]
        print(name)
        print(quantity)
        print(bp)
        print(sp)

        cur.execute("""insert into products(name,stock_quantity,buying_price,selling_price) values (%(name)s, %(quantity)s, %(bp)s, %(sp)s)""" , {"name":name, "quantity":quantity, "bp":bp, "sp":sp})
        return redirect('/inventory')
    else:
        cur.execute("select * from products")
        data = cur.fetchall()
        return render_template("inventories.html", data=data)

@app.route("/sales/<int:pid>", methods=["POST" , "GET"])
def view_sales(pid):
        
        cur.execute("select * from sales where pid = %s",[pid])
        sales = cur.fetchall()
        return render_template("sales.html", sales=sales)

@app.route("/make_sale", methods=["POST","GET"])
def make_sale():
    pid = request.form["product id"]
    purch = request.form['quantity']
    cur.execute("""select stock_quantity from products where id = %(pid)s""", {"pid":pid})
    stock_quantity = cur.fetchone()
    print(make_sale)
    if stock_quantity[0]<=0 :
        pass
        return redirect("/inventory")
    else:
     stock_quantity=int(stock_quantity[0])
     purch=int(purch)

     remaining_stock=stock_quantity-purch
     cur.execute("""update products set stock_quantity=%(remstock)s where id=%(pid)s""", {"remstock":remaining_stock, "pid":pid})
     cur.execute("""insert into sales (pid,quantity,created_at) values (%(pid)s, %(quantity)s, %(created_at)s)""", {"pid":pid, "quantity":purch, "created_at":date.today()})
     conn.commit()
     return redirect("/inventory")

@app.route("/dashboard", methods=["POST","GET"])
def dashboard():
    cur.execute("select count(id) from products")
    tproducts=cur.fetchone()
    print(tproducts)
    return render_template("dashboard.html", tproducts=tproducts[0])


     

        


if __name__=='__main__':
    app.run()