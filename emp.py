from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import matplotlib.pyplot as plt
from pymongo import *
from requests import *
import re 

mw = Tk()
mw.title("Employee Management System")
mw.geometry("1000x800+50+50")
mw.configure(bg="salmon")
f = ("Georgia", 20, "bold")

#add window

def f1():
	mw.withdraw()
	aw.deiconify()
def f2():
	aw.withdraw()
	mw.deiconify()

#view window

def f3():
	mw.withdraw()
	vw.deiconify()
	view_records()
	
def f4():
	vw.withdraw()
	mw.deiconify()

#update window
def f5():
	mw.withdraw()
	uw.deiconify()
def f6():
	uw.withdraw()
	mw.deiconify()

#delete employee window
def f7():
	mw.withdraw()
	dw.deiconify()
def f8():
	dw.withdraw()
	mw.deiconify()

def save():
	con = None
	try:
		con = MongoClient("localhost", 27017)
		db = con["employee24"]
		coll = db["employees"]
		eid = aw_ent_id.get()
		ename = aw_ent_name.get()
		esalary = aw_ent_salary.get()
		
		if eid == "":
			showerror("issue", "eid cannot be empty")
			return
		if eid.isalpha():
			showerror("issue", "eid cannot be text")
			return
		if eid.isspace():
			showerror("issue", "eid cannot contain space ")
			return

		try:
			eid = int(eid)
			if eid < 0:
				showerror("issue", "eid cannot be negative")
				return
			if eid < 1 or eid > 1000:
				showerror("issue", "id must be between 1 and 1000")
				return

		except Exception:
			showerror("issue", "invalid id")
			return

		if not esalary:
			showerror("issue", "salary cannot be empty")
			return
		

		if esalary.isspace():
			showerror("issue", "salary cannot contain space ")
			return


		if esalary.isalpha():
			showerror("issue", "salary cannot be text")
			return

		try:
			esalary = int(esalary)
			if esalary < 0:
				showerror("issue", "salary cannot be negative")
				return

			if esalary < 1000 or esalary > 100000:
				showerror("issue", "salary must be between 1000 and 100000")
				return

		except Exception:
			showerror("issue", "salary must be only numeric")
			return
	

		if not ename:
			showerror("issue", "name cannot be empty")
			return

		if ename.isdigit():
			showerror("issue", "name cannot be number")
			return

		if any(char == '-' for char in ename):
			showerror("issue", "name cannot be negative")
			return

		if not re.match(r"^[a-zA-Z\s]+$", ename):
			showerror("Error", "Name cannot contain special characters.")
			return

		if ename.isspace():
			showerror("issue", "name cannot contain sapces")
			return


		if len(ename) < 2 or len(ename) > 20:
			showerror("issue", "name length shud be  betn 2 and 20 char.")
			return
			

		info = {"_id":eid, "name":ename, "salary":esalary }
		coll.insert_one(info)
		showinfo("Succcess", "Record Created")
		aw_ent_id.delete(0, END)
		aw_ent_name.delete(0, END)
		aw_ent_salary.delete(0, END)
		aw_ent_id.focus()

	except Exception:
		showerror("issue", "values cannot be empty")
		return
	finally:
		if con is not None:
			con.close()

def clear_aw():
	aw_ent_id.delete(0, END)
	aw_ent_name.delete(0, END)
	aw_ent_salary.delete(0, END)
	aw_ent_id.focus()
	

def view_records():
	con = None
	try:
		con = MongoClient("localhost", 27017)
		db = con["employee24"]
		coll = db["employees"]
		data = coll.find()
		vw_st_data.delete(1.0, END)
		for d in data:
			vw_st_data.insert(END, f"eid = {d['_id']}, ename =  {d['name']}, esalary = {d['salary']}\n")
	except Exception as e:
		showerror("Issue", str(e))
	finally:
		if con is not None:
			con.close()

