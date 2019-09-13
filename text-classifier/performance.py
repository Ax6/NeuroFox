import fasttext
import numpy as np
from matplotlib import pyplot as plt

with open('articolo.txt') as f:
    data = f.read().replace('\n', '')

model = fasttext.load_model('model_oroscopo_big.bin')

score = np.zeros(len(data))
for divider in range(1, 100):
    step = round(len(data) / divider)
    for start in range(0, len(data), step):
        end = start + step if start + step < len(data) else len(data)
        label, precision = model.predict(data[start:end])
        if 'oroscopo' in label[0]:
            score[start:end] += 1

returner = 150
for i, letter in enumerate(data):
    row = int(i / returner)
    col = i % returner
    a = score[i] / 100
    plt.text(col / 20, -row / 30, letter, backgroundcolor=(1, 0, 0, a))
plt.xlim([0, 5])
plt.ylim([-1, 0])
plt.axis('off')
plt.show()
