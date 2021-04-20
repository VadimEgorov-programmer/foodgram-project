from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv
import logging

logging.basicConfig(filename='debug.log', level=logging.INFO)


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('recipes/data/ingredients.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                title, dimension = row
                Ingredient.objects.get_or_create(title=title,
                                                 dimension=dimension)
                logging.info(f'Добавлен ингредиент {row}')
