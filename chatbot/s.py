from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message




app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pritishmajumdar066@gmail.com'
app.config['MAIL_PASSWORD'] = 'epbe sksg pkea cufw'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

questions = [
    "Over the last 2 weeks, how often have you been bothered by any of the following problems? Little interest or pleasure in doing things.",
    "Feeling down, depressed, or hopeless.",
    "Trouble falling or staying asleep, or sleeping too much.",
    "Feeling tired or having little energy.",
    "Poor appetite or overeating.",
    "Feeling bad about yourself - or that you are a failure or have let yourself or your family down.",
    "Trouble concentrating on things, such as reading the newspaper or watching television.",
    "Moving or speaking so slowly that other people could have noticed. Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual.",
    "Thoughts that you would be better off dead, or of hurting yourself."
]

@app.route('/phq9')
def phq():
    return render_template('phq9.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    answers = [int(request.form.get(f'q{i}')) for i in range(len(questions))]
    total_score = sum(answers)

    message = "Your score could not be categorized."  # Default message

    if total_score <= 4:
        message = "Your score is within the minimal depression range. However, if you have any concerns, please consult with a healthcare professional."
    elif total_score <= 9:
        message = "Your score is within the mild depression range. It's recommended that you consult with a healthcare professional for further evaluation."
    elif total_score <= 14:
        message = "Your score is within the moderate depression range. It's recommended that you consult with a healthcare professional. Therapy, medication, or a combination of these may be beneficial."
    elif total_score <= 19:
        message = "Your score is within the moderately severe depression range. It's very important that you consult with a healthcare professional soon. Therapy, medication, or a combination of these may be beneficial."
    elif total_score >= 20:
        message = "Your score is within the severe depression range. It's crucial that you consult with a healthcare professional immediately. Immediate action is recommended."
        msg = Message('PHQ-9 Report',
                      sender='pritishmajumdar066@gmail.com',
                      recipients=['pijush2smart@gmail.com'])
        msg.body = f"The PHQ-9 score is: {total_score}. {message}"
        mail.send(msg)

    return f"Your PHQ-9 score is: {total_score}. {message}"

if __name__ == '__main__':
    app.run(debug=True)
