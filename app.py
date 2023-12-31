from flask import Flask, render_template, jsonify
import subprocess
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_prediction')
def get_prediction():
    print ("in get_prediction")
    try:
        print ("in try")
        # Run the Python script and capture its output
        result = subprocess.check_output(['python', 'API_final.py'], universal_newlines=True,stderr=subprocess.STDOUT)

        # Format the output as HTML
        formatted_result = f'<h2>5 Hours Data:</h2>\n<p>{result}</p>'

        return formatted_result
    except Exception as e: 
        print ("in else")
        print(e)
        return f'<h2>Error:</h2>\n<p>{str(e)}</p>'

if __name__ == '__main__':
    app.run(debug=True)
