# main.py
from flask import Flask, request
import requests, csv
from module3 import PlacesModule
# Load RouteAndRoam CSV for explore feature
mod = PlacesModule("RouteAndRoam-Data.csv")
app = Flask(__name__)
# Load your CSV 
#FRONTEND
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
            transform: scale(1.2); /* avoid blur edges */
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
            <a href="/season" style="
                padding: 20px 60px;
                background: #FF4500;
                color: white;
                border-radius: 50px;
                font-size: 28px;
                font-weight: 600;
                text-decoration: none;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            ">Best Season</a>
        </div>
    </div>
    '''
#BACKEND
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
# ====================================
# Shreya's Part Starts Here!
# ====================================
@app.route('/explore')
def explore():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>RouteAndRoam - Amazing Travel Destinations</title>
      <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
      <style>
        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background: linear-gradient(135deg, #ffd166, #ff9a56, #ff6b35, #f7931e);
          margin: 0;
          padding: 20px;
          color: #333;
          min-height: 100vh;
        }
        h1 {
          text-align: center;
          color: white;
          margin-bottom: 10px;
          font-family: 'Playfair Display', serif;
          font-size: 3.6em;
          letter-spacing: 4px;
          text-shadow: 0 8px 25px rgba(0,0,0,0.5);
        }
        .subtitle {
          text-align: center;
          color: #ffffe0;
          margin-bottom: 60px;
          font-size: 1.4em;
          font-style: italic;
          text-shadow: 0 3px 10px rgba(0,0,0,0.4);
        }
        .controls {
          max-width: 900px;
          margin: 0 auto 70px;
          display: flex;
          gap: 25px;
          flex-wrap: wrap;
          justify-content: center;
        }
        select {
          padding: 18px 22px;
          border: none;
          border-radius: 18px;
          font-size: 17px;
          box-shadow: 0 10px 30px rgba(0,0,0,0.3);
          background: rgba(255,255,255,0.92);
          min-width: 260px;
          cursor: pointer;
          backdrop-filter: blur(8px);
        }
        #detailsBox {
          max-width: 1100px;
          margin: 50px auto;
          padding: 60px;
          background: rgba(255, 255, 255, 0.95);
          border-radius: 30px;
          box-shadow: 0 25px 60px rgba(0,0,0,0.35);
          display: none;
          text-align: center;
          backdrop-filter: blur(20px);
          border: 2px solid rgba(255, 180, 80, 0.5);
        }
        #detailsBox h2 {
          color: #d35400;
          margin-top: 0;
          font-size: 3em;
          text-shadow: 0 4px 10px rgba(0,0,0,0.2);
          font-family: 'Playfair Display', serif;
        }
        .description {
          font-size: 1.3em;
          line-height: 2;
          color: #444;
          max-width: 900px;
          margin: 40px auto;
          padding: 30px;
          background: #fffff0;
          border-radius: 20px;
          border-left: 8px solid #e67e22;
          box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }
        .images-container {
          display: flex;
          flex-wrap: wrap;
          gap: 30px;
          justify-content: center;
          margin: 50px 0;
        }
        .images-container img {
          max-width: 100%;
          max-height: 500px;
          border-radius: 25px;
          box-shadow: 0 20px 45px rgba(0,0,0,0.35);
          cursor: pointer;
          transition: transform 0.6s ease, box-shadow 0.6s ease;
          object-fit: cover;
        }
        .images-container img:hover {
          transform: translateY(-20px) scale(1.04);
          box-shadow: 0 40px 80px rgba(0,0,0,0.45);
        }
        .footer {
          text-align: center;
          margin-top: 120px;
          color: #ffffe0;
          font-size: 1.1em;
          text-shadow: 0 3px 12px rgba(0,0,0,0.5);
        }
        @media (max-width: 768px) {
          .images-container {
            flex-direction: column;
            align-items: center;
          }
          h1 { font-size: 3em; }
          select { min-width: 100%; }
          #detailsBox { padding: 40px; }
        }
      </style>
    </head>
    <body>
      <h1>RouteAndRoam</h1>
      <p class="subtitle">Every Route, Every Roam, Your Adventure Awaits</p>
      <div class="controls">
        <select id="countryFilter">
          <option value="">Select a Country</option>
          <option value="Bhutan">Bhutan</option>
          <option value="Maldives">Maldives</option>
          <option value="Singapore">Singapore</option>
          <option value="Thailand">Thailand</option>
        </select>
        <select id="placeFilter" disabled>
          <option value="">First select a country</option>
        </select>
      </div>
      <div id="detailsBox">
        <h2 id="placeName"></h2>
        <div class="description" id="descriptionText"></div>
        <div class="images-container" id="imagesContainer"></div>
      </div>
      <div class="footer">
        Made with love for wanderlust souls ✈️🌴🏖️🍹
      </div>
      <script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js"></script>
      <script>
        const countryFilter = document.getElementById('countryFilter');
        const placeFilter = document.getElementById('placeFilter');
        const detailsBox = document.getElementById('detailsBox');
        const placeName = document.getElementById('placeName');
        const descriptionText = document.getElementById('descriptionText');
        const imagesContainer = document.getElementById('imagesContainer');
        const csvData = `Country,Place,Description,Image_URL_1,Image_URL_2
Maldives,Maafushi Island,"Maafushi Island in South Male Atoll revolutionized Maldives tourism when guesthouses were permitted on local islands in 2009, shifting from exclusive luxury resorts to affordable, authentic experiences. Once a quiet fishing village with a former prison, it now boasts Bikini Beach (rare designated swimwear area on inhabited islands), crystal-clear lagoons, and vibrant marine life. Specialties include budget stays, local Maldivian cuisine like mas huni and hedika snacks, and cultural immersion. Cool activities: snorkeling and diving excursions, dolphin-watching cruises, water sports (jet skiing, parasailing), sandbank picnics, resort day passes, village tours to see traditional life, and sunset fishing trips. With over 100 guesthouses, it's perfect for backpackers seeking paradise without breaking the bank.",https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0c/36/ef/a2/active-watersports-maafushi.jpg?w=1200&h=700&s=1,https://www.maldivesislandsresorts.com/uploads/andamanislands/destinations/main/6762835d63bba184_maafushi.jpg
Maldives,Vaadhoo Island (Sea of Stars),"Vaadhoo Island on Raa Atoll captivates visitors with its world-famous bioluminescent plankton phenomenon known as the 'Sea of Stars,' where waves and footsteps create a glowing blue sparkle at night due to dinoflagellates, best viewed during warm months (June-November). This quiet local island gained global fame through viral photographs promoting grassroots tourism. Specialties: Natural light show and serene beaches. Activities include night beach walks to witness the glow, snorkeling vibrant reefs, diving, kayaking through mangroves, fishing with locals, and cultural experiences like visiting mosques or trying traditional Boduberu drum performances. Stay in modest guesthouses for an authentic, off-the-grid escape.",https://img.atlasobscura.com/-714kRa70D74swzWNha3DgImXZho3G3Bnv3o5jaBEFo/rs:fill:780:520:1/g:ce/q:81/sm:1/scp:1/ar:1/aHR0cHM6Ly9hdGxh/cy1kZXYuczMuYW1h/em9uYXdzLmNvbS91/cGxvYWRzL3BsYWNl/X2ltYWdlcy85NWQ5/ZmE0OC0zYWE4LTRl/MTYtYmNjYS05Zjdi/YTNkNDk1MDFkZTRj/ZThmYzFlZWNhZmQy/OWJfRTQ2MUVCLmpw/Zw.jpg,https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2c/9f/1a/60/caption.jpg?w=800&h=-1&s=1
Maldives,Hanifaru Bay,"Hanifaru Bay in Baa Atoll, a UNESCO Biosphere Reserve, transformed from a historical whale shark hunting site to one of the world's premier marine protected areas since the 1990s. Famous for massive feeding aggregations of up to 200 manta rays and whale sharks during plankton blooms (peak June-November). Strict conservation rules limit visitors and prohibit scuba diving to protect this natural cleaning station. Specialties: Bucket-list manta encounters. Activities: Guided snorkeling sessions (book in advance), contributing to citizen science via photo IDs, staying on nearby resort islands for multi-day experiences, and combining with reef dives in the atoll. A must for marine enthusiasts.",https://images.pexels.com/photos/9215864/pexels-photo-9215864.jpeg,https://images.pexels.com/photos/4751277/pexels-photo-4751277.jpeg
Maldives,Banana Reef,"Banana Reef in North Male Atoll, discovered in the early 1970s, is one of the Maldives' oldest and most celebrated dive sites, named for its curved banana-like shape featuring dramatic cliffs, overhangs, caves, and colorful coral gardens. Teeming with marine life including reef sharks, barracudas, groupers, moray eels, and schools of jacks. Historical significance as a pioneer site that helped establish Maldives diving tourism. Specialties: Year-round diving with varied topography. Activities: Scuba diving (drift dives for advanced), snorkeling shallower parts, night dives to see nocturnal creatures, and combining with nearby sites like Kani Corner. Ideal for all levels.",https://dynamic-media-cdn.tripadvisor.com/media/photo-o/04/54/97/c8/banana-reef.jpg?w=900&h=-1&s=1,https://afar.brightspotcdn.com/dims4/default/81b4ff2/2147483647/strip/false/crop/800x450+0+25/resize/1200x675!/quality=90/?url=https%3A%2F%2Fk3-prod-afar-media.s3.us-west-2.amazonaws.com%2Fbrightspot%2Fce%2F16%2Fd06e385fd247e444e5e639d15e1f%2Foriginal-0c9dec88c40d6e00f1702e1cc70c97ca.jpg
Maldives,Veligandu Island,"Veligandu Island in Rasdhoo Atoll has hosted a luxury resort since 1984, recently renovated in 2024, renowned for romantic overwater villas, a vibrant house reef, and adults-focused ambiance. Known for powdery white sands and turquoise lagoons. History as an early resort pioneering intimate escapes. Specialties: Romance and seclusion. Activities: Snorkeling the excellent house reef, diving world-class sites nearby (like Rasdhoo Madivaru), spa treatments, water sports (windsurfing, catamaran sailing), sunset cruises, private sandbank dinners, yoga sessions, and marine biology talks. Perfect for honeymoons or couples seeking tranquility.",https://dreamoverwater.com/wp-content/uploads/2021/03/veliwvexterior.jpg,https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2e/08/32/e3/birds-eye-view-of-veligandu.jpg?w=900&h=500&s=1
Singapore,Marina Bay Sands,"Opened in 2010, Marina Bay Sands is an architectural icon of modern Singapore, designed by Moshe Safdie with three towers topped by the world's largest rooftop infinity pool and SkyPark. Part of the city's urban renewal. Specialties: Luxury integrated resort experience. Activities: Swim in the 150m infinity pool (hotel guests), visit the observation deck for 360° views, shop at The Shoppes luxury mall, dine at celebrity chef restaurants (like Gordon Ramsay's), try the casino, watch the free Spectra light and water show nightly, and explore the ArtScience Museum.",https://i.ytimg.com/vi/cFGr0m66X3Y/maxresdefault.jpg,https://safdie-staging.imgix.net/b27da03b-d334-4049-ba75-e3679385cb13/01_B-F_MBS-HS_16_SandsSP_4x3.jpg?auto=format%2Ccompress&q=50&ixlib=imgixjs-3.5.1
Singapore,Gardens by the Bay,"Gardens by the Bay, opened in 2012, is a 101-hectare futuristic horticultural park featuring iconic Supertrees (vertical gardens up to 50m), the cooled Cloud Forest dome with the tallest indoor waterfall, and the Flower Dome (largest glass greenhouse). Inspired by Singapore's 'City in a Garden' vision. Specialties: Innovative eco-architecture and nightly light shows. Activities: Walk the OCBC Skyway between Supertrees, watch Garden Rhapsody light and music show, explore themed gardens, visit seasonal floral displays, and enjoy dining with bay views. A blend of nature and technology.",https://www.gardensbythebay.com.sg/en/things-to-do/calendar-of-events/garden-rhapsody/_jcr_content/root/container/container_copy/container_340106661/image.coreimg.png/1663576157040/garden-rhapsody.png,https://upload.wikimedia.org/wikipedia/commons/5/5d/Supertree_Grove%2C_Gardens_by_the_Bay%2C_Singapore_-_20120712-02.jpg
Singapore,Sentosa Island,"Sentosa Island, once a British military fortress and WWII battle site, was transformed into a leisure destination in the 1970s. Now Singapore's premier playground. Specialties: Family entertainment and beaches. Activities: Thrill rides at Universal Studios Singapore, relax on Siloso/Palawan/Tanjong beaches, visit S.E.A. Aquarium, adventure at Mega Adventure Park (zipline), explore historical Fort Siloso, ride the cable car, watch Wings of Time show, and golf or cycle around the island. Endless fun for all ages.",https://daniaexperiences.com/wp-content/uploads/2021/09/img_5952-1280x853-1.jpg?w=1024,https://www.sentosa.com.sg/-/media/sentosa/article-listing/articles/2020/swimming-in-sentosa/swimmmingatsentosamain.jpg?revision=88869462-b375-48a5-91a7-07147f804532
Singapore,Singapore Zoo and Night Safari,"Singapore Zoo (opened 1973) pioneered open-concept habitats, while the adjacent Night Safari (1994) was the world's first nocturnal zoo. Both emphasize conservation and education. Specialties: Immersive wildlife experiences. Activities: Day zoo tram rides and walking trails, animal feeding shows, close encounters; Night Safari tram and walking trails to see nocturnal animals like tigers and flying squirrels, cultural performances, and creature features show. Rainforest vibes without barriers.",https://images.pexels.com/photos/7348123/pexels-photo-7348123.jpeg,https://images.pexels.com/photos/4483515/pexels-photo-4483515.jpeg
Singapore,Chinatown,"Singapore's Chinatown dates to the 1820s as an enclave for early Chinese immigrants, preserving heritage shophouses, temples, and clan associations amid modern bustle. Specialties: Authentic street food at Maxwell and Chinatown Complex hawker centres. Activities: Visit Buddha Tooth Relic Temple, explore Thian Hock Keng Temple, shop for souvenirs on Pagoda Street, night market browsing, heritage walking trails, try Michelin-starred hawker dishes like chicken rice, and cultural performances. Vibrant mix of history and flavors.",http://careergappers.com/wp-content/uploads/2019/09/The-Buddha-Tooth-Relic-Temple-1024x683.jpg,https://images.squarespace-cdn.com/content/v1/5b86a74dc258b486eea0a061/1547648265270-QX4PZF9YLFF6HWZVOTPB/Singapore+Chinatown-112.jpg
Thailand,Bangkok,"Bangkok, founded in 1782 as Thailand's new capital after Ayutthaya's fall, blends ancient royal heritage with chaotic modern energy along the Chao Phraya River. Famous for ornate temples and vibrant street life. Specialties: World-class street food and floating markets. Activities: Visit Grand Palace and Wat Phra Kaew (Emerald Buddha), recline at Wat Pho, river cruises, rooftop bars, Chatuchak weekend market shopping, Khao San Road nightlife, Muay Thai shows, and canal tours. A sensory overload of culture, cuisine, and chaos.",https://media.cntraveler.com/photos/5b9803300e566a7440f144ff/master/pass/Grand-Palace_Bangkok_GettyImages-931087118.jpg,https://cdn.britannica.com/59/252559-050-F959E5DC/Grand-palace-and-Wat-Phra-Keaw-Bangkok.jpg
Thailand,Phuket,"Phuket, Thailand's largest island with a tin-mining past influencing Sino-Portuguese Old Town architecture, boasts stunning beaches and lively nightlife. Tourism boomed post-1970s. Specialties: Fresh seafood and vibrant night markets. Activities: Relax on Patong/Kata/Karon beaches, visit Big Buddha statue, explore Phi Phi islands by speedboat, water sports, Phuket Fantasea show, ethical elephant sanctuaries, old town walking tours, and cabaret performances. Mix of relaxation and adventure.",https://images.goway.com/production/hero_image/iStock-1183240219.jpg,https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/The_Big_Buddha%2C_Phuket.jpg/1200px-The_Big_Buddha%2C_Phuket.jpg
Thailand,Chiang Mai,"Chiang Mai, founded in 1296 as the Lanna Kingdom capital, is surrounded by mountains and dotted with over 300 ancient temples. Known for ethical wildlife tourism shift. Specialties: Northern Thai cuisine like khao soi. Activities: Visit Wat Phra That Doi Suthep, ethical elephant sanctuaries, night bazaar shopping, trekking to hill tribes, Doi Inthanon National Park hikes, Thai cooking classes, lantern festivals (Yi Peng), and temple hopping. Serene cultural contrast to Bangkok.",https://www.jagsetter.com/wp-content/uploads/2020/11/Copy-of-Untitled-3.jpg,https://bodhi.travel/images/thailand/wat-phra-singh.jpg
Thailand,Krabi,"Krabi Province features dramatic limestone karsts rising from emerald waters, with Railay Beach a rock-climbing mecca accessible only by boat. Historical coastal trading post. Specialties: Adventure sports and island hopping. Activities: Rock climbing on Railay, kayaking through mangroves, island tours to Phi Phi/Hong Islands, Emerald Pool and hot springs visits, beach relaxation at Ao Nang, Tiger Cave Temple hike, night markets, and longtail boat adventures. Stunning natural beauty.",https://www.awaygowe.com/wp-content/uploads/2024/07/railay-beach-32-dsc_7836.jpg,https://holeinthedonut.com/wp-content/uploads/2021/05/Thailand-Krabi-Railay-Beach-West-with-Longtail-boats-1640x1100.jpg
Thailand,Pattaya,"Pattaya evolved from a fishing village to a major resort during the Vietnam War era when American troops used it for R&R, boosting nightlife. Specialties: Energetic Walking Street scene. Activities: Relax on Jomtien Beach, visit intricate wooden Sanctuary of Truth temple, Coral Island snorkeling, Nong Nooch Tropical Garden, water parks like Ramayana, floating market, cabaret shows, and golf courses. Lively mix of beach and entertainment.",https://dynamic-media-cdn.tripadvisor.com/media/photo-o/10/c1/5d/f9/pattaya-beach.jpg?w=1200&h=1200&s=1,https://upload.wikimedia.org/wikipedia/commons/f/fb/Santuaryoftruth2.jpg
Bhutan,Paro Taktsang (Tiger’s Nest Monastery),"Paro Taktsang, or Tiger's Nest, clings to a cliff 900m above Paro Valley, built in 1692 around caves where Guru Rinpoche meditated in the 8th century after flying there on a tigress. One of Bhutan's most sacred sites. Specialties: Spiritual trekking pilgrimage. Activities: Challenging 4-6 hour hike (horses available halfway), explore temple complexes, enjoy panoramic valley views, photography, and meditation. A profound cultural and physical experience.",https://www.culturaobscura.com/wp-content/uploads/2019/05/IMG_2030-Version-2-copy-1200x750.jpg,https://www.andbeyond.com/wp-content/uploads/sites/5/Bhutan-Paro-Tigers-Nest-6-Website-1920x1080-fill-gravityauto.jpg
Bhutan,Punakha Dzong,"Punakha Dzong, built in 1637-38 at the confluence of Pho Chu and Mo Chu rivers, is Bhutan's second oldest and most majestic fortress-monastery, former winter capital and site of royal coronations. Famous for intricate architecture and spring jacaranda blooms. Specialties: Historical and architectural grandeur. Activities: Explore ornate interiors (restricted areas), cross the cantilever bridge, attend festivals (Punakha Tshechu), riverside picnics, and photography. Serene and photogenic.",https://upload.wikimedia.org/wikipedia/commons/5/5a/Punakha_Dzong%2C_Bhutan_02.jpg,https://cdn.audleytravel.com/4458/3183/79/16029105-punakha-dzong-at-sunset.jpg
Bhutan,Thimphu (Buddha Dordenma Statue),"The 51-meter gilded Buddha Dordenma statue, completed in 2015 for the fourth king's 60th birthday, overlooks Thimphu Valley and houses 125,000 smaller Buddhas inside. Symbolizes peace and prosperity. Specialties: Panoramic city views. Activities: Drive or hike up for meditation, photography of the massive statue, valley overlooks, picnics, and combining with nearby attractions like Tashichho Dzong. Tranquil spot for reflection.",https://upload.wikimedia.org/wikipedia/commons/4/4e/Buddha_Dordenma.jpg,https://dynamic-media-cdn.tripadvisor.com/media/photo-o/11/bf/91/b7/buddha-point.jpg?w=900&h=-1&s=1
Bhutan,Dochula Pass,"Dochula Pass at 3,100m features 108 Druk Wangyal Chortens built in 2003 to honor soldiers from the 2003 Assam conflict, plus Druk Wangyal Lhakhang temple. On clear days, offers stunning 200° Himalayan views including Masang Gang. Specialties: Spiritual and scenic stop. Activities: Photography, short hikes around chortens, temple visits, tea at the cafe, and snow views in winter. Essential Paro-Thimphu route highlight.",https://www.andbeyond.com/wp-content/uploads/sites/5/Bhutan-Dochu-la-Pass-1365791744-Website-1920x1080-fill-gravityauto.jpg,https://tourbhutan.travel/wp-content/uploads/2023/11/1_Dochula_Pass-1.jpg
Bhutan,Phobjikha Valley (Gangtey),"Phobjikha Valley, a glacial U-shaped wetland, is the winter home (November-March) for endangered black-necked cranes migrating from Tibet, who traditionally circle Gangtey Monastery three times upon arrival. Features 17th-century Gangtey Gonpa. Specialties: Crane festival and pristine nature. Activities: Crane watching from hides, valley nature trails and hikes, monastery visits, cultural homestays, potato farming experiences, and birdwatching. Peaceful, unspoiled rural Bhutan.",https://dynamic-media-cdn.tripadvisor.com/media/photo-o/13/de/01/0d/visit-phobjikha-valley.jpg?w=900&h=-1&s=1,https://cdn.audleytravel.com/1050/750/79/15978917-phobjikha-valley-bhutan.webp
`;
        const results = Papa.parse(csvData, { header: true, skipEmptyLines: true });
        const allPlaces = results.data;
        const placesByCountry = {};
        allPlaces.forEach(place => {
          if (!placesByCountry[place.Country]) {
            placesByCountry[place.Country] = [];
          }
          placesByCountry[place.Country].push(place);
        });
        countryFilter.addEventListener('change', () => {
          const selectedCountry = countryFilter.value;
          placeFilter.innerHTML = '<option value="">Choose a place</option>';
          detailsBox.style.display = 'none';
          if (selectedCountry && placesByCountry[selectedCountry]) {
            placeFilter.disabled = false;
            placesByCountry[selectedCountry].forEach(place => {
              const opt = document.createElement('option');
              opt.value = place.Place;
              opt.textContent = place.Place;
              placeFilter.appendChild(opt);
            });
          } else {
            placeFilter.disabled = true;
          }
        });
        placeFilter.addEventListener('change', () => {
          const selectedPlaceName = placeFilter.value;
          if (!selectedPlaceName) {
            detailsBox.style.display = 'none';
            return;
          }
          const place = allPlaces.find(p => p.Place === selectedPlaceName);
          if (place) {
            placeName.textContent = place.Place;
            descriptionText.textContent = place.Description;
            imagesContainer.innerHTML = '';
            if (place.Image_URL_1 && place.Image_URL_1.trim()) {
              const img1 = document.createElement('img');
              img1.src = place.Image_URL_1;
              img1.alt = place.Place + ' - Image 1';
              img1.onerror = () => { img1.src = 'https://via.placeholder.com/800x500/fffff0/d35400?text=Image+Not+Available'; };
              img1.onclick = () => window.open(place.Image_URL_1, '_blank');
              imagesContainer.appendChild(img1);
            }
            if (place.Image_URL_2 && place.Image_URL_2.trim()) {
              const img2 = document.createElement('img');
              img2.src = place.Image_URL_2;
              img2.alt = place.Place + ' - Image 2';
              img2.onerror = () => { img2.src = 'https://via.placeholder.com/800x500/fffff0/d35400?text=Image+Not+Available'; };
              img2.onclick = () => window.open(place.Image_URL_2, '_blank');
              imagesContainer.appendChild(img2);
            }
            detailsBox.style.display = 'block';
            detailsBox.scrollIntoView({ behavior: 'smooth' });
          }
        });
      </script>
    </body>
    </html>
    '''
