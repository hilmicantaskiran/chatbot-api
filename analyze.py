import json
from prolog import PrologNLP
from tokenizer import Tokenizer


class Analyze:
    def __init__(self):
        self.data = open("Data/data.json")
        self.data = json.load(self.data)
        self.createCorpus()
        self.prolog = PrologNLP()
        
        self.dirList = ["e", "a", "ye", "ya"]
        self.ablList = ["den", "dan", "ten", "tan", "ndan", "nden", "nten", "ntan"]


    def createCorpus(self):
        self.corpus = set()

        for pair in self.data:
            for keys in pair['key-words']:
                for key in keys:
                    self.corpus.add(key)

    def analyzeQuestion(self, question):
        self.answer = ""
        self.answerKeyLength = -1
        
        self.target = ""
        self.location = ""

        questionWords = Tokenizer.tokenize(question)

        questionKeyWords = []
        for index, word in enumerate(questionWords):
            if word in self.ablList:
                self.location = questionWords[index-1]
            elif word in self.dirList:
                self.target = questionWords[index-1]
            
            if word in self.corpus:
                q_answer = []
            else: 
                q_answer = self.prolog.analyzer(word)
            
            for key in self.corpus:
                if key in word:
                    questionKeyWords.append(key)
                
                else:
                    if len(q_answer) != 0:
                        if key == q_answer[0]:
                             questionKeyWords.append(key)
                             
                        if len(q_answer) > 1:
                            if q_answer[-1] in self.ablList:
                                self.location = q_answer[0]
                            elif q_answer[-1] in self.dirList:
                                self.target = q_answer[0]
                            
        if len(questionKeyWords) > 0:
            for pair in self.data:
                for keys in pair['key-words']:
                    if set(questionKeyWords) >= set(keys):
                        if self.answerKeyLength == -1 or len(set(keys)) > self.answerKeyLength:
                            if self.location != "" and self.target != "":
                                if self.location == pair["source"]["location"] and self.target == pair["source"]["target"]:
                                    self.answer = pair['answer']
                                    self.answerKeyLength = len(set(keys))
                            
                            else:
                                self.answer = pair['answer']
                                self.answerKeyLength = len(set(keys))

        if self.answer != "":
            return self.answer
        else:
            return "Bu soruya bir cevap üretemedim."
