import pandas as pd

#importing data and selecting the rows
data= pd.read_csv('checktest.csv')

x=data.iloc[:,0:3].values
y=data.iloc[:,4:9].values

#spliting data into training and test set
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test =train_test_split(x,y,test_size=0.2,random_state=0)

#feature scaling
from sklearn.preprocessing import StandardScaler
sc= StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

#ANN
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
    
bcflr= Sequential()

bcflr.add(Dense(units = 5, kernel_initializer = 'uniform', activation = 'relu', input_dim = 3 ))

bcflr.add(Dense(units = 5, kernel_initializer = 'uniform', activation = 'relu'))

bcflr.add(Dense(units = 5, kernel_initializer = 'uniform', activation = 'sigmoid'))

bcflr.compile(optimizer = 'adam', loss= 'binary_crossentropy', metrics = ['accuracy'])
bcflr.compile(optimizer = 'adam', loss= 'binary_crossentropy', metrics = ['accuracy'])
bcflr.compile(optimizer = 'adam', loss= 'binary_crossentropy', metrics = ['accuracy'])

#training and testing
bcflr.fit(x_train, y_train, batch_size=10, epochs=250)

# evaluate the model
scores = bcflr.evaluate(x_train, y_train, verbose=0)
print("%s: %.2f%%" % (bcflr.metrics_names[1], scores[1]*100))

# save model and architecture to single file
bcflr.save("dlm.h5")
print("Saved model to disk")