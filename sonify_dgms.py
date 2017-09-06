import numpy as np
import scipy.io.wavfile as wavfile

"""
Imagine that we have an $NxT$ input matrix representing
T persistence diagrams vectorized into (N=49)-dim space
"""

def makeTone(freq=220, num_seconds=7.0, SR=44100, mul=1.0):
    N = num_seconds * SR
    t = np.arange(N)*(1.0/SR) #Time indices 
    x = np.cos(2*np.pi*freq*t) #The sinusoid
    x = x*mul
    return x

def makeBaseFreqs(bfq=110.0, numFreqs=49):
	BF = [bfq]
	print(BF[-1])
	for i in range(1, numFreqs):
		BF.append(BF[-1]*(2**(1.0/12.0)))
		print(BF[-1])
	
	print("# of frequencies = " + str(len(BF)))
	return BF #list

def sonifyPI(P, frame_duration=0.5):
	#P: <numpy array> NxT sequence of vectorized persistence dgms
	#frame_duration: num_seconds each dgm plays a sound for
	#generate a matrix of sound values, write to wav file
	BF = makeBaseFreqs()
	myeps = 1e-6 #values below myeps are considered negligible
	mySR = 44100

	N = P.shape[0] # N should be equal to BF.length[0]
	T = P.shape[1]
	X = [] #list of T numpy ndarrays representing tones 
	# elts of X need to be concatenated at the end
	for pd in range(0,T):
		Y = []
		for i in range(0,N):
			if abs(P[i,pd]) > myeps: # CHECK SYNTAX?
				
				# in inner loop:
				# produce a collection of tones 
				# add them together at the end

				Y.append(makeTone(freq=BF[i], num_seconds=frame_duration, SR=mySR, mul=P[i,pd]))
		Y = np.stack(Y)   #stacking row vectors (flat arrays)
		Y = Y.sum(axis=0) #column-major sum
		X.append(Y)

	#concatenate list of tones into single matrix
	X = np.concatenate(X)
	#consider standardizing X before writing to wavfile
	#X = X/np.max(X) #rescale X values
	print(X.shape)
	wavfile.write("random.wav", mySR, X)
	print("saved: "+"random.wav")


#FF = makeBaseFreqs()
P = np.random.random([49,100])

sonifyPI(P)