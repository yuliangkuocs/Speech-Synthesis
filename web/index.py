from flask import Flask, render_template, send_file, jsonify, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = '7433a508b0a1ade2faea975e'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://steven:222222@140.113.123.252:3308/db-Speech-Synthesis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


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
        return render_template('not-login.html')


@app.route('/private-policy/')
def private_policy():
    return render_template('private-policy.html')


@app.route('/login/')
def login():
	if 'user_id' in session:
		print('already login')
		return render_template('already-login.html')
	else:
		print('not login')
		return render_template('login.html')


@app.route('/test/')
def test():
    return render_template('test.html')


@app.route('/steven/')
def steven():
    return render_template('steven.html')


# API
# AUTH
@app.route('/api/auth/login', methods=['POST'])
def api_auth_login():
    request_data = request.get_json()

    try:
        if 'id' not in request_data or 'password' not in request_data:
            return jsonify({'status': False, 'message': 'request data error'}), 400

        if request_data['id'] in users and request_data['password'] == users[request_data['id']]['password']:
            session['user_id'] = request_data['id']
            return jsonify({'status': True, 'message': 'login success', 'id': request_data['id']}), 200

        if request_data['id'] in users and request_data['password'] != users[request_data['id']]['password']:
            session['user_id'] = request_data['id']
            return jsonify({'status': False, 'message': 'wrong password'}), 401

        if request_data['id'] not in users:
            return jsonify({'status': False, 'message': 'user not exists'}), 401

    except Exception as err:
        print('[ERROR - api/auth/login]', err)
        return jsonify({'status': False, 'message': 'undefined error'}), 500


@app.route('/api/auth/logout', methods=['GET'])
def api_auth_logout():
	request_data = request.get_json()

	try:
		if request_data:
			return jsonify({'status': False, 'message': 'request data error'}), 400

		session.pop('user_id', None)
		return jsonify({'status': True, 'message': 'logout success'}), 200

	except Exception as err:
		print('[ERROR - api/auth/logout]', err)
	
		return jsonify({'status': False, 'message': 'undefined error'}), 500

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
