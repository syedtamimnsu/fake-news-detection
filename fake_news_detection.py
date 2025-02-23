# -*- coding: utf-8 -*-
"""fake news detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DzIY_3VS9Q2iYZCqPxmdY5kAmwXv_ka-

importing dependencies
"""

import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

#show stopwords in english language. we will remove those stopwords. because those words not carry for our project
# printing the stopwords in English
print(stopwords.words('english'))

"""data preprocessing"""

# loading the dataset to a pandas DataFrame
# Trying different encodings to handle potential encoding issues
try:
    news_dataset = pd.read_csv('/content/train.csv', encoding='utf-8', on_bad_lines='skip') # Try utf-8 first just in case
except UnicodeDecodeError:
    try:
        news_dataset = pd.read_csv('/content/train.csv', encoding='latin1', on_bad_lines='skip') # Try latin1 if utf-8 fails
    except UnicodeDecodeError:
      try:
        news_dataset = pd.read_csv('/content/train.csv', encoding='ISO-8859-1', on_bad_lines='skip') # Try ISO-8859-1 if latin1 fails
      except UnicodeDecodeError:
        news_dataset = pd.read_csv('/content/train.csv', encoding='utf-8', errors='ignore', on_bad_lines='skip') # Skip error lines
        print("Encoding errors encountered, some lines skipped")

news_dataset.shape

news_dataset.head()

#number of missing values
news_dataset.isnull().sum()

#replacing the null values with empty string
news_dataset = news_dataset.fillna('')

#number of missing values
news_dataset.isnull().sum()

#margin author name and news title
news_dataset['content'] = news_dataset['author']+' '+news_dataset['title']

print(news_dataset['content'])

#separating the data and label column
x = news_dataset.drop(columns='label', axis=1)
y = news_dataset['label']

print(x)
print(y)

"""Stemming: process of reducing a word to its root word. remove prefix and suffix.
EX: actor, acting, actress --> act
"""

port_stem = PorterStemmer()

def stemming(content):
  stemmed_content = re.sub('[^a-zA-Z]',' ', content)     #all number, upper and lower case single letter convert into " " of content
  stemmed_content = stemmed_content.lower()      #convert all of them into lower case
  stemmed_content = stemmed_content.split()
  stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]    #removing top words and Stemming process
  stemmed_content = ' '.join(stemmed_content)        #joing the words by space separate A
  return stemmed_content

news_dataset['content'] = news_dataset['content'].apply(stemming)

print(news_dataset['content'])

x = news_dataset['content'].values
y = news_dataset['label'].values

print(x)

print(y)

x.shape
y.shape

#converting the textual data into neumerical data
vectorizer = TfidfVectorizer()
vectorizer.fit(x)
x = vectorizer.transform(x)

print(x)

# Convert y to float, replacing empty strings with np.nan
y = np.array([np.nan if isinstance(val, str) and not val else float(val) for val in y])

# Fill NaN values with 0 and then convert to integer type
y = np.nan_to_num(y, nan=0).astype(int)

print(y)

"""Splitting dataset to traning and test data"""

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=5)

"""Training the model Logistic Regration"""

model = LogisticRegression()

model.fit(x_train, y_train)

"""Evaluation"""

#accuracy score on the training data
x_train_prediction = model.predict(x_train)
training_data_accuracy = accuracy_score(x_train_prediction, y_train)

print('Accuracy score of training data:', training_data_accuracy)

#accuracy score on the testing data
x_test_prediction = model.predict(x_test)
testing_data_accuracy = accuracy_score(x_test_prediction, y_test)

print('Accuracy score of training data:', testing_data_accuracy)

"""Making a predicting system

prediction 1-->news is fake
prediction 0-->news is real
"""

x_new = x_test[1]

prediction = model.predict(x)
print(prediction)

if(prediction[1]==0):
  print('News is real.')
else:
  print('News is fake')