def update():
	con = None
	try:
		con = MongoClient("localhost", 27017)
		db = con["employee24"]
		coll = db["employees"]
		eid = uw_ent_id.get()
		ename = uw_ent_name.get()
		esalary = uw_ent_salary.get()
		
		if eid == "":
			showerror("issue", "eid cannot be empty")
			return
		if eid.isalpha():
			showerror("issue", "eid cannot be text")
			return
		if eid.isspace():
			showerror("issue", "eid cannot contain space ")
			return

		try:
			eid = int(eid)
			if eid < 0:
				showerror("issue", "eid cannot be negative")
				return
			if eid < 1 or eid > 1000:
				showerror("issue", "id must be between 1 and 1000")
				return

		except Exception:
			showerror("issue", "invalid id")
			return

		if esalary == "":
			showerror("issue", "salary cannot be empty")
			return

		if esalary.isspace():
			showerror("issue", "salary cannot contain space ")
			return

		if esalary.isalpha():
			showerror("issue", "salary cannot be text")
			return

		try:
			esalary = int(esalary)
			if esalary < 0:
				showerror("issue", "salary cannot be negative")
				return
			if esalary < 1000 or esalary > 100000:
				showerror("issue", "salary must be between 1000 and 100000")
				return

		except Exception:
			showerror("issue", "salary must be a numeric")
			return

		if not ename:
			showerror("issue", "name cannot be empty")
			return

		if ename.isdigit():
			showerror("issue", "name cannot be number")
			return

		if any(char == '-' for char in ename):
			showerror("issue", "name cannot be negative")
			return

		if not re.match(r"^[a-zA-Z\s]+$", ename):
			showerror("Error", "Name cannot contain special characters.")
			return

		if ename.isspace():
			showerror("issue", "name cannot contain sapces")
			return


		if len(ename) < 2 or len(ename) > 20:
			showerror("issue", "name length shud be  betn 2 and 20 char.")
			return


		if coll.find_one({"_id":eid}):
			coll.update_one({"_id":eid}, {"$set": {"name":ename, "salary":esalary}})
			showinfo("success", "record updated")
			uw_ent_id.delete(0, END)
			uw_ent_name.delete(0, END)
			uw_ent_salary.delete(0, END)
			uw_ent_id.focus()
		else:
			showinfo("issue", "record does not exists")
	except Exception as e:
		showerror("issue", e)
	finally:
		if con is not None:
			con.close()
def clear_uw():
	uw_ent_id.delete(0, END)
	uw_ent_name.delete(0, END)
	uw_ent_salary.delete(0, END)
	uw_ent_id.focus()


def delete():
	con = None
	try:
		con = MongoClient("localhost", 27017)
		db = con["employee24"]
		coll = db["employees"]

		eid = dw_ent_id.get()
		if eid == "":
			showerror("error", "please enter id ")
			return

		if not eid.isdigit():
			showerror("issue", "invalid order id")
			return

		eid = int(eid)
		if coll.find_one({"_id": eid}):
			coll.delete_one({"_id": eid})
			showinfo("success", "record deleted successfully")
			dw_ent_id.delete(0, END)
			dw_ent_id.focus()
			
		else:
			showinfo("error", "record does not exist")
	except Exception:
			showerror("issue", "invalid id")
	finally:
		if con is not None:
			con.close()

	
def show():
	con = MongoClient("localhost", 27017)
	db = con["employee24"]
	coll = db["employees"]
	data = coll.find().sort("salary", -1).limit(5)
	enames = []
	esalaries = []
	for d in data:
		enames.append(d["name"])
		esalaries.append(d["salary"])

	plt.bar(enames, esalaries, color="blue", width=0.5)
	plt.xlabel("Employee Name")
	plt.ylabel("Salary")
	plt.title("Top5 Highest salaried Employees")
	
	plt.show()
	
def loc_temp():
	try:
		wa = "https://ipinfo.io/"
		res = get(wa)
		if res.status_code == 200:
			data = res.json()
			city_name = data['city']
			state_name = data['region']
			country_name = data['country']
			loc_msg = f"Location: {city_name}, {state_name}, {country_name}"
			mw_lab_loc.configure(text=loc_msg)

			api_key = "b65ff0940dfde6a3283d2d7ccfdd8a17"
			we = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
			responce = get(we)
			if res.status_code == 200:
				temp_data = responce.json()
				temp = temp_data['main']['temp']
				temp_msg = f"Temperature: {temp}\u00b0C"
				mw_lab_temp.configure(text=temp_msg)
			else:
				showerror("issue", "it failed to retrieve temperature data")
		else:
			showerror("issue", "failed to retrieve location")

	except Exception as e:
		showerror("issue", e)


mw_lab_title = Label(mw, text="Employee Management System", bg="salmon", font=f)
mw_lab_title.pack(pady=30)
mw_btn_add = Button(mw, text="Add Emp", width=10, bg="khaki", font=f, command=f1)
mw_btn_view = Button(mw, text="View Emp", width=10, bg="khaki", font=f, command=f3)
mw_btn_update = Button(mw, text="Update Emp", width=10, bg="khaki", font=f, command =f5)
mw_btn_delete = Button(mw, text="Delete Emp", width=10, bg="khaki", font=f, command=f7)
mw_btn_chart = Button(mw, text="Charts", width=10, bg="khaki", font=f, command=show)
mw_btn_add.pack(pady=10)
mw_btn_view.pack(pady=10)
mw_btn_update.pack(pady=10)
mw_btn_delete.pack(pady=10)
mw_btn_chart.pack(pady=10)

