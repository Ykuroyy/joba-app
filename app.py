import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load quiz data from JSON file
with open('quiz_data.json', 'r', encoding='utf-8') as f:
    quiz_data = json.load(f)

@app.route('/')
def index():
    # Render the main quiz page with questions
    return render_template('index.html', questions=quiz_data)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    # Loop through each question to check the submitted answer
    for question in quiz_data:
        question_id = str(question['id'])
        selected_option = request.form.get(question_id)
        # If the selected option is correct, increment the score
        if selected_option and selected_option == question['answer']:
            score += 1
    # Render the result page with the final score
    return render_template('result.html', score=score, total=len(quiz_data))

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    selected_option = data.get('selected_option')

    question = next((q for q in quiz_data if q['id'] == question_id), None)

    if question and selected_option == question['answer']:
        return jsonify({'correct': True})
    else:
        return jsonify({'correct': False})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)