from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Recipe, Ingredient, Instruction

class RecipeListView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        data = []

        for recipe in recipes:
            recipe_data = {
                'id': recipe.id,
                'title': recipe.title,
                'description': recipe.description,
                'created_at': recipe.created_at,
                'ingredients': [
                    {'name': ingredient.name, 'amount': ingredient.amount}
                    for ingredient in recipe.ingredients.all()
                ],
                'instructions': [
                    {'step': instruction.step, 'text': instruction.text}
                    for instruction in recipe.instructions.all()
                ]
            }
            data.append(recipe_data)

        return JsonResponse(data, safe=False)

    @method_decorator(csrf_exempt)
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        title = data.get('title', '')
        description = data.get('description', '')
        ingredients_data = data.get('ingredients', [])
        instructions_data = data.get('instructions', [])

        # Create a new recipe
        new_recipe = Recipe.objects.create(title=title, description=description)

        # Create ingredients
        for ingredient_data in ingredients_data:
            name = ingredient_data.get('name', '')
            amount = ingredient_data.get('amount', '')
            Ingredient.objects.create(recipe=new_recipe, name=name, amount=amount)

        # Create instructions
        for instruction_data in instructions_data:
            step = instruction_data.get('step', 0)
            text = instruction_data.get('text', '')
            Instruction.objects.create(recipe=new_recipe, step=step, text=text)

        # Return the created recipe data
        response_data = {
            'id': new_recipe.id,
            'title': new_recipe.title,
            'description': new_recipe.description,
            'ingredients': [
                {'name': ingredient.name, 'amount': ingredient.amount}
                for ingredient in new_recipe.ingredients.all()
            ],
            'instructions': [
                {'step': instruction.step, 'text': instruction.text}
                for instruction in new_recipe.instructions.all()
            ]
        }
        return JsonResponse(response_data, status=201)

class RecipeDetailView(View):
    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        ingredients = list(recipe.ingredients.values('name', 'amount'))
        instructions = list(recipe.instructions.values('step', 'text'))

        data = {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': ingredients,
            'instructions': instructions,
        }
        return JsonResponse(data)

    @method_decorator(csrf_exempt)
    def put(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        data = json.loads(request.body.decode('utf-8'))
        recipe.title = data.get('title', recipe.title)
        recipe.description = data.get('description', recipe.description)
        recipe.save()

        # Return updated recipe data
        response_data = {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
        }
        return JsonResponse(response_data)

    @method_decorator(csrf_exempt)
    def delete(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.delete()
        return JsonResponse({'message': f'Recipe {pk} deleted'}, status=204)