import fasttext
import html
import numpy as np
from matplotlib import pyplot as plt

block_size = 256

with open('articolo.txt') as f:
    data = f.read().replace('\n', '')

model = fasttext.load_model('model_oroscopo.bin')

score = np.zeros(len(data))
max_divider = round(len(data) / block_size)
print(f"Block size: {block_size}, data size: {len(data)}, pieces: {max_divider}")
for divider in range(1, max_divider + 1):
    step = round(len(data) / divider)
    for start in range(0, len(data), step):
        end = start + step if start + step < len(data) else len(data)
        label, precision = model.predict(data[start:end])
        if 'oroscopo' in label[0]:
            score[start:end] += 1

html_text = ''
returner = 150
for start in range(0, len(data), block_size):
    end = start + block_size if start + block_size < len(data) else len(data)
    a = sum(score[start:end]) / block_size / max_divider
    text = data[start:end]
    html_text += f'<span style="background-color:rgba(255,0,0,{a})">{html.escape(text)}</span>'
with open('html.html', 'w') as f:
    f.write(html_text)
