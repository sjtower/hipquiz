import requests
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

dark_sky_api_key = '8b4d5ca925446f9db4f7d7d0aac8b40c'
gmaps_api_key = 'AIzaSyD7W7v5psM8TDJwUV2WxsPkoYRtByh07Y0'

valid_weather_phrases_response = ['what\'s the weather in <Location>', 'weather in <Location>', '<Location> weather']
valid_weather_phrases = ['what\\\'s the weather in', 'weather in', 'weather']
general_error_message = 'I\'m sorry, I did not understand that. Please ask me about the weather with the following ' \
                        'phrases: {}.'.format('; '.join(valid_weather_phrases_response))


@app.route('/chat/messages', methods=['POST'])
def hipquiz_bot():
    print(request.method + " | " + str(request.form))
    user_action = request.form['action']
    if user_action == 'join':
        welcome_message = 'Hello, {}!'.format(request.form['name'])
        return render_template('text_message.json', text=welcome_message)
    elif user_action == 'message':
        return handle_user_message()


def handle_user_message():
    user_message = request.form['text']
    location = get_location(user_message.lower())

    if location is None:
        return render_template('text_message.json', text=general_error_message)

    location = location.replace('?', '')
    print('location: ' + location)

    geo_location = get_geo_location(location)

    if geo_location is None:
        return render_template('text_message.json', text='I\'m sorry, I could not find that location. Please check '
                                                         'the spelling of your location, and try again.')
    print('geo location: ' + str(geo_location))

    summary, temperature = get_current_weather(geo_location)

    return render_template('text_message.json', text='Currently it\'s {}F. {}'.format(temperature, summary))


def get_current_weather(geo_location):
    dark_sky_url = 'https://api.darksky.net/forecast/{}/{},{}'.format(dark_sky_api_key, geo_location['lat'],
                                                                      geo_location['lng'])
    response_json = requests.get(dark_sky_url).json()
    current_weather_json = response_json['currently']
    summary = current_weather_json['summary']
    temperature = current_weather_json['temperature']
    return summary, temperature


def get_geo_location(location):
    gmaps_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(location, gmaps_api_key)
    response_json = requests.get(gmaps_url).json()
    if response_json['results']:
        geo_location = response_json['results'][0]['geometry']['location']
    else:
        geo_location = None
    return geo_location


# todo: if more phrases are added, convert this if/else block to use a regex with capture groups, instead.
def get_location(user_message):
    phrase1 = valid_weather_phrases[0]
    phrase2 = valid_weather_phrases[1]
    phrase3 = valid_weather_phrases[2]
    if user_message.strip() == 'weather':
        location = None
    elif phrase1 in user_message:
        location = user_message.split(phrase1)[1]
    elif phrase2 in user_message:
        location = user_message.split(phrase2)[1]
    elif phrase3 in user_message:
        location = user_message.split(phrase3)[0]
    else:
        location = None
    return location


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, threaded=True)
