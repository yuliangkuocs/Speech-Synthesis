# coding=UTF-8
from flask import Flask
from database.database import create_tables

app = Flask(__name__)
app.secret_key = '7433a508b0a1ade2faea975e'


if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=8080)
