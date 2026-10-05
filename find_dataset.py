import json
import glob

for file in glob.glob('**/*.json', recursive=True):
    if 'node_modules' in file:
        continue
    try:
        data = json.load(open(file, encoding='utf-8'))
        if isinstance(data, list):
            print(f'{file}: {len(data)} items')
        elif isinstance(data, dict):
            if 'insights' in data:
                print(f'{file}: {len(data["insights"])} insights')
            else:
                print(f'{file}: keys -> {list(data.keys())}')
    except Exception as e:
        pass
