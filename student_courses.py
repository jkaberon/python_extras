from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from tkinter import *
import smtplib

window=Tk()
window.wm_title('Find Me a Course')

lab1=Label(window,text="Subject")
lab1.grid(row=0,column=0)

lab2=Label(window,text="Course")
lab2.grid(row=1,column=0)

lab3=Label(window,text="Sections")
lab3.grid(row=2,column=0)

lab4=Label(window,text="NetID")
lab4.grid(row=0,column=2)

lab5=Label(window,text="Password")
lab5.grid(row=1,column=2)

lab6=Label(window,text="Email")
lab6.grid(row=3,column=2)

lab7=Label(window,text="Password")
lab7.grid(row=4,column=2)

lab8=Label(window,text="Phone")
lab8.grid(row=5,column=2)

e1_val=StringVar()
e1=Entry(window,textvariable=e1_val)
e1.grid(row=0,column=1)

e2_val=StringVar()
e2=Entry(window,textvariable=e2_val)
e2.grid(row=1,column=1)

e3_val=StringVar()
e3=Entry(window,textvariable=e3_val)
e3.grid(row=2,column=1)

e4_val=StringVar()
e4=Entry(window,textvariable=e4_val)
e4.grid(row=0,column=3)

e5_val=StringVar()
e5=Entry(window,show='*',textvariable=e5_val)
e5.grid(row=1,column=3)

e6_val=StringVar()
e6=Entry(window,textvariable=e6_val)
e6.grid(row=3,column=3)

e7_val=StringVar()
e7=Entry(window,show='*',textvariable=e7_val)
e7.grid(row=4,column=3)

e8_val=StringVar()
e8=Entry(window,textvariable=e8_val)
e8.grid(row=5,column=3)

def everything():
	url="https://apps.uillinois.edu/selfservice/"
	subject=e1_val.get()
	course=e2_val.get()
	sections=[s.strip() for s in e3_val.get().split(',')]
	netID=e4_val.get()
	password=e5_val.get()
	email=e6_val.get()
	Epassword=e7_val.get()
	phone=e8_val.get()
	
	browser=webdriver.Chrome()
	browser.get(url)
	link1=browser.find_element_by_link_text("University of Illinois at Urbana-Champaign (URBANA)")
	link1.click()
	box=browser.find_element_by_id("netid")
	box.send_keys(netID)
	browser.find_element_by_id("easpass").send_keys(password)
	browser.find_element_by_name("BTN_LOGIN").click()
	browser.find_element_by_link_text("Registration & Records").click()
	browser.find_element_by_link_text("Classic Registration").click()
	browser.find_element_by_link_text("Look-up or Select Classes").click()
	browser.find_element_by_partial_link_text("I Agree").click()
	browser.find_elements_by_tag_name("option")[1].click()
	browser.find_element_by_xpath("/html/body/div[3]/form/input[2]").click()
	browser.find_element_by_xpath("//*[@value='%s']" %subject).click()
	browser.find_element_by_xpath("/html/body/div[3]/form/input[17]").click()
	
	result=None

	while True:
		if result is None:
			body=browser.find_element_by_xpath("/html/body/div[3]/table[2]/tbody")
			choices=body.find_elements_by_tag_name("tr")
			result=binary_search(choices,course,2,len(choices)-1)
		else:
			body=browser.find_element_by_xpath("/html/body/div[3]/table[2]/tbody")
			choices=body.find_elements_by_tag_name("tr")
		
		choices[result].find_element_by_name("SUB_BTN").click() 
		bod=browser.find_element_by_xpath("/html/body/div[3]/form/table/tbody")
		rows=bod.find_elements_by_tag_name("tr")
		finished=True #False if course has openings
		
		for s in sections:
			res=b_search_2(rows,s,2,len(rows)-1)
			elem=rows[res].find_element_by_tag_name("td")
			try:
				elem.find_element_by_tag_name("input")
			except NoSuchElementException:
				continue
			finished=False
			break
		
		if not finished:
			server=smtplib.SMTP("smtp.gmail.com",587)
			server.starttls()
			server.login(email,Epassword)
			server.sendmail(email,"%s@vtext.com" % phone,"Spot is open!")
			server.quit()
			break
		time.sleep(30)
		browser.back()

def binary_search(c,course,start,end):
    if start>end:
        return "course doesn't exist"
    mid=int((start+end)/2)
    elem=c[mid].find_element_by_tag_name("td")
    num=elem.get_attribute('innerHTML')
    
    if num == course:
        return mid
    elif int(num)<int(course):
        return binary_search(c,course,mid+1,end)
    else:
        return binary_search(c,course,start,mid-1)

def b_search_2(c,section,start,end):
    if start>end:
        return "section doesn't exist"
    mid=int((start+end)/2)
    elem=c[mid].find_elements_by_tag_name("td")[4]
    sec=elem.get_attribute('innerHTML')
    if sec == "&nbsp;":
        elem=c[mid-1].find_elements_by_tag_name("td")[4]
        sec=elem.get_attribute('innerHTML')
		
    if sec==section:
        return mid
    elif sec<section:
        return b_search_2(c,section,mid+1,end)
    else:
        return b_search_2(c,section,start,mid-1)

b1=Button(window,text="Go",command=everything)
b1.grid(row=4,column=1)
    
window.mainloop()