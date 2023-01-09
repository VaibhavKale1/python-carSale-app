from flask import Flask, render_template, request, redirect
import pyodbc
import os

app = Flask(__name__, template_folder="./")

s = os.environ.get('DB_HOST', 'host')  # Your server name
d = os.environ.get('DB_NAME', 'hci-dbdemo')
u = os.environ.get('DB_USER', 'testuser') # Your login
p = os.environ.get('DB_PASS', 'pass')  # Your login password

cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + s + ';DATABASE=' + d + ';UID=' + u + ';PWD=' + p
conn = pyodbc.connect(cstr)


# one time initial setup..
try:
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE [dbo].[TblCars](
	[ID] [int] NOT NULL,
	[Name] [varchar](100) NULL,
	[Year] [int] NOT NULL,
	[Price] [float] NOT NULL);
	INSERT INTO TblCars VALUES (1, 'Toyota Camry', 2018, 2000)
    INSERT INTO TblCars VALUES (2, 'Honda Civic', 2019, 2200)
    INSERT INTO TblCars VALUES (3, 'Chevrolet Silverado', 2017, 1800)
    INSERT INTO TblCars VALUES (4, 'Ford F-150', 2020, 2500)
    INSERT INTO TblCars VALUES (5, 'Nissan Altima', 2021, 3000)
	''')
    conn.commit()
except pyodbc.ProgrammingError:
    print("db is already created")


@app.route("/")
def main():
    cars = []
    # conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.TblCars")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
    # conn.close()
    return render_template("carslist.html", cars = cars)


@app.route("/addcar", methods = ['GET','POST'])
def addcar():
    if request.method == 'GET':
        return render_template("addcar.html", car = {})
    if request.method == 'POST':
        id = int(request.form["id"])
        name = request.form["name"]
        year = int(request.form["year"])
        price = float(request.form["price"])
        # conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.TblCars (id, name, year, price) VALUES (?, ?, ?, ?)", id, name, year, price)
        conn.commit()
        # conn.close()
        return redirect('/')

@app.route('/updatecar/<int:id>',methods = ['GET','POST'])
def updatecar(id):
    cr = []
    # conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM dbo.TblCars WHERE id = ?", id)
        for row in cursor.fetchall():
            cr.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
        # conn.close()
        return render_template("addcar.html", car = cr[0])
    if request.method == 'POST':
        name = str(request.form["name"])
        year = int(request.form["year"])
        price = float(request.form["price"])
        cursor.execute("UPDATE dbo.TblCars SET name = ?, year = ?, price = ? WHERE id = ?", name, year, price, id)
        conn.commit()
        # conn.close()
        return redirect('/')

@app.route('/deletecar/<int:id>')
def deletecar(id):
    # conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.TblCars WHERE id = ?", id)
    conn.commit()
    # conn.close()
    return redirect('/')

if(__name__ == "__main__"):
    app.run()
    conn.close()