mw_lab_loc = Label(mw, text="", font=f, bg="salmon")
mw_lab_loc.pack(pady=40)
mw_lab_temp = Label(mw, text="", font=f, bg="salmon")
mw_lab_temp.pack(pady=5)
loc_temp()


#Add employee

aw = Toplevel(mw)
aw.title("Add Employee")
aw.geometry("1000x800+50+50")
aw.configure(bg="light blue")
f = ("Georgia", 24, "bold")

aw_lab_id = Label(aw, text="enter id:",bg="light blue",  font=f)
aw_ent_id = Entry(aw, font=f)
aw_lab_name = Label(aw, text="enter name:", bg="light blue", font=f)
aw_ent_name = Entry(aw, font=f)
aw_lab_salary = Label(aw, text="enter salary:", bg="light blue",  font=f)
aw_ent_salary = Entry(aw, font=f)
aw_lab_id.pack(pady=10)
aw_ent_id.pack(pady=10)
aw_lab_name.pack(pady=10)
aw_ent_name.pack(pady=10)
aw_lab_salary.pack(pady=10)
aw_ent_salary.pack(pady=10)

aw_btn_save = Button(aw, text="Save", width=10,bg="khaki", font=f, command=save)
aw_btn_clear = Button(aw, text="Clear", width=10, bg="khaki", font=f, command=clear_aw)
aw_btn_back = Button(aw, text="Back", width=10,  font=f, bg="khaki", command=f2)
aw_btn_save.pack(pady=10)
aw_btn_clear.pack(pady=10)
aw_btn_back.pack(pady=10)
aw.withdraw()

#view Employee

vw = Toplevel(mw)
vw.title("View Employee")
vw.geometry("1000x800+50+50")
vw.configure(bg="plum1")
f = ("Georgia", 24, "bold")

vw_st_data = ScrolledText(vw, width=40, height=10, bg="azure", font=("cambria", 20))
vw_btn_back = Button(vw, text="Back", font=f, width=10,  bg="khaki", command=f4)
vw_st_data.pack(pady=10)
vw_btn_back.pack(pady=10)
vw.withdraw()

#update Employee window

uw = Toplevel(mw)
uw.title("update Employee")
uw.geometry("1000x800+50+59")
uw.configure(bg="SeaGreen1")
f = ("Georgia", 24, "bold")

uw_lab_id = Label(uw, text="enter id:",bg="SeaGreen1",  font=f)
uw_ent_id = Entry(uw, font=f)
uw_lab_name = Label(uw, text="enter name:", bg="SeaGreen1", font=f)
uw_ent_name = Entry(uw, font=f)
uw_lab_salary = Label(uw, text="enter salary:", bg="SeaGreen1",  font=f)
uw_ent_salary = Entry(uw, font=f)
uw_lab_id.pack(pady=10)
uw_ent_id.pack(pady=10)
uw_lab_name.pack(pady=10)
uw_ent_name.pack(pady=10)
uw_lab_salary.pack(pady=10)
uw_ent_salary.pack(pady=10)

uw_btn_save = Button(uw, text="Save", width=10,bg="khaki", font=f, command=update)
uw_btn_clear = Button(uw, text="Clear", width=10, bg="khaki", font=f, command=clear_uw)
uw_btn_back = Button(uw, text="Back", width=10,  font=f, bg="khaki", command=f6)
uw_btn_save.pack(pady=10)
uw_btn_clear.pack(pady=10)
uw_btn_back.pack(pady=10)
uw.withdraw()

#delete employee window
dw = Toplevel(mw)
dw.title("Delete Employee")
dw.geometry("1000x800+50+59")
dw.configure(bg="aquamarine2")
f = ("Georgia", 24, "bold")

dw_lab_id = Label(dw, text="enter id:",bg="aquamarine2",  font=f)
dw_ent_id = Entry(dw, font=f)
dw_lab_id.pack(pady=10)
dw_ent_id.pack(pady=10)


dw_btn_delete = Button(dw, text="delete", width=10,bg="khaki", font=f, command=delete)
dw_btn_back = Button(dw, text="Back", width=10,  font=f, bg="khaki", command=f8)
dw_btn_delete.pack(pady=10)
dw_btn_back.pack(pady=10)
dw.withdraw()



mw.mainloop()