import numpy as np
from tqdm import trange

# calculate the entropy of a data set
def entropy(data, label):
    rows, cols = data.shape
    # Count the number and proportion of different categories
    label_counts = np.unique(label, return_counts=True)[1]
    label_probs = label_counts / rows
    # Calculate the entropy of a data set
    ent = -np.sum(label_probs * np.log2(label_probs))
    return ent

# calculate the conditional entropy of a data set on a certain feature
def cond_entropy(data, label, feature):
    rows, cols = data.shape
    # Get all values of the feature in the data set
    values = data[:, feature]
    # Count the number of different values
    value_list, value_counts = np.unique(values, return_counts=True)
    # Calculate the probability of different values
    value_probs = value_counts / rows

    cond_ent = 0
    for i in range(len(value_counts)):
        # Get the sub-dataset corresponding to the value
        sub_data = data[data[:, feature] == value_list[i]]
        # Get the sub-label column corresponding to the value
        sub_label = label[data[:, feature] == value_list[i]]
        # Calculate the entropy of a subdataset
        sub_ent = entropy(sub_data, sub_label)
        # Calculate conditional entropy
        cond_ent += value_probs[i] * sub_ent
    return cond_ent

# calculate the information gain of a data set on a certain feature
def info_gain(data, label, feature):
    # Calculate the entropy of a data set
    ent = entropy(data, label)
    # Calculate the conditional entropy of the data set on this feature
    cond_ent = cond_entropy(data, label, feature)
    # Calculate information gain
    gain = ent - cond_ent
    return gain

# calculate the information gain for each column of the matrix
def info_gain_matrix(data, label):
    cols = data.shape[1]
    # Initialize an empty list to store the information gain of each column
    gain_list = []
    # Calculate the information gain for each column
    for i in trange(cols):
        gain = info_gain(data, label, i)
        gain_list.append(gain)
    gain_array = np.array(gain_list)
    return gain_array
