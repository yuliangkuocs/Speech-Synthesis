from index import app
from flask import url_for, render_template, session, redirect


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


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/test/')
def test():
    return render_template('test.html')


@app.route('/steven/')
def steven():
    return render_template('steven.html')
