from flask import Blueprint, render_template, request
import os
from pathlib import Path
from transformers import BertForQuestionAnswering, BertTokenizer

from .chatbot import Chatbot
from ..database import Database

index_bp = Blueprint('index_bp', __name__,
	template_folder='templates',
	static_folder='static')

# Routing
@index_bp.route('/')
def index():
	return render_template('index/index.html', title='Jaeyoung Cho', intro=True, menu_main=True)

# Global Variables
progress = 0

# Database
docs_fetcher = Database('appn044eNg7t3BgMn', 'Introduction')
question_uploader = Database('appn044eNg7t3BgMn', 'Logs', False)

# Model
model_dir = str(Path('jaeyoungcho/index/bert').absolute())
model = BertForQuestionAnswering.from_pretrained(model_dir)
tokenizer = BertTokenizer.from_pretrained(model_dir)
chatbot = Chatbot(model_dir, model, tokenizer, docs_fetcher.fetch(['Sentence'], None, lambda lst: ' '.join(word['Sentence'] for word in lst)))

@index_bp.route('/chatbot', methods=['POST'])
def answer_question():
	global progress, chatbot
	chatbot.docs = docs_fetcher.fetch(['Sentence'], None, lambda lst: ' '.join(word['Sentence'] for word in lst))
	progress = 10

	question = request.form['text']
	debug = request.form['debug']
	progress = 30

	chatbot.createAnswer(question)
	answer = chatbot.answer
	score = chatbot.score
	progress = 80
	if answer is None:
		return "Empty question entered"

	question_uploader.append(Question=question, Answer=answer, Score=str(score), Debug=str(debug=='true'))
	progress = 100
	return chatbot.generateText(debug == 'true')	

@index_bp.route('/chatbot/progress', methods=['POST'])
def get_percentage():
	global progress
	return str(progress)