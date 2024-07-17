from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.title

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    amount = models.CharField(max_length=100)

def __str__(self):
    return f'{self.amount} of {self.name}'

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='instructions', on_delete=models.CASCADE)
    step = models.IntegerField()
    text = models.TextField()

def __str__(self):
    return f'Step {self.step}: {self.text}'