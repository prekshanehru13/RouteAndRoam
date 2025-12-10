# main.py 
from flask import Flask, request
import requests, csv

app = Flask(__name__)

# Load your CSV (your teammates' part remains untouched)
places = []
try:
    with open('RouteAndRoam-Data.csv', newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            places.append(row)
except:
    places = []

@app.route('/')
def home():
    return '''
    <div style="
        position: relative;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        align-items: center;
        padding-bottom: 220px;
        font-family: 'Poppins', sans-serif;
        overflow: hidden;
    ">

        <!-- Blurred background layer -->
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('"\static\RouteAndRoamBG.jpg"');
            background-size: cover;
            background-position: center;
            filter: blur(18px) brightness(0.8);
            transform: scale(1.2);     /* avoid blur edges */
            z-index: -2;
        "></div>

        <!-- Main image (full but not zoomed) -->
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('"\static\RouteAndRoamBG.jpg"');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            z-index: -1;
        "></div>

        <!-- Buttons -->
        <div style="
            display: flex;
            gap: 40px;
            z-index: 5;
        ">
            <a href="/places" style="
                padding: 20px 60px;
                background: #FF4500;
                color: white;
                border-radius: 50px;
                font-size: 28px;
                font-weight: 600;
                text-decoration: none;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            ">Destinations</a>

            <a href="/currency" style="
                padding: 20px 60px;
                background: #FF4500;
                color: white;
                border-radius: 50px;
                font-size: 28px;
                font-weight: 600;
                text-decoration: none;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            ">Currency Exchange</a>
        </div>

    </div>
    '''

@app.route('/places')
def show():
    html = "<h1 style='text-align:center; color:#5f27cd; margin:70px; font-size:55px;'>Our Beautiful Places</h1><div style='display:grid; grid-template-columns:repeat(auto-fit,minmax(350px,1fr)); gap:30px; padding:40px;'>"
    for p in places:
        
        html += f"""
        <div style='background:white; border-radius:30px; padding:30px; 
        box-shadow:0 25px 50px rgba(0,0,0,0.15); text-align:center;'>

            <h2 style='color:#ff6b6b;'>{p.get('PLACE','')}</h2>
            <h3 style='color:#54a0ff;'>{p.get('COUNTRY','')}</h3>

            <p><b>Language:</b> {p.get('LANGUAGE','')}</p>
            <p><b>Timezone:</b> {p.get('TIMEZONE','')}</p>
            <p><b>Specialities:</b> {p.get('SPECIALITIES','')}</p>

            <img src="{p.get('IMAGES','')}" 
            style="width:100%; border-radius:20px; margin-top:15px;">
        </div>
        """


    return html + '</div><div style="text-align:center; margin:70px;"><a href="/" style="padding:20px 60px; background:#feca57; color:white; border-radius:60px; text-decoration:none; font-size:26px;">Home</a></div>'

# ─────────────────────────────────────────────────────────────
# PRIYAL'S STARTS HERE →  CURRENCY CONVERTER 
# ─────────────────────────────────────────────────────────────
@app.route('/currency', methods=['GET','POST'])
def curr():
    if request.method == 'POST':
        try:
            a = float(request.form['a'])
            f = request.form['f']
            t = request.form['t']
            rate = requests.get(f"https://api.exchangerate-api.com/v4/latest/{f}").json()['rates'][t]
            result = a * rate

            return f'''
            <div style="min-height:100vh; display:flex; align-items:center; justify-content:center; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:linear-gradient(135deg,#ffe6e6,#fff0f5);">
                <div style="background:#fff; border-radius:25px; padding:60px 80px; box-shadow:0 15px 40px rgba(0,0,0,0.15); max-width:700px; width:90%; text-align:center; position:relative;">
                    <div style="font-size:50px; margin-bottom:20px;">💰💱</div>
                    <h1 style="font-size:50px; color:#e63946; margin-bottom:15px;">
                        {a:,.2f} {f} = {result:,.2f} {t}
                    </h1>
                    <p style="font-size:22px; color:#555; margin-bottom:40px;">
                        🔹 Exchange Rate: 1 {f} = {rate:.4f} {t}
                    </p>

                    <div style="display:flex; gap:20px; justify-content:center; flex-wrap:wrap;">
                        <a href="/currency" style="padding:15px 45px; background:#e63946; color:white; border-radius:12px; text-decoration:none; font-size:18px; box-shadow:0 5px 15px rgba(230,57,70,0.3); transition:0.3s;">Convert Again 🔄</a>
                        <a href="/" style="padding:15px 45px; background:#6c757d; color:white; border-radius:12px; text-decoration:none; font-size:18px; box-shadow:0 5px 15px rgba(108,117,125,0.3); transition:0.3s;">Home 🏠</a>
                    </div>

                    <p style="font-size:14px; color:#999; margin-top:30px;">Made by Priyal Singh</p>
                </div>
            </div>
            '''
        except:
            return '<h1 style="text-align:center; padding:200px; color:#ff4c4c; font-size:60px;">Oops! Try again ⚠️</h1><a href="/currency" style="font-size:30px;">Back</a>'

    # MAIN PROFESSIONAL + COLOURFUL CONVERTER PAGE
    return '''
    <div style="min-height:100vh; display:flex; align-items:center; justify-content:center; font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:linear-gradient(135deg,#ffe6e6,#fff0f5);">
        <div style="background:#fff; border-radius:25px; padding:60px 80px; box-shadow:0 20px 60px rgba(0,0,0,0.1); max-width:700px; width:90%; text-align:center; position:relative;">
            <div style="font-size:50px; margin-bottom:20px;">💰💱</div>
            <h1 style="font-size:45px; color:#e63946; margin-bottom:15px;">Currency Converter</h1>
            <p style="font-size:20px; color:#555; margin-bottom:40px;">Convert any currency quickly and accurately ✨</p>

            <form method="post" style="display:flex; flex-direction:column; gap:25px;">
                <input name="a" value="1000" placeholder="Enter amount" style="padding:18px; border-radius:12px; border:1px solid #ccc; font-size:20px; width:100%; outline:none;">

                <div style="display:flex; gap:20px; flex-wrap:wrap; justify-content:center;">
                    <select name="f" style="padding:15px; border-radius:12px; font-size:18px; border:1px solid #ccc;">
                        <option>INR</option><option>USD</option><option>EUR</option><option>GBP</option><option>AED</option><option>THB</option><option>SGD</option><option>JPY</option>
                    </select>
                    <select name="t" style="padding:15px; border-radius:12px; font-size:18px; border:1px solid #ccc;">
                        <option>USD</option><option>INR</option><option>EUR</option><option>GBP</option><option>AED</option><option>THB</option><option>SGD</option><option>JPY</option>
                    </select>
                </div>

                <button type="submit" style="padding:18px 0; background:#e63946; color:white; border:none; border-radius:12px; font-size:20px; cursor:pointer; transition:0.3s;">Convert 💹</button>
            </form>

            <p style="font-size:14px; color:#999; margin-top:30px;">Made by Priyal Singh</p>
        </div>
    </div>
    '''

# ─────────────────────────────────────────────────────────────
# PRIYAL'S PART ENDS HERE
# ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("RouteAndRoam started → Your currency converter is now the CUTEST EVER!")
    app.run(debug=True)
