import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
dataset = pd.read_csv('https://storage.googleapis.com/dqlab-dataset/pythonTutorial/online_raw.csv')

# print('Shape dataset:', dataset.shape)
# print('\nLima data teratas:\n', dataset.head())
# print('\nInformasi dataset:')
# print(dataset.info())
# print('\nStatistik deskriptif:\n', dataset.describe())

# dataset['Revenue'] = dataset['Revenue'].astype(int)
# dataset['Weekend'] = dataset['Weekend'].astype(int)
# dataset_corr = dataset.corr(numeric_only=True)
# print('Korelasi dataset:\n', dataset.corr(numeric_only=True))
# print('Distribusi Label (Revenue):\n', dataset['Revenue'].value_counts())
# print('Korelasi BounceRates-ExitRates:', dataset_corr.loc['BounceRates', 'ExitRates'])
# print('\nKorelasi Revenue-PageValues:', dataset_corr.loc['Revenue', 'PageValues'])
# print('\nKorelasi TrafficType-Weekend:', dataset_corr.loc['TrafficType', 'Weekend'])

# # checking the Distribution of customers on Revenue
# plt.rcParams['figure.figsize']=(12,5)
# plt.subplot(1,2,1)
# sns.countplot(x='Revenue', hue='Revenue', data=dataset, palette='pastel', legend=False)
# plt.title('Buy or Not', fontsize =20)
# plt.xlabel('Revenue or not', fontsize=14)
# plt.ylabel('count',fontsize=14)
# # checking the Distribution of customers on Weekend
# plt.subplot(1,2,2)
# sns.countplot(x='Weekend', hue='Weekend', data=dataset, palette='inferno', legend=False)
# plt.title('Purchase on Weekends', fontsize= 20)
# plt.xlabel('Weekend or not', fontsize =14)
# plt.ylabel ('count', fontsize=14)
# plt.show()

#checking missing value for each feature  
print('Checking missing value for each feature:')
print(dataset.isnull().sum())
#Counting total missing value
print('\nCounting total missing value:')
print(dataset.isnull().sum().sum())
#Drop rows with missing value
dataset_clean = dataset.dropna()  
print('\nUkuran dataset_clean:', dataset_clean.shape)
print("\nBefore imputation:")
# Checking missing value for each feature  
print(dataset.isnull().sum())
# Counting total missing value  
print(dataset.isnull().sum().sum())
print("\nAfter imputation:")
# Fill missing value with mean of feature value  
dataset.fillna(dataset.mean(numeric_only=True), inplace = True)
# Checking missing value for each feature  
print(dataset.isnull().sum())
# Counting total missing value  
print(dataset.isnull().sum().sum())

from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import numpy as np 
#Define MinMaxScaler as scaler  
scaler = MinMaxScaler()  
#list all the feature that need to be scaled  
scaling_column = ['Administrative', 'Administrative_Duration', 'Informational', 'Informational_Duration', 'ProductRelated', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 'PageValues']
#Apply fit_transfrom to scale selected feature
dataset[scaling_column]= scaler.fit_transform(dataset[scaling_column])
#Cheking min and max value of the scaling_column
print(dataset[scaling_column].describe().T[['min','max']])

# Convert feature/column 'Month'
LE = LabelEncoder()
dataset['Month'] = LE.fit_transform(dataset['Month'])
# print(LE.classes_)
# print(np.sort(dataset['Month'].unique()))
# print('')

# Convert feature/column 'VisitorType'
LE = LabelEncoder()
dataset['VisitorType'] = LE.fit_transform(dataset['VisitorType'])
# print(LE.classes_)
# print(np.sort(dataset['VisitorType'].unique()))

# removing the target column Revenue from dataset and assigning to X
X = dataset.drop(['Revenue'],axis=1)
# assigning the target column Revenue to y
y = dataset['Revenue']
# checking the shapes
print('Shape of X:', X.shape)
print('Shape of y:', y.shape)

from sklearn.model_selection import train_test_split
# splitting the X, and y
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state = 0)
# checking the shapes
print('Shape of X_train :', X_train.shape)
print('Shape of y_train :', y_train.shape)
print('Shape of X_test :', X_test.shape)
print('Shape of y_test :', y_test.shape)

from sklearn.metrics import confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier
# Call the classifier
model = DecisionTreeClassifier()
# Fit the classifier to the training data
model = model.fit(X_train, y_train)
# Apply the classifier/model to the test data
y_pred = model.predict(X_test)
print(y_pred.shape)

# evaluating the model
print('Training Accuracy :', model.score(X_train, y_train))
print('Testing Accuracy :', model.score(X_test, y_test))

# confusion matrix
print('\nConfusion matrix:')
cm = confusion_matrix(y_test, y_pred)
print(cm)

# classification report
print('\nClassification report:')
cr = classification_report(y_test, y_pred)
print(cr)

from sklearn.linear_model import LogisticRegression

# Call the classifier
logreg = LogisticRegression()
# Fit the classifier to the training data  
logreg = logreg.fit(X_train, y_train)
#Training Model: Predict 
y_pred = logreg.predict(X_test)

#Evaluate Model Performance
print('Training Accuracy :', logreg.score(X_train, y_train))  
print('Testing Accuracy :', logreg.score(X_test, y_test)) 

# confusion matrix
print('\nConfusion matrix:')
cm = confusion_matrix(y_test, y_pred)
print(cm)

# classification report
print('\nClassification report:')
cr = classification_report(y_test, y_pred)
print(cr)

