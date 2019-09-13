import os
import random
piece_length = 300
train_frac = 0.92
save_path = 'oroscopo-data'

oroscopo_datapath = '../char-rnn/data/oroscopo/input.txt'
wiki_dir = '../spider/scrapy/data/'


def load_wiki(path):
    data = ''
    files = os.listdir(path)
    for name in files:
        if name.endswith('.txt'):
            with open(os.path.join(path, name)) as f:
                data += f.read()
    return data


def load_input(path):
    with open(path) as f:
        return f.read()


def split(text, label):
    final = []
    for i in range(0, len(text), piece_length):
        start = i
        end = i + piece_length
        text_piece = text[start:end] if end < len(text) else text[start:]
        final.append('__label__' + label + ' ' + text_piece)
    return final


wiki = load_wiki(wiki_dir).replace('\n', ' ')
inpu = load_input(oroscopo_datapath).replace('\n', ' ')

print(len(wiki), len(inpu))

pwiki = split(wiki, 'useless')
pinpu = split(inpu, 'oroscopo')

total = pwiki + pinpu
random.shuffle(total)

train_count = int(len(total) * train_frac)
print(f"Saving {train_count} labels for training, {len(total) - train_count} for validation")
with open(os.path.join(save_path, 'oroscopo.train'), 'w') as f:
    f.write('\n'.join(total[:train_count]))
with open(os.path.join(save_path, 'oroscopo.valid'), 'w') as f:
    f.write('\n'.join(total[train_count:]))
