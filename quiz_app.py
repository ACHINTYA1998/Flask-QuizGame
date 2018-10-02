from flask import Flask, render_template,request,url_for,redirect,session
import requests
import random
import base64
import json
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
	return render_template('homepage.html')

@app.route('/categories')
def showcategories():
	url = 'https://opentdb.com/api_category.php'
	resp = requests.get(url)
	dicttdata = json.loads(resp.text) #Returns a dictionary with key of string and a value of a list of
	#dictionaries, which have 2 items: an id and name
	categories =[] #Store category name AND id to be able to request API for a particular quiz type
	for item in dicttdata['trivia_categories']:
		categories.append((item['id'],item['name']))
	return render_template('selectquiz.html',data=categories)

'''@app.route('/form',methods=['GET','POST'])
def quizform(quizid=None):
	qid = quizid 
	if request.method=='GET':
		return render_template('questionform.html',val=qid)
	elif request.method=='POST':
		level = request.form['level']
		qtype = request.form['qtype']
		qid = request.form['id']	
	return 'Data returned to page: {},{},{}'.format(qid,level,qtype)
		#'Data submitted to the page via form: {},{},{}'.format(qid,level,qtype)
'''

@app.route('/quiz1')
def sample_quiz():
	session.pop('ques',None) #Remove the questions list object if exists in session
	args = {'amount':10,'difficulty':'medium','type':'multiple'}
	resp = requests.get('https://opentdb.com/api.php',params = args)
	#ans = resp.status_code
	data = json.loads(resp.text)
	#print(data)
	questions = [] #A list of dictionaries, one for each question
	if data['response_code'] == 1:
		return 'There are not enough questions satisfying the criteria you set. Please choose again'
	else:
		for question in data['results']:
			questions.append({'question':question['question'],'correct':question['correct_answer']})
			answers = [question['correct_answer']] + question['incorrect_answers']
			random.shuffle(answers)
			questions[-1]['answers'] = answers
		session['ques'] = questions 
		return render_template('questions.html',questions=questions)


@app.route('/quiz',methods=['GET','POST'])
def makequiz():
	if request.method=='GET':
		return redirect(url_for('home'))
	if request.method=='POST':
		args = {'amount':10,'type':'multiple'}
		args['difficulty'] = request.form['difficulty']
		args['category'] = int(request.form['category'])
		resp = requests.get('https://opentdb.com/api.php',params = args)
		data = json.loads(resp.text)
	#print(data)
	questions = [] #A list of dictionaries, one for each question
	if data['response_code'] == 1:
		return 'There are not enough questions satisfying the criteria you set. Please choose again'
	else:
		for question in data['results']:
			questions.append({'question':question['question'],'correct':question['correct_answer']})
			answers = [question['correct_answer']] + question['incorrect_answers']
			random.shuffle(answers)
			questions[-1]['answers'] = answers
		session['ques'] = questions 
		return render_template('questions.html',questions=questions)



@app.route('/result',methods=['GET','POST'])
def result():
	data = session['ques']
	user_answers = request.form
	correct_answers = [i['correct'] for i in data]
	user_resp = [i[1] for i in user_answers.items()]
	score = sum(x in correct_answers for x in user_resp)
	print(type(data))
	return 'Your score is {}!' .format(score)


if __name__=='__main__':
	app.run(debug=True,port=6453)
