import pickle

with open("infer_test.bin", "rb") as f:
    loaded_data = pickle.load(f)
print(loaded_data[0])
