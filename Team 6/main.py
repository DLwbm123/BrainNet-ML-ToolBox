"""
Target Problem:
---------------
* A classifier for the diagnosis of Autism Spectrum Disorder (ASD)

Proposed Solution (Machine Learning Pipeline):
----------------------------------------------
* Standard Scaling -> PCA -> SVM

Input to Proposed Solution:
---------------------------
* Directories of training and testing data in csv file format
* These two types of data should be stored in n x m pattern in csv file format.

  Typical Example:
  ----------------
  n x m samples in training csv file (n number of samples, m - 1 number of features, ground truth labels at last column)
  k x s samples in testing csv file (k number of samples, s number of features)

* These data set files are ready by load_data() function.
* For comprehensive information about input format, please check the section
  "Data Sets and Usage Format of Source Codes" in README.md file on github.

Output of Proposed Solution:
----------------------------
* Predictions generated by learning model for testing set
* They are stored in "submisson.csv" file.

Code Owner:
-----------
* Copyright © Team 6. All rights reserved.
* Copyright © Istanbul Technical University, Learning From Data Spring 2019. All rights reserved. """

import numpy as np
import pandas as pd

from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

np.random.seed(5)  # anchoring randomization during training step


def load_data():

    train_data = pd.read_csv('train.csv', header=0)
    test_data = pd.read_csv('test.csv', header=0)
    return train_data, test_data


def preprocessing(train_data, test_data):

    """
    The method splits features and labels of training data into two separate sections.
    Then, it applies standard scaling operation on training and testing sets.

    Parameters:
    -----------
    train_data: It is numpy array containing features and labels together
    test_data: It is numpy array containing only features """

    x_train = train_data.iloc[:, 0:595].values
    y_train = train_data.iloc[:, 595:].values
    x_test = test_data.iloc[:].values

    sc = StandardScaler()
    scaled_x_train = sc.fit_transform(x_train)
    scaled_x_test = sc.transform(x_test)

    return scaled_x_train, scaled_x_test, y_train


def dimension_reduction(scaled_x_train, scaled_x_test):

    """
    The method performs pca technique to reduce the dimension of feature space in which observations are situated.

    Parameters:
    -----------
    scaled_x_train: scaled features of training data
    scaled_x_test: scaled features of testing data """

    # reducing training and testing samples into lower dimension
    pca = PCA(n_components=2)
    reduced_x_train = pca.fit_transform(scaled_x_train)
    reduced_x_test = pca.transform(scaled_x_test)

    return reduced_x_train, reduced_x_test


def train_model(reduced_x_train, y_train):

    """
    The method trains svm learning model by using training features cross its ground truth labels.

    Parameters:
    -----------
    reduced_x_train: features of training data lying on principal component axes
    y_train: ground truth labels of those features """

    svc = SVC(kernel='poly', gamma=0.5, C=1, random_state=3)
    svc.fit(reduced_x_train, y_train.ravel())
    return svc


def predict(svc, reduced_x_test):

    """
    The method predicts outputs for test samples by using learning model.

    Parameters:
    -----------
    svc: trained learning model
    reduced_x_test: features of testing set lying on principal component axes """

    predictions = svc.predict(reduced_x_test)
    return predictions


def write_output(predictions):

    # writing predictions to the file
    f = open("submission.csv", "w")
    f.write("ID,Predicted\n")
    for i in range(0, len(predictions)):
        f.write(str(i+1) + "," + str(predictions[i]) + "\n")


# ******* Main Program ******* #

train_data, test_data = load_data()

scaled_x_train, scaled_x_test, y_train, = preprocessing(train_data, test_data)
reduced_x_train, reduced_x_test = dimension_reduction(scaled_x_train, scaled_x_test)

svc_model = train_model(reduced_x_train, y_train)
predictions = predict(svc_model, reduced_x_test)

write_output(predictions)
