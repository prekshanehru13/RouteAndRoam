# main.py
from flask import Flask, request
import requests, csv
import pandas as pd
url= https://raw.githubusercontent.com/prekshanehru13/RouteAndRoam/refs/heads/main/RouteAndRoam-Data.csv
try:
    df = pd.read_csv(url)
    print(df.head())
except Exception as e:
    print(f"Error reading CSV: {e}")


app = Flask(__name__)


places = []
with open('RouteAndRoam-Data.csv', newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        places.append(row)

@app.route('/')
def home():
    return '''
    <h1 style="color:#e91e63;text-align:center;margin-top:100px;font-family:Arial">
        RouteAndRoam – Travel Guide
    </h1>
    <h2 style="text-align:center;">
        <a href="/places" style="padding:20px 40px;background:#4caf50;color:white;text-decoration:none;border-radius:15px;font-size:25px;">View Places</a>
        <br><br>
        <a href="/currency" style="padding:20px 40px;background:#ff5722;color:white;text-decoration:none;border-radius:15px;font-size:25px;">Currency Converter</a>
    </h2>
    '''

@app.route('/places')
def show():
    html = "<h1 style='color:#2196f3;text-align:center;'>All Places</h1><div style='max-width:900px;margin:auto;'>"
    for p in places:
        html += f"<h2>{p.get('name','')} – {p.get('city','')}</h2><p>{p.get('description','')}</p><hr>"
    return html + '<br><a href="/">← Home</a></div>'

@app.route('/currency', methods=['GET','POST'])
def curr():
    if request.method == 'POST':
        try:
            a = float(request.form['a'])
            f = request.form['f']
            t = request.form['t']
            r = requests.get(f"https://api.exchangerate-api.com/v4/latest/{f}").json()['rates'][t]
            return f"<h2 style='color:green'>Success: {a} {f} = {a*r:.2f} {t}</h2><br><a href='/currency'>Again</a> | <a href='/'>Home</a>"
        except:
            return "<h2 style='color:red'>Error!</h2><a href='/currency'>Try Again</a>"

    return '''
    <h1 style="text-align:center;color:#9c27b0">Currency Converter</h1>
    <form method=post style="text-align:center;font-size:22px">
        Amount <input name=a value=1000 style="padding:10px"><br><br>
        From <select name=f><option>INR</option><option>USD</option><option>EUR</option><option>GBP</option></select>
        To   <select name=t><option>USD</option><option>INR</option><option>EUR</option><option>GBP</option></select><br><br>
        <button style="padding:15px 40px;background:#ff4081;color:white;border:none;font-size:20px;border-radius:12px">Convert</button>
    </form>
    <br><a href="/">Home</a>
    '''

if __name__ == '__main__':
    print(f"Loaded {len(places)} places from RouteAndRoam-Data.csv")
    app.run(debug=True)
