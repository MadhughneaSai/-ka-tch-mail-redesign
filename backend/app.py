# Author: MrKangs

from flask import Flask
from routes.mail_routes import mail_bp
from routes.auth_routes import auth_bp
from flask_cors import CORS
from flask_session import Session
from flask_mail import Mail

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
# app.config.from_object(Config)

Session(app)

mail = Mail(app)

# Remove all Google OAuth2 and Gmail API related code

# Register blueprints
app.register_blueprint(mail_bp, url_prefix='/mail')
app.register_blueprint(auth_bp, url_prefix='/auth')

# CORS Configuration - Added PUT method for bonus features
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
}}, supports_credentials=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)