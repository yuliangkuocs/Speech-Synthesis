from flask import Flask, render_template


app = Flask(__name__)

# Page
@app.route('/')
def text_to_speech():
	return render_template('text-to-speech.html')


@app.route('/about-us/')
def about_us():
	return render_template('about-us.html')


@app.route('/privacy-policy/')
def privacy_policy():
	return render_template('private-policy.html')


@app.route('/login/')
def login():
	return render_template('login.html')


@app.route('/logout/')
def logout():
	return render_template('logout.html')

# API


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)

