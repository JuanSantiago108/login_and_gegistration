from flask import Flask
from flask import flash,session
app = Flask(__name__)
app.secret_key = "\x1fkX\xc6N\xb8v\xe7\xabS\xc5'O]\x05o\xab\xa2\x1c\xd1\x9f"
DATABASE = "user_email"
