from flask import Flask, request, render_template, redirect, url_for
import re
import string
import json
import annealing_decryption
from column_transposition import transpos
app = Flask(__name__)

text = ""

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def my_form_post():
    global text
    text = request.form['text']
    return redirect(url_for('my_methods'))

@app.route('/substitution')
def substitution():
    global text
    userinput = text.upper()
    key = string.ascii_uppercase
    ciphertype = "substitution"
    regex = re.compile('[^A-Z]')
    print("solving")
    result = annealing_decryption.anneal(regex.sub('', userinput), key, ciphertype, "swap", "")
    print(result)
    return(result)

@app.route('/columntrans', methods=['GET', 'POST'])
def columntrans():
    global text
    userinput = text.upper()
    regex = re.compile('[^A-Z]')
    colno = int(request.get_json())
    if colno > 1:
        return(transpos(regex.sub('', userinput), colno))

    else:
        threads = []
        for x in range(2, 10):
            process = Thread(target=transpos, args=[
                            regex.sub('', userinput), x])
            process.start()
            threads.append(process)

@app.route('/methods')
def my_methods():
    return render_template('methods.html')

@app.route('/methods', methods=['GET', 'POST'])
def my_methods_post():
    global text
    userinput = text.upper()
    key = string.ascii_uppercase
    ciphertype = "substitution"
    regex = re.compile('[^A-Z]')
    return(annealing_decryption.anneal(regex.sub('', userinput), key, ciphertype, "swap", ""))    

if __name__ == '__main__':
   app.run(debug = True)