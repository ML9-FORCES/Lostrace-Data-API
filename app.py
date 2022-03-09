from flask import Flask, render_template

app = Flask(__name__)

# To run python file without re-running the flask command
def before_request():
    app.jinja_env.cache = {}
app.before_request(before_request)


# Routes
@app.route('/')
def home():
    return render_template('home.html')


# init
if __name__ == '__main__':
    app.run(debug=True)

