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
            <div style="min-height:100vh; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); display:flex; align-items:center; justify-content:center; font-family:'Comic Sans MS',cursive; position:relative; overflow:hidden;">
                <!-- Super cute floating friends -->
                <img src="https://img.icons8.com/fluency/260/000000/piggy-bank.png" style="position:absolute; top:8%; left:8%; animation:float 6s infinite;">
                <img src="https://img.icons8.com/color/220/000000/taj-mahal.png" style="position:absolute; bottom:10%; right:10%; animation:float 7s infinite;">
                <img src="https://img.icons8.com/emoji/200/000000/airplane.png" style="position:absolute; top:5%; right:0; animation:fly 15s linear infinite;">
                <img src="https://img.icons8.com/color/180/000000/beach.png" style="position:absolute; top:50%; left:5%; animation:float 8s infinite;">

                <div style="background:rgba(255,255,255,0.95); border-radius:50px; padding:70px 100px; box-shadow:0 40px 80px rgba(0,0,0,0.3); text-align:center; border:12px dashed #feca57;">
                    <h1 style="font-size:90px; background:linear-gradient(45deg,#ff6b6b,#feca57,#54a0ff,#48dbfb); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:20px 0;">
                        {a:,.0f} {f} = {result:,.2f} {t}
                    </h1>
                    <p style="font-size:35px; color:#5f27cd; margin:30px;">Rate: 1 {f} = {rate:.4f} {t}</p>

                    <div style="font-size:50px; margin:50px 0;">Have an amazing trip!</div>
                    <div style="font-size:80px; margin:30px 0;">Safe travels!</div>

                    <div>
                        <a href="/currency" style="padding:25px 70px; background:#ff6b6b; color:white; border-radius:70px; font-size:30px; text-decoration:none; margin:20px; box-shadow:0 20px 40px rgba(255,107,107,0.6);">Convert Again</a>
                        <a href="/" style="padding:25px 70px; background:#54a0ff; color:white; border-radius:70px; font-size:30px; text-decoration:none;">Home</a>
                    </div>
                </div>
            </div>
            '''
        except:
            return '<h1 style="text-align:center; padding:200px; color:#ff6b6b; font-size:60px;">Oops! Try again</h1><a href="/currency" style="font-size:40px;">Back</a>'

    # MAIN CUTE CONVERTER PAGE
    return '''
    <div style="min-height:100vh; background:linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); display:flex; align-items:center; justify-content:center; font-family:'Comic Sans MS',cursive; position:relative; overflow:hidden;">
        
        <!-- Floating cute elements -->
        <img src="https://img.icons8.com/fluency/280/000000/piggy-bank.png" style="position:absolute; top:10%; left:10%; animation:float 5s infinite ease-in-out;">
        <img src="https://img.icons8.com/color/200/000000/eiffel-tower.png" style="position:absolute; bottom:12%; left:12%; animation:float 7s infinite;">
        <img src="https://img.icons8.com/color/180/000000/statue-of-liberty.png" style="position:absolute; top:15%; right:15%; animation:float 6s infinite;">
        <img src="https://img.icons8.com/emoji/160/000000/palm-tree-emoji.png" style="position:absolute; bottom:18%; right:10%; animation:float 8s infinite;">
        <img src="https://img.icons8.com/color/150/000000/camera.png" style="position:absolute; top:50%; right:8%; animation:float 9s infinite;">

        <div style="background:white; border-radius:60px; padding:80px 120px; box-shadow:0 50px 100px rgba(0,0,0,0.25); text-align:center; border:15px solid #feca57; position:relative; z-index:10;">
            <h1 style="font-size:80px; background:linear-gradient(45deg,#ff6b6b,#feca57,#54a0ff,#ff9ff3); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:30px;">
                Currency Magic!
            </h1>
            <p style="font-size:32px; color:#5f27cd; margin-bottom:40px;">How much money are we converting today?</p>

            <form method="post">
                <input name="a" value="1000" placeholder="Enter amount" style="padding:30px; width:100%; border-radius:40px; border:6px solid #48dbfb; font-size:38px; text-align:center; margin:30px 0; outline:none; background:#fff;">

                <div style="display:flex; gap:40px; justify-content:center; margin:50px 0;">
                    <select name="f" style="padding:30px; border-radius:40px; font-size:32px; background:#ff9ff3; color:white; border:none; box-shadow:0 20px 40px rgba(255,159,243,0.5);">
                        <option>INR</option><option>USD</option><option>EUR</option><option>GBP</option><option>AED</option><option>THB</option><option>SGD</option><option>JPY</option>
                    </select>
                    <select name="t" style="padding:30px; border-radius:40px; font-size:32px; background:#54a0ff; color:white; border:none; box-shadow:0 20px 40px rgba(84,160,255,0.5);">
                        <option>USD</option><option>INR</option><option>EUR</option><option>GBP</option><option>AED</option><option>THB</option><option>SGD</option><option>JPY</option>
                    </select>
                </div>

                <button type="submit" style="padding:35px 120px; background:linear-gradient(45deg,#ff6b6b,#feca57); color:white; border:none; border-radius:100px; font-size:42px; cursor:pointer; box-shadow:0 30px 60px rgba(255,107,107,0.7); transition:0.4s;">
                    CONVERT NOW!
                </button>
            </form>

            <p style="margin-top:60px; font-size:28px; color:#5f27cd;">Made with love by Priyal for RouteAndRoam</p>
        </div>
    </div>

    <style>
    @keyframes float {
        0%,100% { transform:translateY(0) rotate(0deg); }
        50% { transform:translateY(-40px) rotate(5deg); }
    }
    @keyframes fly {
        0% { transform:translateX(-100vw); }
        100% { transform:translateX(100vw); }
    }
    button:hover { transform:scale(1.1); }
    </style>
    '''
# ─────────────────────────────────────────────────────────────
# PRIYAL'S PART ENDS HERE
# ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("RouteAndRoam started → Your currency converter is now the CUTEST EVER!")
    app.run(debug=True)
