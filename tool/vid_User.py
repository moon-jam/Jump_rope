import json

def write(file, gmail, name):
    with open("data/vid_User.json", 'r') as f:
        content = json.load(f)
    input = {file:gmail}
    content.update(input)
    with open("data/vid_User.json", 'w') as f_new:
        json.dump(content, f_new)
