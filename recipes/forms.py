from django import forms
from django.core.exceptions import ValidationError

from .models import Recipe, Tag, Ingredient
from .service import add_ingredients_to_recipe


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        label='Теги',
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    ingredients = forms.CharField(
        required=False,
        label='Ингредиенты',
        widget=forms.TextInput(attrs={'id': 'nameIngredient'}),
    )

    class Meta:
        model = Recipe
        fields = (
            'title',
            'tags',
            'ingredients',
            'cooking_time',
            'text',
            'image',
        )
        labels = {
            'title': 'Название рецепта',
            'text': 'Рецепт',
            'cooking_time': 'Время приготовления',
            'image': 'Загрузить фото',
        }
        widgets = {
            'cooking_time': forms.TextInput(),
        }

    def clean_ingredients(self):
        ingredients = list(
            zip(
                self.data.getlist('nameIngredient'),
                self.data.getlist('valueIngredient'),
            ),
        )
        if not ingredients:
            raise forms.ValidationError('Отсутствуют ингредиенты')

        all_ingredients = Ingredient.objects.all()
        ingredients_clean = []
        for name, quantity in ingredients:
            if not all_ingredients.filter(title=name):
                raise ValidationError(
                    f'В базе данных нет ингредиента "{name}".')
            if int(quantity) < 1:
                raise forms.ValidationError(
                    f'Исправьте количество ингредиента "{name}"')
            else:
                ingredients_clean.append({
                    'title': name,
                    'quantity': quantity,
                })
        return ingredients_clean

    # def clean_cooking_time(self):
    #     cooking_time =

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        ingredients = self.cleaned_data['ingredients']
        self.cleaned_data['ingredients'] = []
        self.save_m2m()
        add_ingredients_to_recipe(self.instance, ingredients)

        return instance
