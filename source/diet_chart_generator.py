import random

class DietChartGenerator:
    def __init__(self, df):
        self.df = df.copy()

    def generate_diet(self, prakriti="Vata", days=7):
        """
        Generate a diet chart in structured format (Breakfast, Lunch, Snacks, Dinner).
        """
        recommendations = []

        # Filter based on prakriti (basic Ayurvedic rules)
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

        for day in range(1, days + 1):
            day_plan = {
                "Day": day,
                "Breakfast": random.choice(subset["Food"].tolist()),
                "Lunch": random.choice(subset["Food"].tolist()),
                "Snacks": random.choice(subset["Food"].tolist()),
                "Dinner": random.choice(subset["Food"].tolist()),
                "Notes": "1 cup of milk can be taken before/after 2 hours of meals. Drink warm water sip by sip."
            }
            recommendations.append(day_plan)

        return recommendations
