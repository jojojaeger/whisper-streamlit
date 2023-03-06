import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import pandas as pd

# read csv
df = pd.read_csv('c_m.csv', names=['c1', 'c2', 'c3'], sep=';')

df_list = []
# iterate over the rows of the input DataFrame
for i, row in df.iterrows():
    # create a new DataFrame with col3 number of copies of the current row
    new_df = pd.DataFrame([row] * row['c3'])
    # append the new DataFrame to the list
    df_list.append(new_df)

# concatenate all the resulting DataFrames into a single DataFrame
result_df = pd.concat(df_list)

df = result_df

ground_truth = df.iloc[:20, 0]
predictions = df.iloc[:20, 1]

# compute confusion matrix
labels = list(set(ground_truth.str.split().explode().unique())
              | set(predictions.str.split().explode().unique()))

cm = confusion_matrix(ground_truth, predictions, labels=labels)

# plot confusion matrix
fig, ax = plt.subplots()
im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
ax.figure.colorbar(im, ax=ax)

# set title and axis labels
ax.set(title="Confusion Matrix", xlabel="Predicted label", ylabel="True label")
ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))
ax.set_xticklabels(labels, rotation=90)
ax.set_yticklabels(labels)

# add annotations to the plot
thresh = cm.max() / 2.
for i in range(len(labels)):
    for j in range(len(labels)):
        if cm[i, j] > 0:
            ax.text(j, i, int(cm[i, j]),
                    ha="center", va="center", fontsize=8,
                    color="white" if cm[i, j] > thresh else "black")

# add grid to the plot

fig.subplots_adjust(bottom=0.3)

plt.show()
