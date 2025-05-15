# app.py (Flask)
from flask import Flask, send_file, render_template, request,flash, redirect
from music import extract_measures_with_detailed_notes
import os
import sys
import webbrowser


if getattr(sys, 'frozen', False):  # Bundled by PyInstaller
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

template_folder = os.path.join(base_path, 'templates')
static_folder = os.path.join(base_path, 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

app.secret_key = 'WL7QykZg19n659351'

data = []
key_sig = ''
time_sig = ''
ks_changes = {}
ts_changes = {}
title = ''
data_size = 1
UPLOAD_FOLDER = 'scores'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/score', methods=['GET','POST'])
def score():
    counter = 0
    global data_size
    global time_sig
    global key_sig
    if request.method == 'POST':
        action = request.form['action']
        counter = int(request.form['ctr']) - 1

        if action == 'next' and counter != (len(data)-1):
            counter = counter+1
        elif action == 'previous' and counter != 0:
            counter = counter-1
        elif action == 'jump' and counter > (len(data)-1):
            counter = data_size-1

        if counter in ks_changes:
            key_sig = ks_changes[counter]

        if counter in ts_changes:
            time_sig = ts_changes[counter]
    return render_template('measure.html',measure_data=data[counter],count=(counter+1), ks=key_sig, ts=time_sig, title=title,ds=data_size)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file and uploaded_file.filename.endswith(('.musicxml', '.xml','.mxl')):
            save_path = os.path.join(UPLOAD_FOLDER, 'score.musicxml')
            uploaded_file.save(save_path)
            flash('File uploaded successfully!')

            #Initialize Score
            global data
            global key_sig
            global time_sig
            global title
            global data_size
            global ts_changes
            global ks_changes
            data,key_sig,time_sig,title,ts_changes,ks_changes = extract_measures_with_detailed_notes('scores/score.musicxml')
            data_size = len(data)
            return redirect('/score')
        else:
            flash('Please upload a valid MusicXML file (.musicxml or .xml)')
            return redirect('/')
    return render_template('upload.html')

if __name__ == '__main__':

    #Remove these below lines if you are deploying remotely
    url = "http://127.0.0.1:8080/"
    webbrowser.open(url)

    #Start app
    app.run(host='0.0.0.0', port=8080, debug=False)
