import numpy
import theano
import heapq
import theano.tensor as T
from numpy import linalg as LA

test = numpy.loadtxt(open("test.csv","r"), delimiter = ',', skiprows = 1)
print "read test csv ..."
train = numpy.loadtxt(open("train.csv","r"), delimiter = ',', skiprows = 1)
print "read train csv ..."

(N_test, m) = test.shape
(N_train, m) = train.shape
k = 9

data = numpy.hsplit(train,numpy.array([m-1,2*(m-1)]))

predictions = numpy.zeros((N_test,), dtype = numpy.int)
labels = 10

for i in range(N_test):
	h = []
	for j in range(k):
		dist = LA.norm(test[i,:] - data[0][j,:],2)
		heapq.heappush(h,[-dist, data[1][j][0] - 1])
		heapq.heapify(h)


	for j in range(k,N_train):
		dist = LA.norm(test[i,:] - data[0][j,:],2)
		if h[0][0] < -dist:
			heapq.heappop(h)
			heapq.heappush(h,[-dist, data[1][j][0] - 1])
			heapq.heapify(h)


	count = numpy.zeros((labels,), dtype = numpy.int)
	for elem in h:
		count[elem[1]] = count[elem[1]] + 1
		
	best_count = -1
	for j in range(labels):
		if count[j] > best_count:
			best_count = count[j]
			best_label = j

	predictions[i] = best_label + 1
	print i

numpy.savetxt("pred.csv", predictions, fmt= '%d', delimiter = ",")

