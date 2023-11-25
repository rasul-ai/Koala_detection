import pandas as pd
from matplotlib import pyplot as plt

# Set the figure size
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True



df = pd.read_csv("/home/bapary/Downloads/runs/detect/train/results.csv", usecols=[2,9])
print(df.head())

df.plot()
k = "train_box_loss vs val_box_loss"
# plt.savefig(f"/home/bapary/Desktop/{k}.png")
plt.show()
