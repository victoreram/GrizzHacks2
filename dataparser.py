import csv
import json
import re



with open("Recipes/nutrition.csv", encoding = "ISO-8859-1") as in_file, \
     open("data.json", "w") as out_file:
    inreader = csv.reader(in_file)


    data = {}
    next(inreader)
    for line in inreader:
        try:
            grp = re.search(r"(\d* g)", line[12])
            serv = float(grp[0][:-2]) if grp else 1
            fat = float(line[26]) / serv if line[26] else 0
            carb = float(line[38]) / serv if line[38] else 0
            sugar = float(line[39]) / serv if line[39] else 0
            fiber = float(line[44]) / serv if line[44] else 0
            protein = float(line[45]) / serv if line[45] else 0
            sodium = float(line[47]) / serv if line[47] else 0
            cal = 9 * fat + 4 * carb + 4 * protein

            data[line[1].strip().lower()] = {"serv": line[12], "cal": cal, "fat": fat, "carb": carb,
                             "sugar": sugar, "fiber": fiber, "protein": protein,
                             "sodium": sodium}
        except:
            print("bad unicode")

    json.dump(data, out_file)
