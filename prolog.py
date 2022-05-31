from mt import PrologMT

class PrologNLP:
    def __init__(self):
        self.prolog = PrologMT()
        self.prolog.consult("morphophonologicalAnalyzer.pl")

    def analyzer(self, word):
        query = self.prolog.query(f"analyze({word},L).")
        
        s_list = []
        for soln in query:
            for i in range(len(soln["L"])):
                s_list.append(str(soln["L"][i]))
        
        return s_list