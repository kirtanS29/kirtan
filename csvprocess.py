from flask import Flask, request, send_file
import pandas as pd
from pandas_profiling import ProfileReport
import os

app = Flask(__name__)

# Specify the directory for saving the reports
REPORTS_DIR = 'reports'

@app.route('/')
def index():
    return '''
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv">
        <input type="submit" value="Upload CSV File">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return "No file part"
        
    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        df = pd.read_csv(file)
        profile = ProfileReport(df)
        
        # Create the reports directory if it doesn't exist
        if not os.path.exists(REPORTS_DIR):
            os.makedirs(REPORTS_DIR)
        
        report_path = os.path.join(REPORTS_DIR, 'output.html')
        profile.to_file(report_path)
        
        return f"CSV file processed successfully. <a href='/report/{report_path}'>View the report</a>"

@app.route('/report/<path:filename>')
def serve_report(filename):
    return send_file(filename)

if __name__ == '__main__':
    app.run(debug=True)