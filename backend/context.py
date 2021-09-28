import csv
from recipes.models import Ingredient

CSV_PATH = 'C:/dev/recipes/food/data/ingredients.csv'

with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader1 = csv.reader(csvfile, delimiter=",")
    for row in reader1:
        Ingredient.objects.create(name=row[0], measurement_unit=row[1])
