import json
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"]
)

redis = get_redis_connection(
    host="red-cqra9k56l47c73ebbuv0",
    port=6379
)

class Recipe(HashModel):
    name: str
    description: str
    ingredients: str  # Store serialized list of dicts

    class Meta:
        database = redis

# Updated RecipeCreateRequest model
class Ingredient(BaseModel):
    ingredient: str
    amount: str
    unit: str

class RecipeCreateRequest(BaseModel):
    name: str
    description: str
    ingredients: list[Ingredient]

@app.post("/recipes")
def create_recipe(recipe: RecipeCreateRequest):
    # Serialize the list of ingredients into a JSON string
    recipe_data = Recipe(
        name=recipe.name,
        description=recipe.description,
        ingredients=json.dumps([ingredient.model_dump() for ingredient in recipe.ingredients])
    )
    recipe_data.save()
    return recipe_data

@app.get("/recipes")
def get_recipe_names():
    return [format_recipe_name(pk) for pk in Recipe.all_pks()]

@app.delete("/recipes/{pk}")
def del_recipe(pk: str):
    return Recipe.delete(pk)

@app.get("/recipes/{pk}")
def get_recipe(pk: str):
    return format_recipe(pk)

# Updated formatting functions
def format_recipe(pk: str):
    a_recipe = Recipe.get(pk)
    ingredient_list = json.loads(a_recipe.ingredients)  # Deserialize the ingredients list

    return {
        "id": a_recipe.pk,
        "name": a_recipe.name,
        "description": a_recipe.description,
        "ingredients": ingredient_list
    }

def format_recipe_name(pk: str):
    a_recipe = Recipe.get(pk)
    return {
        "id": a_recipe.pk,
        "name": a_recipe.name,
        "description": a_recipe.description
    }