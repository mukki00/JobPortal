from flask import Flask
from controllers.job_controller import job_controller
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=['http://localhost:4200'])

app.register_blueprint(job_controller)

if __name__ == '__main__':
    app.run(debug=True)

