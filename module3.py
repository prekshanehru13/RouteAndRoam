import pandas as pd
import requests
from io import BytesIO
from PIL import Image
import re
import os

class PlacesModule:
    def __init__(self, csv_path="places.csv"):
        # Convert given path to absolute safe path
        csv_path = os.path.abspath(csv_path)

        print(f"Loading CSV from: {csv_path}")

        try:
            self.df = pd.read_csv(csv_path)

            # Clean column values correctly
            self.df["COUNTRY"] = (
                self.df["COUNTRY"].astype(str).str.strip().str.lower()
            )

            self.df["PLACE"] = (
                self.df["PLACE"].astype(str).str.strip().str.lower()
            )

        except FileNotFoundError:
            print(f"ERROR: Could not find the file: {csv_path}")
            self.df = pd.DataFrame()

    def normalize(self, text):
        text = re.sub(r"\s+", " ", text)
        return text.strip().lower()

    def list_places_by_country(self, country):
        if self.df.empty:
            return []

        c = self.normalize(country)
        rows = self.df[self.df["COUNTRY"] == c]

        return rows["PLACE"].tolist()

    def get_place_info(self, country, place):
        if self.df.empty:
            return None

        c = self.normalize(country)
        p = self.normalize(place)

        row = self.df[(self.df["COUNTRY"] == c) & (self.df["PLACE"] == p)]

        if row.empty:
            return None

        return row.iloc[0].to_dict()

    def show_image(self, url):
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content))
            img.show()

        except Exception as e:
            print("Could not load image:", e)
