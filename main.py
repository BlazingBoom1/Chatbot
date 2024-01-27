from flask import Flask, render_template
from flask_socketio import SocketIO
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import PyPDF2

app = Flask(__name__)
socketio = SocketIO(app)


# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    return text


# Create a chatbot instance
chatbot = ChatBot('WebChatBot')

# Create a trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot on some example conversation
trainer.train("chatterbot.corpus.english")


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(msg):
    response = str(chatbot.get_response(msg))
    socketio.emit('response', response)


if __name__ == '__main__':
    # Replace 'your_pdf_path.pdf' with the path to your PDF file
    pdf_path = '/static/Bhagavad-gita-Swami-BG-Narasingha.pdf'

    # Extract text from the PDF and train the chatbot on it
    pdf_text = extract_text_from_pdf(pdf_path)
    trainer.train([pdf_text])

    # Run the Flask app with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000)
