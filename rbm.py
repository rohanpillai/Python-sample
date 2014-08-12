import numpy
import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams


def sigmoid(array):
	return 1 / (1 + numpy.exp(-array))

class RBM():
		
	def __init__(self, n_visible=784, n_hidden=500):
		self.nvisible = n_visible
		self.nhidden = n_hidden

		self.W = numpy.array(numpy.random.uniform(
                      low=-4 * numpy.sqrt(6. / (n_hidden + n_visible)),
                      high=4 * numpy.sqrt(6. / (n_hidden + n_visible)),
                      size=(n_visible, n_hidden)))
	

		self.hbias = numpy.zeros(n_hidden)
		self.vbias = numpy.zeros(n_visible)

		self.gradW = numpy.zeros((n_visible, n_hidden))
		self.gradV = numpy.zeros((n_visible,))
		self.gradH = numpy.zeros((n_hidden,))
		self.reconstruction_error = 0.0


	def propup(self,vis):
		pre_sig_up = numpy.dot(vis,self.W) + self.hbias
		return pre_sig_up

	def propdown(self,hid):
		pre_sig_down = numpy.dot(hid,numpy.transpose(self.W)) + self.vbias
		return pre_sig_down

	def sample_h_given_v(self,vis):
		pre_sig_up = self.propup(vis)
		h_sample = numpy.random.binomial(size = pre_sig_up.shape, n = 1, p = sigmoid(pre_sig_up))
		return h_sample

	def sample_v_given_h(self,hid):
		pre_sig_down = self.propdown(hid)
		v_sample = numpy.random.binomial(size = pre_sig_down.shape, n = 1, p = sigmoid(pre_sig_down))
		return v_sample

	def gibbs_vhv(self,vis):
		h_sample = self.sample_h_given_v(vis)
		v_sample = self.sample_v_given_h(h_sample)

		return v_sample
		
	def get_energy(self,vis):
		h_sample = self.sample_h_given_v(vis)
		energy = - numpy.dot(vis, numpy.transpose(numpy.dot(h_sample,numpy.transpose(self.W)))) - numpy.dot(vis,self.vbias) - numpy.dot(h_sample,self.hbias)
		return energy

	def update(self,vis):
		h_sample1 = self.sample_h_given_v(vis)

		v_sample = self.sample_v_given_h(h_sample1)

		h_sample2 = self.sample_h_given_v(v_sample)
		
		E_data_w = numpy.transpose(numpy.asmatrix(vis))* numpy.asmatrix(h_sample1)
		E_model_w = numpy.transpose(numpy.asmatrix(v_sample))* numpy.asmatrix(h_sample2)

		self.gradW = self.gradW + (E_data_w - E_model_w)

		self.gradV = self.gradV + (vis - v_sample)

		self.gradH = self.gradH + (h_sample1 - h_sample2)

	def batch_train(self,data):
		(N,m) = data.shape
		lr = 0.3
		
		self.gradW = self.gradW * 0
		self.gradH = self.gradH * 0
		self.gradV = self.gradV * 0

		total_energy = 0.0		
		reconstruction_error = 0.0
		for i in range(N):
			self.update(data[i])
			total_energy = total_energy + self.get_energy(data[i])
			reconstruction_error = reconstruction_error + numpy.sum(numpy.absolute(self.gradV))
		
		self.gradW = lr*(self.gradW/N)
		self.gradV = lr*(self.gradV/N)
		self.gradH = lr*(self.gradH/N)

		self.W = self.W + self.gradW
		self.vbias = self.vbias + numpy.asarray(self.gradV).reshape(-1)
		self.hbias = self.hbias + numpy.asarray(self.gradH).reshape(-1)

		return [total_energy/N, reconstruction_error/N]
		
		


def train():
	file_data = numpy.loadtxt(open("digit_train.csv","r"), delimiter = ',', skiprows = 1)
	(N, m) = file_data.shape
	print "read data ... "

	labels_file = []

	tmp_data = numpy.hsplit(file_data,numpy.array([1,m]))

	data = numpy.asmatrix(tmp_data[1])
	for i in range(N):
		for j in range(m-1):
			if data[i,j] > 0:
				data[i,j] = 1

			labels_file.append(tmp_data[0][i])

	numpy.savetxt("solutions.csv",labels_file,fmt="%d",delimiter=",")
	print "written to file"

	
	feats = m
	numHidden = 200
	rbm = RBM(feats,numHidden)

	batch_size = 100
	numBatch = N/batch_size
	maxIter = 8

	file_energy = []
	file_error = []

	for epoch in range(maxIter):
		recontruction_error = 0.0
		energy = 0.0
		for i in range(numBatch):
			X = data[i*batch_size:(i+1)*batch_size,]
			[e, error] = rbm.batch_train(X)
			energy = energy + e
			recontruction_error = recontruction_error + error
			print epoch,i, e, error
			
		file_energy.append(energy)
		file_error.append(recontruction_error)

	numpy.savetxt("reconstruction.csv",file_error,delimiter = ",")
	numpy.savetxt("energy.csv",file_energy,delimiter=",")

	return rbm


def test():
	data = numpy.matrix('1,2,4,3;7,5,8,2;5,7,4,1', dtype = theano.config.floatX)
	b = RBM(4,3)

#	X = T.matrix("X")
#	gibs = b.gibbs_vhv(X)
#	reconstruct = theano.function([X],gibs)


	return b
	


	
