from flask import Flask

# cria uma application instance
app = Flask(__name__) # nome do main module para o Flask determinar o root path

@app.route('/')
def index():
    return "<h1>Hello World!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
