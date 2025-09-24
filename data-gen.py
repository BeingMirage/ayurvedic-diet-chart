import google.generativeai as genai
import pandas as pd
import random
import time

# -----------------------------
# 1. Setup Gemini API
# -----------------------------
API_KEY = "AIzaSyBfWQalzeXnTMrGuvd9Fl2_5nNCj_FWkNE"   # <<-- hardcode your key here
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------
# 2. Seed Recipe List
# -----------------------------
recipes = [
    "Palak Paneer", "Aloo Paratha", "Gobhi Masala", "Veg Biryani",
    "Paneer Sandwich", "Masala Dosa", "Pasta Alfredo", "Veg Burger",
    "Dal Tadka", "Chole Bhature", "Idli Sambar", "Veg Fried Rice",
    "Rasgulla", "Mango Lassi", "Quinoa Salad", "Miso Soup",
    "Avocado Toast", "Falafel Wrap", "Sushi Roll", "Veggie Pizza"
]

# -----------------------------
# 3. Variation dictionary
# -----------------------------
variation_map = {
    "pizza": ["Paneer Pizza", "Mushroom Pizza", "Vegan Pizza", "Cheese Burst Pizza", "Margherita Pizza"],
    "dosa": ["Masala Dosa", "Mysore Dosa", "Paneer Dosa", "Onion Dosa", "Cheese Dosa"],
    "biryani": ["Hyderabadi Biryani", "Veg Biryani", "Paneer Biryani", "Mushroom Biryani", "Lucknowi Biryani"],
    "pasta": ["Alfredo Pasta", "Arrabbiata Pasta", "Pesto Pasta", "Carbonara Pasta", "Veggie Pasta"],
    "paneer": ["Palak Paneer", "Paneer Butter Masala", "Chili Paneer", "Shahi Paneer", "Paneer Tikka Masala"],
    "curry": ["Veg Curry", "Chickpea Curry", "Tofu Curry", "Spinach Curry", "Mixed Veg Curry"],
    "burger": ["Veg Burger", "Paneer Burger", "Cheese Burger", "Mushroom Burger", "Grilled Veggie Burger"],
    "paratha": ["Aloo Paratha", "Paneer Paratha", "Methi Paratha", "Onion Paratha", "Mix Veg Paratha"],
    "fried rice": ["Veg Fried Rice", "Paneer Fried Rice", "Egg Fried Rice", "Mushroom Fried Rice", "Schezwan Fried Rice"],
    "sandwich": ["Paneer Sandwich", "Veg Sandwich", "Grilled Cheese Sandwich", "Club Sandwich", "Spinach Corn Sandwich"]
}

generic_cooking_styles = ["Spicy", "Mild", "Fried", "Baked", "Grilled", "Steamed"]
generic_health_tags = ["Low-fat", "Vegan", "Gluten-free", "Protein-rich", "Keto", "Ayurvedic"]
generic_regions = ["Punjabi", "South Indian", "North Indian", "Mediterranean-style", "Italian-style", "Thai-style"]

def generate_variations(dish, num_variants=3):
    dish_lower = dish.lower()
    variants = []

    # Check if dish has a mapped variation set
    for key, mapped_variants in variation_map.items():
        if key in dish_lower:
            variants.extend(random.sample(mapped_variants, min(num_variants, len(mapped_variants))))
            break
    else:
        # Fallback: generic variations
        for _ in range(num_variants):
            variant = []
            if random.random() < 0.5:
                variant.append(random.choice(generic_cooking_styles))
            if random.random() < 0.5:
                variant.append(random.choice(generic_health_tags))
            if random.random() < 0.5:
                variant.append(random.choice(generic_regions))
            variant_name = " ".join(variant + [dish])
            variants.append(variant_name.strip())

    return list(set(variants))  # unique only

# -----------------------------
# 4. Gemini batch function
# -----------------------------
def get_batch_ayurvedic_properties(dish_list):
    dish_text = "\n".join([f"{i+1}. {dish}" for i, dish in enumerate(dish_list)])
    prompt = f"""
    You are an Ayurveda expert. Classify the following recipes into their Ayurvedic properties.

    For each dish, return data in **CSV row style** (no extra text):
    Food,Rasa,Virya,Vipaka,Dosha_Effect

    Rasa: choose from [Sweet, Sour, Salty, Pungent, Bitter, Astringent] (can be multiple, comma separated)
    Virya: Heating or Cooling
    Vipaka: Sweet, Sour, or Pungent
    Dosha_Effect: describe effect, e.g., "Balances Vata and Pitta, Increases Kapha"

    Recipes:
    {dish_text}

    Now return only rows in this format, one per recipe.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip().splitlines()
    except Exception as e:
        print(f"⚠️ API error: {e}")
        return []

# -----------------------------
# 5. Dataset generation
# -----------------------------
data = []
row_id = 1
target_rows = 5000
batch_size = 20

while len(data) < target_rows:
    # Pick base dish
    base_dish = recipes[(len(data) // batch_size) % len(recipes)]
    # Create authentic + generic variations
    batch = [base_dish] + generate_variations(base_dish, num_variants=batch_size-1)

    results = get_batch_ayurvedic_properties(batch)

    for row in results:
        try:
            parts = row.split(",")
            if len(parts) < 5:
                continue
            food = parts[0].strip()
            rasa = parts[1].strip()
            virya = parts[2].strip()
            vipaka = parts[3].strip()
            dosha = ",".join(parts[4:]).strip()

            data.append([row_id, food, rasa, virya, vipaka, dosha])
            row_id += 1

            print(f"✅ Added: {food}")
            if len(data) >= target_rows:
                break
        except Exception as parse_error:
            print(f"⚠️ Parse error for row: {row} | {parse_error}")
    
    time.sleep(1)

# -----------------------------
# 6. Save CSV
# -----------------------------
df = pd.DataFrame(data, columns=["S.No", "Food", "Rasa", "Virya", "Vipaka", "Dosha_Effect"])
df.to_csv("recipes_dataset_gemini_smart_variations.csv", index=False, encoding="utf-8")

print(f"🎉 Dataset generated: recipes_dataset_gemini_smart_variations.csv with {len(df)} rows.")
