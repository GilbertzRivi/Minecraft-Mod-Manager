import os, json

def read(file_path, binary = False):
    file_path = os.path.join(f'{os.path.dirname(os.path.abspath(__file__))}', file_path)
    if binary:
        with open(file_path, 'rb') as f:
            data = f.read()
    else:
        with open(file_path) as f:
            data = f.read()
    return data

def write(file_path, data, binary = False):
    file_path = os.path.join(f'{os.path.dirname(os.path.abspath(__file__))}', file_path)
    if binary:
        with open(file_path, 'wb') as f:
            f.write(data)
    else:
        with open(file_path, 'w') as f:
            f.write(data)

def dict_add(data, place, content, update = True):
    copy = data
    if len(place) == 0:
        data.update(content)
    else:
        for i in place:
            copy = copy[i]
        if update:
            copy.update(content)
        else:
            copy = content
    return data

def dict_rem(data, place):
    copy = data
    if len(place) == 1:
        del data[place[0]]
    else:
        for i in place[:-1]:
            copy = copy[i]
        del copy[place[-1]]

def json_load(path):
    return json.loads(read(path))

def json_save(data, path):
    write(path, json.dumps(data, indent=4, sort_keys=True))