from flask import Flask
from models import db
from routes import routes_bp  # Blueprint importieren

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)
app.register_blueprint(routes_bp)  # Blueprint registrieren

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
