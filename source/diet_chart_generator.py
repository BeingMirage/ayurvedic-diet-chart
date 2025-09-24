import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
import random

class DietChartGenerator:
    def __init__(self, df):
        self.df = df.copy()

        # Create a combined feature string from rasa, virya, vipaka
        self.df["features"] = (
            self.df["Rasa"].astype(str) + " " +
            self.df["Virya"].astype(str) + " " +
            self.df["Vipaka"].astype(str)
        )

        # Vectorize text features
        self.vectorizer = CountVectorizer()
        self.X = self.vectorizer.fit_transform(self.df["features"])

        # Train Nearest Neighbors model
        self.model = NearestNeighbors(n_neighbors=5, metric="cosine")
        self.model.fit(self.X)

    def get_similar_foods(self, food_name, n=5):
        """
        Find similar foods to the given one using ML (cosine similarity).
        """
        try:
            idx = self.df[self.df["Food"] == food_name].index[0]
        except IndexError:
            return []

        distances, indices = self.model.kneighbors(self.X[idx], n_neighbors=n)
        similar_foods = self.df.iloc[indices[0]]["Food"].tolist()
        return similar_foods

    def generate_diet(self, prakriti="Vata", days=7):
        """
        Generate a structured diet plan using Ayurveda + ML similarity.
        """
        recommendations = []

        # Filter by prakriti compatibility
        if prakriti == "Vata":
            subset = self.df[self.df["Dosha_Effect"].str.contains("Balances Vata")]
        elif prakriti == "Pitta":
            subset = self.df[self.df["Dosha_Effect"].str.contains("Balances Pitta")]
        elif prakriti == "Kapha":
            subset = self.df[self.df["Dosha_Effect"].str.contains("Balances Kapha")]
        else:
            subset = self.df

        if subset.empty:
            subset = self.df  # fallback

        # Generate meals for each day
        for day in range(1, days + 1):
            # Pick a random "seed" food
            seed_food = random.choice(subset["Food"].tolist())
            similar_foods = self.get_similar_foods(seed_food, n=5)

            # Assign meals (if not enough, fallback to seed_food)
            meals = similar_foods if len(similar_foods) >= 4 else [seed_food] * 4

            day_plan = {
                "Day": day,
                "Breakfast": meals[0],
                "Lunch": meals[1],
                "Snacks": meals[2],
                "Dinner": meals[3],
                "Notes": "1 cup of milk can be taken before/after 2 hours of meals. Drink warm water sip by sip."
            }
            recommendations.append(day_plan)

        return recommendations
