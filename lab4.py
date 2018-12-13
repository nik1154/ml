import numpy as np

# X = (hours sleeping, hours studying), y = score on test
X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
y = np.array(([92], [86], [89]), dtype=float)

# scale units
X = X/np.amax(X, axis=0) # maximum of X array
y = y/100 # max test score is 100
learning_rate=1

def sigmoid(x):
    return 1/(1+np.exp(-x))

def diffrentiate(x):
    return x*(1-x)
 
class NeuralNetwork(object):
    #Initialisation
    def __init__(neurons):
        neurons.input=2
        neurons.hidden=3
        neurons.output=1
        
        neurons.weights_from_input_hidden=np.random.randn(neurons.input,neurons.hidden)
        neurons.weights_from_hidden_output=np.random.randn(neurons.hidden,neurons.output)
        #bias_hidden=np.random.randn(1,hidden_neurons)
        #bias_output=np.random.randn(1,output_neurons)
    
    #Forward propogation
    def forward(neurons,X):
        neurons.transfer_hidden_neurons=np.dot(X,neurons.weights_from_input_hidden)
        neurons.activate_hidden=sigmoid(neurons.transfer_hidden_neurons)
        neurons.transfer_output_neurons=np.dot(neurons.activate_hidden,neurons.weights_from_hidden_output)
        activate_output=sigmoid(neurons.transfer_output_neurons)
        return activate_output
    
    
    #Backward propogation
    def backward(neurons,X,y,output):
        neurons.error_output_hidden=y-output
        neurons.errorGradient_output_hidden=neurons.error_output_hidden*(diffrentiate(output))
        neurons.error_hidden_input=neurons.errorGradient_output_hidden.dot(neurons.weights_from_hidden_output.T)
        neurons.errorGradient_hidden_input=neurons.error_hidden_input*(diffrentiate(neurons.activate_hidden))
        #Adjustments
        neurons.weights_from_hidden_output+= neurons.activate_hidden.T.dot(neurons.errorGradient_output_hidden)*learning_rate
        neurons.weights_from_input_hidden+= X.T.dot(neurons.errorGradient_hidden_input)*learning_rate
    
    #Train
    def train(neurons,X,y):
        output=neurons.forward(X)
        neurons.backward(X,y,output)
        
                                                    

NN=NeuralNetwork()                                
for i in range(1000): # trains the NN 1,000 times
  print ("Input: \n" , str(X))
  print ("Actual Output: \n" , str(y))
  print ("Predicted Output: \n" , str(NN.forward(X))) 
  print ("Loss: \n" , str(np.mean(np.square(y - NN.forward(X))))) # mean sum squared loss
  print ("\n")
  NN.train(X, y)