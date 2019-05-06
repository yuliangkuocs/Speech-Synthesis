from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
	return '<h1>This is Index Page</h1>'


@app.route('/aboutus/')
def aboutus():
	return '<h1>About Us</h1>'

@app.route('/tts/')
def tts():
	return render_template('tts.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)

