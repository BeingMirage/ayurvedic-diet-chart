from data_loader import load_dataset
from diet_chart_generator import DietChartGenerator
from pdf_exporter import export_to_pdf

def main():
    # Load dataset
    df = load_dataset()

    # Initialize generator
    generator = DietChartGenerator(df)

    # Doctor input
    prakriti = input("Enter patient's prakriti (Vata/Pitta/Kapha): ").strip().capitalize()
    days = int(input("Enter number of days for the diet chart: "))

    # Generate chart
    diet_chart = generator.generate_diet(prakriti=prakriti, days=days)

    # Print to console (structured format)
    for day in diet_chart:
        print(f"\nDay {day['Day']}:")
        print(f"  Breakfast: {day['Breakfast']}")
        print(f"  Lunch: {day['Lunch']}")
        print(f"  Mid Evening Snacks: {day['Snacks']}")
        print(f"  Dinner: {day['Dinner']}")
        print(f"  Note: {day['Notes']}")

    # Export to PDF
    export_to_pdf(diet_chart, filename="diet_chart.pdf")

if __name__ == "__main__":
    main()