# ====================================
# Shreya's part ends here
# ====================================
# ====================================
# Rachana's Part Starts Here
# ====================================
travel_data = {
    "Thailand": {
        "Phuket": {"season": "Cool & Dry Season", "months": "November to April"},
        "Bangkok": {"season": "Dry & Pleasant Season", "months": "November to February"},
        "Pattaya": {"season": "Best Beach Season", "months": "November to May"}
    },
    "Maldives": {
        "Maafushi Island": {"season": "Dry Season", "months": "December to March"},
        "Vaadhoo Island": {"season": "Dry Season", "months": "January to March"},
        "Hanifaru Bay": {"season": "Manta Season", "months": "August to November"},
        "Banana Reef": {"season": "Calm Sea Months", "months": "January to April"},
        "Veligandu Island": {"season": "Dry Season", "months": "November to April"}
    },
    "Bhutan": {
        "Dochula Pass": {"season": "Spring / Autumn", "months": "March to May, September to November"},
        "Paro Taktsang": {"season": "Spring / Autumn", "months": "April to May, September to November"},
        "Phobjikha Valley": {"season": "Autumn", "months": "October to December"},
        "Punakha Dzong": {"season": "Spring", "months": "February to April"},
        "Thimphu": {"season": "Spring / Autumn", "months": "March to May, September to November"}
    },
    "Singapore": {
        "Sentosa Island": {"season": "Dry & Sunny Months", "months": "February to April"},
        "Marina Bay Sands": {"season": "Best Weather Months", "months": "February to August"},
        "Gardens by the Bay": {"season": "Festival Season", "months": "November to January"}
    }
}
@app.route('/season', methods=['GET', 'POST'])
def season():
    base_style = """
    <style>
        body{
            margin:0;
            min-height:100vh;
            font-family:'Poppins', sans-serif;
            background:linear-gradient(135deg,#ffb300,#ff9800,#ff7043);
            display:flex;
            justify-content:center;
            align-items:center;
        }
        .card{
            background:white;
            padding:50px 70px;
            border-radius:30px;
            box-shadow:0 25px 60px rgba(0,0,0,0.25);
            text-align:center;
            width:90%;
            max-width:600px;
        }
        h1{
            color:#e65100;
            font-size:42px;
            margin-bottom:30px;
        }
        p{
            font-size:22px;
            color:#444;
        }
        select, button{
            padding:18px 25px;
            font-size:20px;
            border-radius:18px;
            border:none;
            margin-top:20px;
            width:100%;
        }
        select{
            background:#fff3e0;
        }
        button{
            background:#ff6f00;
            color:white;
            cursor:pointer;
            font-weight:600;
        }
        button:hover{
            background:#e65100;
        }
        a{
            display:inline-block;
            margin-top:25px;
            text-decoration:none;
            color:white;
            background:#ff9800;
            padding:12px 35px;
            border-radius:25px;
            font-size:18px;
        }
        a:hover{
            background:#e65100;
        }
    </style>
    """

    if request.method == 'POST':
        country = request.form.get('country')
        place = request.form.get('place')

        if place:
            info = travel_data[country][place]
            return f"""
            <html><body>
            {base_style}
            <div class="card">
                <h1>{place}</h1>
                <p><b>Best Season:</b> {info['season']}</p>
                <p><b>Best Months:</b> {info['months']}</p>
                <a href="/season">Search Again</a>
                <br><br>
                <a href="/">Home</a>
            </div>
            </body></html>
            """

        places = travel_data.get(country, {})
        options = "".join(f"<option value='{p}'>{p}</option>" for p in places)

        return f"""
        <html><body>
        {base_style}
        <div class="card">
            <h1>Select Place in {country}</h1>
            <form method="post">
                <input type="hidden" name="country" value="{country}">
                <select name="place">
                    {options}
                </select>
                <button>Show Best Season</button>
            </form>
        </div>
        </body></html>
        """

    country_options = "".join(f"<option value='{c}'>{c}</option>" for c in travel_data)

    return f"""
    <html><body>
    {base_style}
    <div class="card">
        <h1>Select Country</h1>
        <form method="post">
            <select name="country">
                {country_options}
            </select>
            <button>Next</button>
        </form>
    </div>
    </body></html>
    """
# ====================================
# Rachana's Part Ends Here
# ====================================
if __name__ == '__main__':
    print("RouteAndRoam started → Explore to your heart's content!")
    app.run(debug=True)


