from flask import Flask, render_template, request

app = Flask(__name__)

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

@app.route('/')
def home():
    return render_template("home.html", countries=travel_data)

@app.route('/places', methods=['POST'])
def places():
    country = request.form.get("country")

    if country not in travel_data:
        return render_template("home.html", countries=travel_data, error="Invalid Country Selected")

    return render_template("places.html", country=country, places=travel_data[country])

@app.route('/result', methods=['POST'])
def result():
    country = request.form.get("country")
    place = request.form.get("place")

    info = travel_data[country][place]

    return render_template("result.html", country=country, place=place, info=info)

if __name__ == "__main__":
    app.run(debug=True)
