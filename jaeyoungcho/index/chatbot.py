from transformers import pipeline
from transformers import BertForQuestionAnswering, BertTokenizer
import string

class Chatbot():
    def __init__(self, model_dir, docs=None):
        self.__docs = docs

        model = BertForQuestionAnswering.from_pretrained(model_dir)
        tokenizer = BertTokenizer.from_pretrained(model_dir)
        self.__qa = pipeline('question-answering', model=model, tokenizer=tokenizer)

        self.__question = ""
        self.__score = ""
        self.__answer = ""

    @property
    def docs(self):
        return self.__docs
    
    @docs.setter
    def docs(self, docs):
        self.__docs = docs
    
    @property
    def answer(self):
        return self.__answer
    
    @property
    def score(self):
        return self.__score

    def __pronoun(self, sentence):
        forms = {"are" : "am", 'you' : 'I', 'your' : 'my', 'yours' : 'mine'}
        result = ""
        for word in sentence.translate(str.maketrans('', '', string.punctuation)).split():
            if word.lower() in forms.keys():
                result += forms[word.lower()] + " "
            else:
                result += word + " "
        return result
    
    def createAnswer(self, question):
        assert self.__docs is not None, "Empty Context Data"
        try:
            result = self.__qa(question=self.__pronoun(question), context=self.__docs)
            self.__question = question
            self.__answer = result['answer']
            self.__score = result['score']
        except ValueError:
            self.__answer = None
            self.__score = None
        
    def generateText(self, debug=False):
        assert all((self.__question is not None, self.__answer is not None, self.__score is not None)),\
            "Missing data found"
        
        log = (
            f"[Question]: {self.__question}\n"
            f"[Answer]: {self.__answer}\n"
            f"[Score]: {self.__score}" 
        )
        lackConfidence = (
            "I'm not sure I'm understanding this right\n"
            "But you can still reach me by email at chotravis87@gmail.com\n"
        )
        if float(self.__score) < 0.3:
            text = self.__answer.capitalize() + '\n' + lackConfidence
        else:
            text = self.__answer.capitalize() + '\n'
        
        return text + log if debug else text

    