from flask import Blueprint, render_template, request
from pathlib import Path
import os
import string

from airtable import Airtable

from transformers import pipeline
from transformers import BertForQuestionAnswering, BertTokenizer

import threading

index_bp = Blueprint('index_bp', __name__,
	template_folder='templates',
	static_folder='static')

# NLP
model_dir = str(Path('index/bert').absolute())
model = BertForQuestionAnswering.from_pretrained(model_dir)
tokenizer = BertTokenizer.from_pretrained(model_dir)
qa = pipeline('question-answering', model=model, tokenizer=tokenizer)

# Airtable
AIRTABLE_API = os.environ.get('AIRTABLE_API')
docs_engine = Airtable('appn044eNg7t3BgMn', 'Introduction', AIRTABLE_API)
question_engine = Airtable('appn044eNg7t3BgMn', 'Logs', AIRTABLE_API)
docs = None

# Utilities
def fetch_docs():
	data = ""
	for row in docs_engine.get_all():
		try:
			data += row['fields']['Sentence'] + " "
		except:
			pass
	global docs
	docs = data.strip()

def pronoun(sentence):
	forms = {"are" : "am", 'you' : 'I', 'your' : 'my', 'yours' : 'mine'}
	result = ""
	for word in sentence.translate(str.maketrans('', '', string.punctuation)).split():
		if word.lower() in forms.keys():
			result += forms[word.lower()] + " "
		else:
			result += word + " "
	return result

# Routing
@index_bp.route('/')
def index():
	return render_template('index/index.html', title='Jaeyoung Cho', intro=True, menu_main=True)

progress = 0

@index_bp.route('/chatbot', methods=['POST'])
def answer_question():
	global docs, progress
	progress = 0
	question = request.form['text']
	debug = request.form['debug']
	progress = 30
	result = qa(question=pronoun(question), context=docs)
	progress = 70
	log = '[Question]: ' + question + '\n[Answer]: ' + result['answer'] + '\n[Score]: ' + str(result['score']) + '\n'
	question_engine.insert({
		'Question': question,
		'Answer': result['answer'],
		'Score': str(result['score'])
		})
	progress = 90
	if result['score'] < 0.3:
		text = result['answer'].capitalize() + '\n' + "I am not sure I understand correctly.\nBut you can still reach me by email at chotravis87@gmail.com\n"
	else:
		text = result['answer'].capitalize() + '\n'
	progress = 100
	return text + log if debug == 'true' else text

@index_bp.route('/chatbot/progress')
def get_percentage():
	global progress
	return progress