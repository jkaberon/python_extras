#Program to store name, elevation, latitude, longitude of volcanoes
#Functions: View all, search, add, update, delete

from tkinter import *
import sqlite3
import pandas

window=Tk()

lab1=Label(window,text="Name")
lab1.grid(row=0,column=0)

lab2=Label(window,text="Elevation")
lab2.grid(row=1,column=0)

lab3=Label(window,text="Latitude")
lab3.grid(row=0,column=2)

lab4=Label(window,text="Longitude")
lab4.grid(row=1,column=2)

e1_val=StringVar()
ent1=Entry(window,textvariable=e1_val)
ent1.grid(row=0,column=1)

e2_val=StringVar()
ent2=Entry(window,textvariable=e2_val)
ent2.grid(row=1,column=1)

e3_val=StringVar()
ent3=Entry(window,textvariable=e3_val)
ent3.grid(row=0,column=3)

e4_val=StringVar()
ent4=Entry(window,textvariable=e4_val)
ent4.grid(row=1,column=3)

def create_table():
    conn=sqlite3.connect("volcanoes.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS info(name TEXT,elevation INTEGER,latitude REAL,longitude REAL)")
    conn.commit()
    conn.close()

def view():
    conn=sqlite3.connect("volcanoes.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM info")
    rows=cur.fetchall()
    listb.delete(0,END)
    for row in rows:
        listb.insert(END,row)
    conn.close()

b1=Button(window,text="View all",command=view)
b1.grid(row=2,column=3)

def search():
    a,b,c,d=e1_val.get(), e2_val.get(), e3_val.get(), e4_val.get()
    conn=sqlite3.connect("volcanoes.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM info WHERE name=? OR elevation=? OR latitude=? OR longitude=?",(a,b,c,d))
    rows=cur.fetchall()
    listb.delete(0,END)
    for row in rows:
        listb.insert(END,row)
    conn.close()

b2=Button(window,text="Search entry",command=search)
b2.grid(row=3,column=3)

def add():
    a,b,c,d=e1_val.get(), e2_val.get(), e3_val.get(), e4_val.get()
    conn=sqlite3.connect("volcanoes.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO info VALUES(?,?,?,?)",(a,b,c,d))
    conn.commit()
    conn.close()

b3=Button(window,text="Add entry",command=add)
b3.grid(row=4,column=3)

def update():
    a,b,c,d=e2_val.get(), e3_val.get(), e4_val.get(), e1_val.get()
    conn=sqlite3.connect("volcanoes.db")
    cur=conn.cursor()
    cur.execute("UPDATE info SET elevation=?,latitude=?,longitude=? WHERE name=?",(a,b,c,d))
    conn.commit()
    conn.close()

b4=Button(window,text="Update",command=update)
b4.grid(row=5,column=3)

def delete():
    conn=sqlite3.connect("volcanoes.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM info WHERE name=?",(e1_val.get(),))
    conn.commit()
    conn.close()

b5=Button(window,text="Delete",command=delete)
b5.grid(row=6,column=3)

listb=Listbox(window,height=10,width=48)
listb.grid(row=2,column=0,rowspan=5,columnspan=2)

sb=Scrollbar(window)
sb.grid(row=2,column=2,rowspan=10)

listb.configure(yscrollcommand=sb.set)
sb.configure(command=listb.yview)

#create_table()
#initialize_table()

def initialize_table():
    df=pandas.read_csv("volcanoes.txt")
    lat=list(df["LAT"])
    lon=list(df["LON"])
    names=list(df["NAME"])
    elevs=list(df["ELEV"])
    conn=sqlite3.connect("volcanoes.db")
    cur=conn.cursor()
    for a,b,c,d in zip(names,elevs,lat,lon):
        cur.execute("INSERT INTO info VALUES(?,?,?,?)",(a,b,c,d))
    conn.commit()
    conn.close()


window.mainloop()
