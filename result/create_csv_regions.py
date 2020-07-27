import csv
from imitation import parser

data = parser.get_options(parser.driver.page_source, "region")[0]
print(type(data))

filename = "regions.csv"

with open(filename, 'w') as csvfile:
    csvwriter = w = csv.DictWriter(csvfile, data[0].keys())
    csvwriter.writeheader()
    csvwriter.writerows(data)
