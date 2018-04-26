from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

dark_sky_api_key = '8b4d5ca925446f9db4f7d7d0aac8b40c'
gmaps_api_key = 'AIzaSyD7W7v5psM8TDJwUV2WxsPkoYRtByh07Y0'

valid_weather_phrases_response = ['what\'s the weather in <Location>', 'weather in <Location>', '<Location> weather']
valid_weather_phrases = ['what\\\'s the weather in', 'weather in', 'weather']
error_message = 'I\'m sorry, I did not understand that. Please ask me about the weather with the following phrases: ' \
                + '; '.join(valid_weather_phrases_response) + '.'


@app.route('/chat/messages', methods=['POST'])
def hipquiz_bot():
    print(request.method + " | " + str(request.form))
    user_action = request.form['action']
    if user_action == 'join':
        welcome_message = 'Hello, ' + request.form['name'] + '!'
        return render_template('text_message.json', text=welcome_message)
    elif user_action == 'message':
        return handle_user_message()


def handle_user_message():
    user_message = request.form['text']
    if valid_weather_phrases[0] in user_message or valid_weather_phrases[1] in user_message:
        location = user_message.split()[-1]
    elif valid_weather_phrases[2] in user_message:
        location = user_message.split()[0]
    else:
        return render_template('text_message.json', text=error_message)

    location = location.replace('?', '')
    print('location: ' + location)

    return render_template('text_message.json', text="success!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, threaded=True)
