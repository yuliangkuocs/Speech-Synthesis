from flask import Flask, render_template, send_file, jsonify


app = Flask(__name__)

# Page
@app.route('/')
def text_to_speech():
	return render_template('text-to-speech.html')


@app.route('/about-us/')
def about_us():
	return render_template('about-us.html')


@app.route('/private-policy/')
def private_policy():
	return render_template('private-policy.html')


@app.route('/login/')
def login():
	return render_template('login.html')


@app.route('/logout/')
def logout():
	return render_template('logout.html')


@app.route('/test/')
def test():
	return render_template('test.html')


# API
@app.route('/api/demo/getAudio', methods=['POST'])
def api_demo_getAudio():
	filePath = '../data/tacotron-ch-92000-0.wav'

	return jsonify(send_file(filePath, 'audio/wav', True, 'tacotron-ch-92000-0.wav')), 200


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)

