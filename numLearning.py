from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
from collections import OrderedDict
from sklearn.utils import shuffle
from sklearn.datasets import fetch_mldata
from sklearn.cross_validation import train_test_split
import numpy as np
import theano
import theano.tensor as T
import generateTestDate

mnist = fetch_mldata('MNIST original')
train_X, train_y = shuffle(mnist.data.astype('float32'),
                           mnist.target.astype('int32'), random_state=42)

train_X = train_X / 255.0
train_y = np.eye(10)[train_y]
test_X = np.array([generateTestDate.image_convert("file1.bmp").astype('float32'),
                   generateTestDate.image_convert("file3.bmp").astype('float32')])



trng = RandomStreams(42)
rng = np.random.RandomState(1234)

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
    Layer(100, 10, T.nnet.softmax)
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
