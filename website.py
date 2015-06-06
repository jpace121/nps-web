from distanceSensor import DistanceSensor
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

app = Flask(__name__) #I'm globla. Is this ok?
app.config['DEBUG'] = True # should be False in production

@app.route('/')
def index():
    return render_template('index.html',user="Jimmy")

@app.route('/receive', methods=['POST','GET'])
def receive():
    number1 = request.form['number1']
    number2 =request.form['number2']
    summed = int(number1) + int(number2)
    return render_template('receive.html',sum=summed)

if __name__ == '__main__':
    app.run()

