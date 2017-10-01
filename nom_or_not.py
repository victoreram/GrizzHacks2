from flask import Flask
from flask_ask import Ask, statement, question
import logging
import json



app = Flask(__name__)
ask = Ask(app, "/")
log = logging.getLogger('flask_ask').setLevel(logging.DEBUG)

with open("basic.json") as df:
    FOOD_DB = json.load(df)


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
        carb = FOOD_DB[food]['carbs']
        cal = FOOD_DB[food]['calories']
        fat = FOOD_DB[food]['fat']
        pro = FOOD_DB[food]['pro']
        highest = max(carb, cal, fat, pro)
        if food[-1] == 's':
            verb = "are"
        else:
            verb = "is"
            if highest == carb or highest == pro:
                max_val = ('carbs' if carb == max(carb, pro) else "pro")
                return statement("{} {} high in {}. This fits into your diet"
                                 .format(food, verb, max_val))
            else:
                max_val = ('fat' if fat == max(fat, cal) else "calories")
                return statement("{} {} high in {}. This does not fit into your"
                                 " diet".format(food, verb, max(fat, cal)))
    return question("Sorry, I don't have any information on that. What "
                    "were you planning to eat?")\
        .reprompt("Please repeat the request or choose a different item.")


@ask.intent("no_intent")
def no_intent():
    return statement("Then why did you bother me then?")


if __name__ == '__main__':
    app.run(debug=True)
