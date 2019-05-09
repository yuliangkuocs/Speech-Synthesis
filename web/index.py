from flask import Flask, render_template, send_file, jsonify, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '7433a508b0a1ade2faea975e'


users = {'admin': {'password': 'admin'}}


# Page
@app.route('/')
def home():
	if 'user_id' in session:
		return redirect(url_for('text_to_speech'))
	return render_template('home.html')


@app.route('/about-us/')
def about_us():
	return render_template('about-us.html')


@app.route('/text-to-speech/')
def text_to_speech():
	if 'user_id' in session:
		return render_template('text-to-speech.html')
	else:
		return '<h1>Bad Login</h1>'


@app.route('/private-policy/')
def private_policy():
	return render_template('private-policy.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')

	request_data = request.get_json()
	print(request_data)
	if request_data['id'] in users and request_data['password'] == users[request_data['id']]['password']:
		session['user_id'] = request_data['id']
		return jsonify({'response': 'Login Success'}), 200

	return jsonify({'response': 'Wrong name or pw'}), 401


@app.route('/logout/')
def logout():
	session.pop('user_id', None)
	return redirect(url_for('home'))


@app.route('/test/')
def test():
	return render_template('test.html')


@app.route('/steven/')
def steven():
	return render_template('steven.html')


# API
@app.route('/api/demo/getAudio', methods=['POST'])
def api_demo_getAudio():
	filePath = 'static/test.wav'
	
	# return jsonify({'response': 'hi'}), 200
	return jsonify(send_file(filePath, 'audio/wav', True, 'tacotron-ch-92000-0.wav')), 200

# API using Response
#@app.route('/api/demo/wav', methods=['GET', 'POST'])
#def streamwav():
#	def generate():
#        	with open("/static/test.wav", "rb") as fwav:
#	           	data = fwav.read(1024)
#        	    	while data:
#                		yield data
#                		data = fwav.read(1024)
#    return Response(generate(), mimetype="audio/x-wav")

# API Steven test 2
@app.route('/api/test2', methods=['POST'])
def view_method():
     path_to_file = "/static/test.wav"

     return send_file(
         path_to_file, 
         mimetype="audio/wav", 
         as_attachment=True, 
         attachment_filename="test.wav")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)

