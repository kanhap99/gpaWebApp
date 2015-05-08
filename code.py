#!/usr/bin/env python
import web

"""
TODO:Validate the update form and give the appropriate messages
TODO:Learn sql databsing or figure out if you need one, if you don't just use a csv stored to the server
TODO:Once done with the sql, use it to write the Check and Clear classes
TODO:For the check class, use mpld3

"""


urls = (
    '/','formpage',
    '/index','formpage',
    '/update','update',
)
app = web.application(urls,globals())
render = web.template.render('templates/') #searches for files to render in templates
 
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
	    pass 
	elif formInput.options == 'Clear':
	    return formInput
class update:
    def __init__(self):
        self.grades = {'A*':4.3,'A':4.0,'B':3.0,'C':2.0,'D':1.0,'F':0.0}
	self.n = 7 #number of subjects 

    def calculate(self,scores):
        gpa = round(sum([self.grades[x] for x in scores])/self.n, 2) #round to the second precision point
	return gpa

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
                return render.results(gpa)  
if __name__=='__main__':
    app.run()
