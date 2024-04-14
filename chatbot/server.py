from flask import Flask, request, render_template, session
import google.generativeai as genai
import re
from parrot import Parrot
import torch
import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
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

# Initialize the Parrot model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=False)


# app = Flask(__name__)
app.secret_key = 'your_secret_key'

genai.configure(api_key="AIzaSyAqWrxIAK5LoTiMEUDrpuo9x6AwIBKbW_w")

generation_config = {
  "temperature": 0.5,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 1400,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": 'BLOCK_NONE'
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": 'BLOCK_NONE'
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": 'BLOCK_NONE'
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": 'BLOCK_NONE'
  },
]

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


model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def remove_text_within_double_asterisks(text):
    return re.sub(r'\*\*.*?\*\*', '', text)

def save_to_file(data):
    with open('data.txt', 'a') as file:
        file.write(str(data) + '\n')

@app.route("/")
def home():
    session.pop('chat_history', None)  # Clear the chat history
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('user_input')  # get the user input from the form
    chat_history = session.get('chat_history', [])  # get the chat history from the session

    # Start a new chat
    convo = model.start_chat()

    # Send the user's message to the conversation
    convo.send_message("As a therapist, how would you respond to this: " + user_input)

    # Get the AI's response
    ai_response = convo.last.text

    # Remove the text within double asterisks
    ai_response = remove_text_within_double_asterisks(ai_response)

    paraphrases = parrot.augment(input_phrase=ai_response)[0]
    ai_response = paraphrases[0] 

    save_to_file({'user_input': user_input, 'ai_response': ai_response})

    chat_history.append(('User', user_input))  # append the user's message
    chat_history.append(('AI', ai_response))  # append the AI's response

    session['chat_history'] = chat_history  # store the updated chat history in the session
    return render_template('index.html', chat_history=chat_history)  # pass the chat history to the template


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
