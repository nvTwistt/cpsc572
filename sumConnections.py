import json
convertedDict = {}
with open("degrees.txt", "r") as file:
    file_content = file.read()
    print(file_content)
    convertedDict = json.loads(file_content)

