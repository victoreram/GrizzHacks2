from flask import Flask
from flask_ask import Ask, statement, question
import logging
import json



app = Flask(__name__)
ask = Ask(app, "/")
log = logging.getLogger('flask_ask').setLevel(logging.DEBUG)

with open("data.json") as data:
    FOOD_DB = json.load(data)


@app.route("/")
def hello():
    return "Hello World!"


@ask.launch
def start_skill():
    return question("What were you planning to eat?")\
        .reprompt("I'm sorry, I didn't get that.")


@ask.intent("food_intent")
def yes_intent(food):
    if food == "Ursula":
        return statement("{} is pretty and smart. Plus she has a nice butt!"
                         .format(food))
    elif food == "mayonnaise":
        return statement("{} is vile and eating it should be punishable by "
                         "death!".format(food))
    elif food in FOOD_DB:
        carb = FOOD_DB[food]['carb']
        cal = FOOD_DB[food]['cal']/100
        fat = FOOD_DB[food]['fat']
        sugar = FOOD_DB[food]['sugar']
        fiber = FOOD_DB[food]['fiber']
        sodium = FOOD_DB[food]['sodium']
        protein = FOOD_DB[food]['protein']
        highest = max(carb, cal, fat, protein, sugar, fiber, sodium)
        if food[-1] == 's':
            verb = "are"
        else:
            verb = "is"
            if highest == carb or highest == protein:
                max_val = ('carbohydrates' if carb == max(carb, protein) else "protein")
                return statement("{} {} high in {}. This fits into your diet"
                                 .format(food, verb, max_val))
            elif highest == fiber or highest == protein:
                max_val = ('fiber' if fiber == max(fiber, protein) else "protein")
                return statement("{} {} high in {}. This fits into your diet"
                                 .format(food, verb, max_val))
            elif highest == sugar:
                return statement("{} {} high in {}. This does not fit into your diet"
                                 .format(food, verb, 'sugar'))
            else:
                max_val = ('fat' if fat == max(fat, cal) else "calories")
                return statement("{} {} high in {}. This does not fit into your"
                                 " diet".format(food, verb, max_val))
    return question("Sorry, I don't have any information on that. What "
                    "were you planning to eat?")\
        .reprompt("Please repeat the request or choose a different item.")


@ask.intent("no_intent")
def no_intent():
    return statement("Then why did you bother me then?")


if __name__ == '__main__':
    app.run(debug=True)
