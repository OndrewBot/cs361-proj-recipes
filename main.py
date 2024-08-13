import json
from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
    ingredients: str  # Store serialized list
    amounts: str  # Store serialized list
    units: str  # Store serialized list

    class Meta:
        database = redis

@app.post("/newrecipe")
def create_recipe(name: str, description: str, ingredients: list[str], amounts: list[str], units: list[str]):
    recipe = Recipe(
        name=name, 
        description=description, 
        ingredients=json.dumps(ingredients),
        amounts=json.dumps(amounts), 
        units=json.dumps(units)
    )
    recipe.save()
    return recipe

@app.get("/recipes/{pk}")
def get_recipe(pk: str):
    return format_recipe(pk)

@app.get("/recipes")
def get_recipe_names():
    return [format_recipe_name(pk) for pk in Recipe.all_pks()]

def format_recipe(pk: str):
    a_recipe = Recipe.get(pk)
    ingredient_list = json.loads(a_recipe.ingredients)
    amount_list = json.loads(a_recipe.amounts)
    unit_list = json.loads(a_recipe.units)

    ingredients = []
    for i in range(len(ingredient_list)):
        ingredients.append({
            "ingredient": ingredient_list[i],
            "amount": amount_list[i],
            "unit": unit_list[i]
        })

    return {
        "id": a_recipe.pk,
        "name": a_recipe.name,
        "description": a_recipe.description,
        "ingredients": ingredients
    }

def format_recipe_name(pk: str):
    a_recipe = Recipe.get(pk)
    return {
        "id": a_recipe.pk,
        "name": a_recipe.name,
        "description": a_recipe.description
    }
