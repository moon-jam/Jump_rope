import json

def write(gmail, name):
    with open("data/mail_name.json", 'r') as f:
        content = json.load(f)
    input = {gmail:name}
    content.update(input)
    with open("data/mail_name.json", 'w') as f_new:
        json.dump(content, f_new)
