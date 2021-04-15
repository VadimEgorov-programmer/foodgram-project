from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Подключать для логирования чтобы не было ошибки
        # file was loaded in the wrong encoding: 'UTF-8'
        # with open('recipes/data/ingredients.csv') as file:
        with open('recipes/data/ingredients.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                title, dimension = row
                Ingredient.objects.get_or_create(title=title,
                                                 dimension=dimension)
                # logger.debug(row)  # Логирование
