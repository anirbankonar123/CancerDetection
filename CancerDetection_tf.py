#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 19:42:50 2018

@author: anirban
"""
import tensorflow as tf
import pandas as pd
import numpy as np

# The data needs to be split into a training set and a test set
# To use 80/20, set the training size to .8
training_set_size_portion = .8

# Set to True to shuffle the data before you split into training and test sets
do_shuffle = True
# Keep track of the accuracy score
accuracy_score = 0
# The DNN has hidden units, set the spec for them here
hidden_units_spec = [10,20,10]
n_classes_spec = 2
# Define the temp directory for keeping the model and checkpoints
tmp_dir_spec = "tmp/model"
# The number of training steps
steps_spec = 2000
# The number of epochs
epochs_spec = 15
# File Name - be sure to change this if you upload something else
file_name = "/home/anirban/Downloads/wdbc.csv"

# Here's a set of our features. If you look at the CSV, 
# you'll see these are the names of the columns. 
# In this case, we'll just use all of them:
features = ['radius','texture']

# Here's the label that we want to predict -- it's also a column in the CSV
labels = ['diagnosis_numeric']

# Here's the name we'll give our data
#data_name = '/home/anirban/Downloads/wsbc.csv'
#
## Here's where we'll load the data from
#data_url = 'http://www.laurencemoroney.com/wp-content/uploads/2018/02/wdbc.csv'
#
#file_name = tf.keras.utils.get_file(data_name, data_url)
my_data = pd.read_csv(file_name, delimiter=',')

if do_shuffle:
 randomized_data = my_data.reindex(np.random.permutation(my_data.index))
else:
 randomized_data = my_data
 
 
total_records = len(randomized_data)
training_set_size = int(total_records * training_set_size_portion)
test_set_size = total_records - training_set_size

training_features = randomized_data.head(training_set_size)[features].copy()
training_labels = randomized_data.head(training_set_size)[labels].copy()
print(training_features.head())
print(training_labels.head())

testing_features = randomized_data.tail(test_set_size)[features].copy()
testing_labels = randomized_data.tail(test_set_size)[labels].copy()

feature_columns = [tf.feature_column.numeric_column(key) for key in features]

classifier = tf.estimator.DNNClassifier(
    feature_columns=feature_columns, 
    hidden_units=hidden_units_spec, 
    n_classes=n_classes_spec, 
    model_dir=tmp_dir_spec)


train_input_fn = tf.estimator.inputs.pandas_input_fn(x=training_features, y=training_labels, num_epochs=epochs_spec, shuffle=True)
 
classifier.train(input_fn=train_input_fn, steps=steps_spec)

test_input_fn = tf.estimator.inputs.pandas_input_fn(x=testing_features, y=testing_labels, num_epochs=epochs_spec, shuffle=False)

accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]
print("Accuracy = {}".format(accuracy_score))

prediction_set = pd.DataFrame({'radius':[14, 13], 'texture':[25, 26]})

predict_input_fn = tf.estimator.inputs.pandas_input_fn(x=prediction_set, num_epochs=1, shuffle=False)

predictions = list(classifier.predict(input_fn=predict_input_fn))

predicted_classes = [p["classes"] for p in predictions] 
results=np.concatenate(predicted_classes) 
print(results)
