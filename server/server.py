from flask import Flask
from data import db_session, api
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def main():
    app.register_blueprint(api.blueprint)
    db_session.global_init(f'data/main.db')
    app.run(host="0.0.0.0", port=8080)


if __name__ == '__main__':
    main()

print(os.getenv("FLAG"))