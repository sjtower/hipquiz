from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/chat/messages', methods=['POST'])
def handle_messages():
    print(request.method + " | " + str(request.form))
    return render_template('text_message.json', text='test text')


if __name__ == '__main__':
    app.run(host='localhost', port=9000)
