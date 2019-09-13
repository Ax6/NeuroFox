import fasttext

model = fasttext.train_supervised(input="./oroscopo-data/oroscopo.train",
                                  epoch=20, dim=500, wordNgrams=2)
model.save_model("model_oroscopo_big.bin")

print(model.test("./oroscopo-data/oroscopo.valid"))
