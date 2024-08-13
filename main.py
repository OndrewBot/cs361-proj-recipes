from typing import Optional
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['*'],
    allow_credentials=True,
    allow_headers=['*']
)

redis = get_redis_connection(
    host="red-cqra9k56l47c73ebbuv0",
    port=6379
)

class Recipe(HashModel):
    name: str
    description: str
    ingredients: list[str]  # This will store ingredient names or keys
    amounts: list[str]  # Amounts corresponding to ingredients
    units: list[str]  # Units corresponding to ingredients

    class Meta:
        database = redis

# FastAPI app for managing recipes
@app.post("/newrecipe")
def create_recipe(name: str, description: str, ingredients: list[str], amounts: list[str], units: list[str]):
    recipe = Recipe(name=name, ingredients=ingredients, amounts=amounts, units=units)
    recipe.save()
    return recipe

@app.get("/recipes/{pk}")
def get_recipe(pk: str):
    return format(pk)

@app.get("/recipes")
def get_recipe_names(pk: str):
    return [format_names(pk) for pk in Recipe.all_pks()]

def format(pk: str):
    a_recipe = Recipe.get(pk)
    ingredient_list = []
    for i in range(len(a_recipe.ingredients)):
        ingredient_list.append({a_recipe.ingredients[i], a_recipe.amounts[i], a_recipe.units[i]})

    return {
        'id': a_recipe.pk,
        'name': a_recipe.name,
        'description': a_recipe.description,
        'ingredients': ingredient_list
    }

def format_names(pk: str):
    a_recipe = Recipe.get(pk)
    return {
        'id': a_recipe.pk,
        'name': a_recipe.name,
        'description': a_recipe.description
    }