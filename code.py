#!/usr/bin/env python
import web
import datetime
import csv 
import matplotlib.pyplot as plt
import mpld3
import pandas as pd
"""
TODO major:For the check class, use mpld3 to visualize the progress
"""


urls = (
    '/','formpage',
    '/update','update',
)
app = web.application(urls,globals())
render = web.template.render('templates/') #searches for files to render in templates
 
def csvToDict():
    with open('log.csv') as filename:
        reader  = csv.reader(filename,delimiter=',') #fieldnames=['Date','GPA'] 
	display = [{row[0]:row[1]} for row in reader]
        print display
        return display
def clearCsv():
    f = open('log.csv','w+') #truncate the file
    f.close()

class formpage:
    def __init__(self):
        self.simpleForm = web.form.Form(
            web.form.Radio('options',['Check your current progress','Update your score log','Clear your score log']),
            web.form.Button('Submit')    
        ) #initializing a form with these attributes
 
    def GET(self):                
        return render.index(self.simpleForm,None)
 
    def POST(self):
        formInput = web.input()
        if formInput.options == 'Update':
            return render.updateForm(7,update().grades.keys())  
	#write classes for these later
	elif formInput.options == 'Check':
	    return check().form
	elif formInput.options == 'Clear':
	    clearCsv()
            return """<p>Progress log was cleared successfully</p> <p> <a href="/"> Return to main page</a>"""
	else: 
            return render.index(self.simpleForm,'Please choose an option')
class update:
    def __init__(self):
        self.grades = {'A*':4.3,'A':4.0,'B':3.0,'C':2.0,'D':1.0,'F':0.0}
	self.n = 7 #number of subjects
	self.table = dict()  
    
    #calculates and returns gpa based on a list of letter grades
    def calculate(self,scores):
        gpa = round(sum([self.grades[x] for x in scores])/self.n, 2) #round to the second precision point
	return gpa

    #adds result to csv
    def add(self,entry):
        with open('log.csv','a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([entry[0],entry[1]])
    def POST(self):
        data = web.input(score=[])
	scores = data.score #gets the array of scores
	if '' in scores:
            return render.updateForm(7,self.grades.keys(),"Please fill in all fields")
	else:
            count=0
	    for score in scores:
	        if score not in self.grades.keys():
		    count +=1
	    if count>0:
	        return render.updateForm(7,self.grades.keys(),'One or more of the scores were invalid letter grades')
	    else:
	        gpa = self.calculate(scores)
		date = datetime.date.today() #the date on which it is accessed
		self.add([date,gpa]) #add log as date,gpa pair
		display = csvToDict() #create dict to display as a table of results
		return render.results(gpa,display,'Your updated Progress table is:',None)
class check:
    def __init__(self):
        self.display =  csvToDict()
        self.form = render.results(None,self.display,'Your progress table is:',None) 
    """def logToGraph(self):
        df = pd.DataFrame({'2015-05-16':[3.94],'2015-06-16':[4.00]})
	print df
        fig = mpld3.fig_to_html(df.plot())
        return fig"""
        
if __name__=='__main__':
    app.run()
