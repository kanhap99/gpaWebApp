#!/usr/bin/env python
import web
import datetime
import csv 
"""
Have used a static csv to store progress values
TODO major:For the check class, use mpld3 to visualize the progress
"""


urls = (
    '/','formpage',
    '/update','update',
)
app = web.application(urls,globals())
render = web.template.render('templates/') #searches for files to render in templates
 
def csvToDict():
    with open('log.csv','r') as filename:
        reader  = csv.reader(filename,delimiter=',') #fieldnames=['Date','GPA'] 
        display = dict()
	for row in reader:
            display[row[0]] = row[1]
        print display
        return display
def clearCsv():
    f = open('log.csv','w+') #truncate the file
    f.close()

class formpage:
    def __init__(self):
        self.simpleForm = web.form.Form(
            web.form.Radio('options',['Check your current progress','Update your score log','Clear your score log']),
            web.form.Button('submit')    
        ) #initializing a form with these attributes
 
    def GET(self):                
        return render.index(self.simpleForm)
 
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
	print scores
	if '' in scores:
            return render.updateForm(7,self.grades.keys(),"Please fill in all fields")
	else:
            count=0
	    for score in scores:
	        if score not in self.grades.keys():
		    count +=1
	    if count>0:
	        return render.updateForm(7,self.grades.keys(),'One or more of the scores were invalid')
	    else:
	        gpa = self.calculate(scores)
		date = datetime.date.today() #the date on which it is accessed
		self.add([date,gpa]) #add log as date,gpa pair
		display = csvToDict() #create dict to display as a table of results
		return render.results(gpa,display,'Your updated Progress table is:')
class check:
    def __init__(self):
        self.display =  csvToDict()
        self.form = render.results(None,self.display,'Your progress table is:')     
if __name__=='__main__':
    app.run()
