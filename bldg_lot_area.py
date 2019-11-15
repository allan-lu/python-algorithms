import matplotlib.pyplot as plt
import json

path = "INSERT PATH TO FILE"

with open(path) as f:
    data = f.read()
    d = json.loads(data)
    area_dic = {}
    for feature in d["features"]:
        for area in feature["properties"]:
            if area in area_dic:
                area_dic[area] += feature["properties"][area]
            else:
                area_dic[area] = 0
        points = feature["geometry"]["coordinates"][0][0]
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        plt.plot(x, y)
    del area_dic["zipcode"]
    for area in area_dic:
        print('The total', area, 'is', format(area_dic[area], ',d'), 'square feet.')
plt.show()
