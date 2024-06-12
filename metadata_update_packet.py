import pandas as pd
import os

df = pd.read_csv("merritt-updates/palmu_metadata_delivery1-merrit-update.csv")

path = "/Users/ngoziharrison/Documents/palmu-data/merritt-updates"

txt_template = """erc: 
what:{six}
what:{seven}
where: {one}
where: {two}
where: {three}
where: {four}
where: {five}
"""

for index, row in df.head(5).iterrows():
    folder = row["where"]
    print(folder)
    os.mkdir(os.path.join(path, folder))

    with open(path + "/" + folder + "/mrt-erc.txt", "w") as file:
        file.write(txt_template.format(six = row[5], seven = row[6], one = row[0], two = row[1], three = row[2], four = row[3], five = row[4]))