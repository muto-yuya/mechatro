import cv2
from sklearn.utils import shuffle
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
from collections import OrderedDict

import numpy as np
import theano
import theano.tensor as T

trng = RandomStreams(42)
rng = np.random.RandomState(1234)
def image_convert(filename):
    file = cv2.imread(filename)
    file = np.array(file[:,:,0]).flatten()
    file = (255-file)/255
    return file

def strnum_make(i):
    if i < 10:
        strnum = "00"+str(i)
    elif i < 100:
        strnum = "0"+str(i)
    else:
        strnum = str(i)
    return strnum


samples_length = 1000
pluses = np.empty((0,784))
subs = np.empty((0,784))
multis = np.empty((0,784))
divs = np.empty((0,784))

for i in range(0,samples_length):
    img_plus = image_convert("plus/plus_"+strnum_make(i)+".bmp")
    img_sub = image_convert("sub/sub_"+strnum_make(i)+".bmp")
    img_multi = image_convert("multi/multi_"+strnum_make(i)+".bmp")
    img_div = image_convert("div/div_"+strnum_make(i)+".bmp")

    pluses = np.append(pluses,np.array([img_plus]),axis=0)
    subs = np.append(subs,np.array([img_sub]),axis=0)
    multis = np.append(multis,np.array([img_multi]),axis=0)
    divs = np.append(divs,np.array([img_div]),axis=0)

all_X = np.append(pluses,subs,axis=0)
all_X = np.append(all_X,multis,axis=0)
all_X = np.append(all_X,divs,axis=0)
all_y = np.append(np.ones(samples_length)*0,np.ones(samples_length)*1)
all_y = np.append(all_y,np.ones(samples_length)*2)
all_y = np.append(all_y,np.ones(samples_length)*3)

train_X = all_X
train_y = all_y
random_state = np.random.RandomState(0)
train_X,train_y = shuffle(train_X.astype('float32'),train_y.astype('int32'))
train_y = np.eye(4)[train_y]

test_X = [image_convert("test_000.bmp"),
          image_convert("test_001.bmp"),
          image_convert("test_002.bmp"),
          image_convert("test_003.bmp"),
          image_convert("test_004.bmp"),
          image_convert("test_005.bmp"),
          image_convert("test_006.bmp"),
          image_convert("test_007.bmp"),
          image_convert("test_008.bmp")]
test_X = np.array(test_X).astype('float32')

# Multi Layer Perceptron
class Layer:
    # Constructor
    def __init__(self, in_dim, out_dim, function):
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.function = function
        self.W = theano.shared(rng.uniform(low=-0.08, high=0.08,
                                           size=(in_dim, out_dim)
                                           ).astype('float32'), name='W')
        self.b = theano.shared(np.zeros(out_dim).astype('float32'), name='b')
        self.params = [self.W, self.b]

    # Forward Propagation
    def f_prop(self, x):
        self.z = self.function(T.dot(x, self.W) + self.b)
        return self.z


# Stochastic Gradient Descent
def sgd(params, g_params, eps=np.float32(0.1)):
    updates = OrderedDict()
    for param, g_param in zip(params, g_params):
        updates[param] = param - eps*g_param
    return updates

def tanh(x):
    return T.nnet.sigmoid(x)*2-1
layers = [
    Layer(784, 100, tanh),
    Layer(100, 4, T.nnet.softmax)
]

x = T.fmatrix('x')
t = T.imatrix('t')

params = []
for i, layer in enumerate(layers):
    params += layer.params
    if i == 0:
        layer_out = layer.f_prop(x)
    else:
        layer_out = layer.f_prop(layer_out)

y = layers[-1].z
cost = T.mean(T.nnet.categorical_crossentropy(y, t))

g_params = T.grad(cost=cost, wrt=params)
updates = sgd(params, g_params)

train = theano.function(inputs=[x, t], outputs=cost, updates=updates,
                        allow_input_downcast=True, name='train')
test = theano.function(inputs=[x], outputs=T.argmax(y, axis=1), name='test')

batch_size = 50
n_batches = train_X.shape[0]//batch_size
for epoch in range(10):
    train_X, train_y = shuffle(train_X, train_y)
    for i in range(n_batches):
        start = i*batch_size
        end = start + batch_size
        train(train_X[start:end], train_y[start:end])
    pred_y = test(test_X)
print(pred_y)
pred = []
for i in range(0,pred_y.shape[0]):
    if pred_y[i] == 0:
        pred.append("+")
    elif pred_y[i] == 1:
        pred.append("-")
    elif pred_y[i] == 2:
        pred.append("*")
    elif pred_y[i] == 3:
        pred.append("/")
print(pred)