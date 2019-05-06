from flask import Flask, render_template


app = Flask(__name__)

# Page
@app.route('/')
def home():
	return render_template('home.html')


@app.route('/about-us/')
def about_us():
	return render_template('about-us.html')


@app.route('/text-to-speech/')
def text_to_speech():
	return render_template('text-to-speech.html')

# API


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)

