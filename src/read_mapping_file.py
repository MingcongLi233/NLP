import csv

def read_mapping_file(file):
    keywords = []
    mapping = {}
    with open(file, 'r') as map_file:
        reader = csv.reader(map_file)
        for row in reader:
            keywords.append(row[0])
            mapping[row[0]] = row[1]
        return (keywords, mapping)