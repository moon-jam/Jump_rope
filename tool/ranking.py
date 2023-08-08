import json

def re_rank(content):
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
    input_data = {file: [{"score": score, "ranking": 0}]}
    content.update(input_data)
    re_rank(content)
    rank = content[file][0]["ranking"]
    return rank

def get_ranking(file):
    with open("data/ranking.json", 'r') as f:
        content = json.load(f)
    rank = content[file][0]["ranking"]
    return rank

if __name__ == '__main__':
    with open("data/ranking.json", 'r') as f:
        content = json.load(f)
    re_rank(content)
