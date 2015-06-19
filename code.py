#!/usr/bin/env python
import web
import datetime
import csv 
import plotly.plotly as py
from plotly.graph_objs import *
from requests.exceptions import *
import collections
urls = (
    '/','formpage',
    '/update','update',
)

app = web.application(urls,globals())
render = web.template.render('templates/') #searches for files to render in templates
 
def csvToDict():
    with open('log.csv') as filename:
        reader  = csv.reader(filename) #fieldnames=['Date','GPA'] 
	return [{row[0]:float(row[1])} for row in reader] #storing it as a list of dictionaries will allow the user to update his gpa more than once in a day

def clearCsv():
    f = open('log.csv','w+') #truncate the file
    f.close()

def listToDict(l):
    return collections.OrderedDict(sorted({k:v for d in l for k,v in d.items()}.items()))

class formpage:
    def __init__(self):
        self.simpleForm = web.form.Form(
            web.form.Radio('options',['Check your current progress','Update your score log','Clear your score log']),
            web.form.Button('Submit')    
        )

    def GET(self):                
        return render.index(self.simpleForm,None)

    def POST(self):
        formInput = web.input()
        if formInput.options == 'Update':
            return render.updateForm(8,update().grades.keys())  
	elif formInput.options == 'Check':
	    try:
	        return check().form #form attribute of the check instance
	    except ConnectionError:   
		return render.internet() #simple template rendered when there is no internet connection
	elif formInput.options == 'Clear':
	    #show flash message code here for confirmation
	    clearCsv()
	    return '<p>Progress log was cleared successfully</p> </br></br> <a href="/"> Return to the main page </a>'
class update:
    def __init__(self):
        self.grades = {'A*':4.3,'A':4.0,'B':3.0,'C':2.0,'D':1.0,'F':0.0} 
	self.n = 8 #number of subjects
  
    def calculate(self,scores):
        gpa = round(sum([self.grades[x] for x in scores])/self.n, 2) #round to the second precision point
	return gpa

    def add(self,entry):
        with open('log.csv','a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([entry[0],entry[1]])

    def POST(self):
        data = web.input(score=[])
	scores = data.score #gets the array of scores
	gpa = self.calculate(scores)
	date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #the date on which it is accessed
	self.add([date,gpa]) #add log as date,gpa pair
	display = listToDict(csvToDict()) #create dict to display as a table of results
	return render.results(gpa,display,'Your updated Progress table is:',None)

class check:
    def __init__(self):
        self.display =  listToDict(csvToDict())
    	self.graph = self.plot_src(self.display)
	self.form = render.results(None,self.display,'Your progress table is:',self.graph+'.embed') 
    
    def plot_src(self,d): #returns the url of the graph as a string
	trace = dict(x=d.keys(),y=d.values()) #plotly dictionary differs from python dictionary
	data = [trace]
	layout = Layout(
	    xaxis = XAxis(
		showgrid=True,
		autorange=True
	    ),
	    yaxis=YAxis(
		showgrid=True,
		range=[2.0,4.3]
	    ),
	)        
	fig = Figure(data=data, layout=layout)
	URL = py.plot(fig, filename = 'basic-line',auto_open=False)
	return URL
        

if __name__=='__main__':
    app.run()
    
