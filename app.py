from flask import Flask
from controllers.job_controller import job_controller

app = Flask(__name__)

app.register_blueprint(job_controller)

if __name__ == '__main__':
    app.run(debug=True)

