from flask import Flask, render_template, send_file, jsonify
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user


app = Flask(__name__)
app.secret_key = '7433a508b0a1ade2faea975e'

login_manager - LoginManager(app)
users = {'admin': {'password': 'admin'}}


class User(UserMixin):
	pass


@login_manager.user_loader
def user_loader(user_id):
	if user_id not in users:
		return
	user = User()
	user.id = user_id
	return user


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
	if request.method == 'GET':
		return render_template('login.html')
	
	user_id = request.form['id']
	if request.form['password'] == users[user_id]['password']:
		user = User()
		user.id = user_id
		login_user(user)
		return redirect(url_for('protect'))
	return 'Login Fail'


@app.route('/protect/')
def protect():
	if current_user.is_active:
		return 'Logged in as: ' + current_user.id

@app.route('/logout/')
def logout():
	return render_template('logout.html')


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

