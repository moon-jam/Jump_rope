import json

def re_rank():
    with open("data/ranking.json", 'r') as f:
        content = json.load(f)

    # Rank
    sorted_content = {}
    sorted_filenames = sorted(content.keys(), key=lambda x: content[x][0]["score"], reverse=True)

    for idx, filename in enumerate(sorted_filenames):
        content[filename][0]["ranking"] = idx + 1
        sorted_content[filename] = content[filename]

    with open("data/ranking.json", 'w') as f_new:
        json.dump(sorted_content, f_new)

def write(file, score):
    with open("data/ranking.json", 'r') as f:
        content = json.load(f)
    input = {file:[{"score":score, "ranking":0}]}
    content.update(input)
    with open("data/ranking.json", 'w') as f_new:
        json.dump(content, f_new)
    re_rank()

if __name__ == '__main__':
    re_rank()
