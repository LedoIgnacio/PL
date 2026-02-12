from flask import Flask
from route import route

app = Flask(__name__, template_folder = "templates", static_folder = "static")

app.config["SECRET_KEY"] = "powerlab_secret_key"

route(app)

if __name__ == "__main__":
    app.run(debug = True)