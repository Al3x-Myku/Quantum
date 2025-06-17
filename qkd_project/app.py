from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/bloch')
def bloch():
    return render_template('bloch.html')

@app.route('/bb84')
def bb84():
    return render_template('bb84.html')

@app.route('/bb84_eve')
def bb84_eve():
    return render_template('bb84_eve.html')

@app.route('/e91')
def e91():
    return render_template('e91.html')

if __name__ == '__main__':
    app.run(debug=True)