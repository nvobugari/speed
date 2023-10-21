from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_prediction')
def get_prediction():
    try:
        # Run the Python script using subprocess.run
        result = subprocess.run(['python', 'mysite/API_final.py'], capture_output=True, text=True, check=True)
        
        # Format the output as HTML
        formatted_result = f'<h2>5 Hours Data:</h2>\n<p>{result.stdout}</p>'
        return formatted_result
    except subprocess.CalledProcessError as e:
        return f'<h2>Error:</h2>\n<p>{e.stderr}</p>'
    except Exception as e:
        return f'<h2>Error:</h2>\n<p>{str(e)}'

if __name__ == '__main__':
    app.run(debug=False)  # Debug should be False in a production environment
