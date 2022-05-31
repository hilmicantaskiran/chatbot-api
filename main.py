from flask import Flask, request
from analyze import Analyze

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.get_json().get('question')
        answer = analyze.analyzeQuestion(question)
        return {
            'success': True,
            'answer': answer
        }
        
    else: return 'Server is running'

if __name__ == "__main__":
    analyze = Analyze()
    app.run(host='0.0.0.0', port=8080, debug=True)
