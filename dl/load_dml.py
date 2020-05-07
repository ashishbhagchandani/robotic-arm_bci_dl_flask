# load and evaluate a saved model
from numpy import loadtxt
import numpy as np
import tensorflow as tf
 
# load model
bcflr = tf.keras.models.load_model('dlm.h5')

# summarize model.
bcflr.summary()

# load dataset
data = loadtxt(fname="checktest.csv", delimiter=",")

# split into input (X) and output (Y) variables
x= data[:,0:3]
y= data[:,4:9]

#prediction
x1=data[:,4]                  #case5(poor quality)
y1=np.array(x1)
a1=np.count_nonzero(y1 == 1)
print(a1)

x2=data[:,5]                  #case1(attention with calmness)
y2=np.array(x2)
a2=np.count_nonzero(y2 == 1)
print(a2)

x3=data[:,6]                  #case2(No attention with calmness)
y3=np.array(x3)
a3=np.count_nonzero(y3 == 1)
print(a3)

x4=data[:,7]                  #case3(Attention with no calmness)
y4=np.array(x4)
a4=np.count_nonzero(y4 == 1)
print(a4)

x5=data[:,8]                  #case4(No attention with no calmness)
y5=np.array(x5)
a5=np.count_nonzero(y5 == 1)
print(a5)

if(a1>a2 and a1>a3 and a1>a4 and a1>a5):
    state="poor quality"
    #print("poor quality")
elif(a2>a1 and a2>a3 and a2>a4 and a2>a5):
    print("attention with calmness")
elif(a3>a1 and a3>a2 and a3>a4 and a3>a5):
    state="No attention with calmness"
   # print("No attention with calmness")
elif(a4>a1 and a4>a2 and a4>a3 and a4>a5):
    state="Attention with no calmness"
    #print("Attention with no calmness")
else:
    state="No attention with no calmness"
    #print("No attention with no calmness")
print(state)

# evaluate the model
score = bcflr.evaluate(x, y, verbose=0)
print("%s: %.2f%%" % (bcflr.metrics_names[1], score[1]*100))