# main.py 
from flask import Flask, request
import requests, csv
from module3 import PlacesModule
mod = PlacesModule('RouteAndRoam-Data.csv')


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
            background-image: url('https://raw.githubusercontent.com/prekshanehru13/RouteAndRoam/refs/heads/main/RouteAndRoamBG.jpg');
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
            background-image: url('https://raw.githubusercontent.com/prekshanehru13/RouteAndRoam/refs/heads/main/RouteAndRoamBG.jpg');
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
            <a href="/explore" style="
                padding: 20px 60px;
                background: #FF4500;
                color: white;
                border-radius: 50px;
                font-size: 28px;
                font-weight: 600;
                text-decoration: none;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            ">Explore</a>
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

# ================================================
# PRIYAL SINGH'S CURRENCY CONVERTER STARTS
# ====================================
@app.route('/currency', methods=['GET','POST'])
def currency():
    currencies = ["INR","USD","EUR","GBP","JPY","AED","THB","CNY","KRW","SGD","AUD","CAD","CHF","BRL","PHP","VND","IDR","MYR"]
    options = "".join(f"<option value='{c}'>{c}</option>" for c in currencies)

    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            f = request.form['f']
            t = request.form['t']
            rate = requests.get(f"https://api.exchangerate-api.com/v4/latest/{f}").json()['rates'][t]
            result = amount * rate

            return f'''
            <div style="min-height:100vh;background:linear-gradient(135deg,#ffb300,#ff9800);display:flex;align-items:center;justify-content:center;font-family:system-ui;">
                <audio autoplay><source src="https://assets.mixkit.co/sfx/preview/mixkit-coin-cha-ching-2108.mp3"></audio>
                <div style="background:white;padding:60px 100px;border-radius:30px;box-shadow:0 25px 60px rgba(0,0,0,0.2);text-align:center;width:90%;max-width:600px;">
                    <h1 style="font-size:48px;color:#e65100;margin:20px 0;">{amount:,.0f} {f}</h1>
                    <div style="font-size:60px;color:#ff6f00;margin:30px 0;">↓</div>
                    <h1 style="font-size:60px;color:#e65100;margin:20px 0;">{result:,.2f} {t}</h1>
                    <p style="font-size:24px;color:#e65100;margin:30px 0;">Rate: 1 {f} = {rate:.4f} {t}</p>
                    <h2 style="font-size:44px;color:#ff6f00;margin:40px 0;">CHA-CHING!</h2>
                    <div>
                        <a href="/currency" style="padding:15px 60px;background:#ff6f00;color:white;border-radius:30px;font-size:22px;margin:10px;">Again</a>
                        <a href="/" style="padding:15px 60px;background:#333;color:white;border-radius:30px;font-size:22px;margin:10px;">Home</a>
                    </div>
                </div>
            </div>
            '''
        except:
            return "<h1 style='color:red;text-align:center;padding-top:40vh;font-size:40px;'>Error! Check amount</h1><a href='/currency'>Back</a>"

    # MAIN PAGE – COMPACT & BEAUTIFUL
    return f'''
    <div style="min-height:100vh;background:linear-gradient(135deg,#ffb300,#ff9800);display:flex;align-items:center;justify-content:center;font-family:system-ui;">
        <div style="background:white;padding:70px 90px;border-radius:30px;box-shadow:0 25px 60px rgba(0,0,0,0.2);text-align:center;width:90%;max-width:600px;">
            <h1 style="font-size:48px;color:#e65100;margin-bottom:30px;">Currency Converter</h1>
            <form method="post">
                <input name="amount" value="1000" placeholder="Amount" style="padding:20px;width:100%;border-radius:20px;border:2px solid #ff6f00;font-size:30px;text-align:center;margin:30px 0;background:#fff8e1;">
                <div style="display:flex;gap:30px;justify-content:center;margin:50px 0;">
                    <select name="f" style="padding:20px;border-radius:20px;font-size:26px;background:#ff8a65;color:white;border:none;width:48%;">{options}</select>
                    <select name="t" style="padding:20px;border-radius:20px;font-size:26px;background:#ff7043;color:white;border:none;width:48%;">{options}</select>
                </div>
                <button style="padding:20px 120px;background:#e65100;color:white;border:none;border-radius:30px;font-size:32px;cursor:pointer;">CONVERT NOW</button>
            </form>
            <p style="margin-top:60px;font-size:18px;color:#666;">by Priyal Singh</p>
        </div>
    </div>
    '''
# ====================================
# PRIYAL SINGH'S CURRENCY CONVERTER ENDS
# ====================================
if __name__ == '__main__':
    print("RouteAndRoam started → Your currency converter is now the CUTEST EVER!")
    app.run(debug=True)

# ====================================
# Shreya's Part Starts Here!
# ====================================
@app.route('/explore', methods=['GET', 'POST'])
def explore():
    if request.method == 'POST':
        country = request.form['country']
        places = mod.list_places_by_country(country)

        if not places:
            return f"<h2>No places found in {country}</h2><a href='/explore'>Back</a>"

        # If country submitted but no place selected yet
        if 'place' not in request.form:
            html = f"<h1>Places in {country.title()}</h1>"
            html += "<form method='post'>"
            html += f"<input type='hidden' name='country' value='{country}'>"
            html += "<select name='place'>"

            for p in places:
                html += f"<option value='{p}'>{p}</option>"

            html += "</select>"
            html += "<button type='submit'>Show Details</button></form>"
            return html

        # Step 2: User selected place
        place = request.form['place']
        info = mod.get_place_info(country, place)

        if info is None:
            return "<h2>Place not found</h2> <a href='/explore'>Try Again</a>"

        return f"""
        <h1>Details</h1>
        <p><b>Country:</b> {info['COUNTRY']}</p>
        <p><b>Place:</b> {info['PLACE']}</p>
        <p><b>Language:</b> {info['LANGUAGE']}</p>
        <p><b>Timezone:</b> {info['TIMEZONE']}</p>
        <p><b>Specialities:</b> {info['SPECIALITIES']}</p>
        <img src="{info['IMAGES']}" width="400">
        <br><br>
        <a href='/explore'>Search Again</a>
        """
    
    # FIRST LOAD — ask for country
    return """
    <h1>Search Places</h1>
    <form method="post">
        <input name="country" placeholder="Enter country name">
        <button type="submit">Search</button>
    </form>
    """



# ====================================
# Shreya's part ends here
# ====================================


