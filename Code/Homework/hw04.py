import numpy as np
import matplotlib as plt
# Question 3
##############################################################################################
# Part (a)


matrixA = np.array([[0.8, 0.0, 0.0, 0.05, 0.15],
                   [1.0, 0.0, 0.0, 0.0, 0.0],
                   [0.3, 0.2, 0.5, 0.0, 0.0],
                   [0.0, 0.0, 0.05, 0.95, 0.0],
                   [0.0, 0.0, 0.0, 0.2, 0.8]])


# Print matrix to make sure its been intialzed correctly.
print("Matrix A:\n",matrixA)

# Check that each rows coumn values add up to one.
for row in matrixA:
    sum_acum = 0
    for col in row:
        sum_acum += col
    if sum_acum  == 1:
        # print("Stochastic!")
        continue
    else:
        print(f"Not stocahstic at with this {row}")
        break

# Question 3
##############################################################################################
# Part (b)

# Intialize opnion vector
opnionVector = np.array([[1], [1], [0.5], [0], [0]])

# Verify initialized opnion matrix 
print("Opnion Matrix:\n", opnionVector)

# Perform matrix multiplication
matrixProduct = matrixA @ opnionVector

# Print to verify matrix mutliplication was done correctly by hand
print("Matrix DOT Product Output:\n", matrixProduct)

# Question 3
##############################################################################################
# Part (c)
# Perfrom matrix multiplication to show how values converge. 
print("Matrix as \'t\' Approaches Inifinity:\n", np.linalg.matrix_power(matrixA,100000))

# Question 4
##############################################################################################
# Part (a)

# This represnt the first part of the equations which is the sumation of elements in the matrix 
# from the beging step to the range of t specified steps.
def compute_series(Lam, A, t):
    n = A.shape[0]
    accum = np.zeros(n, n)
    for i in range(t):
        accum += np.linalg.matrix_power(Lam@A, i)
    return accum

def friedkin_johnsen(Lam,A,x0,k,plot_result = False) :
  n = A.shape[0] # assuming everything is dimensioned right
  I = np.eye(n)
  xx = np.zeros((n,k))
  xx[:,0] = x0
  for i in range(1,k) :
    xx[:,i] = Lam@A@xx[:,i-1] + (I-Lam)@x0
    print(xx)
    input()
  if plot_result:
    plt.plot(xx.T)
  return xx 

# Create power constant for simulation runs
k = 1

# Initalize matrix from question 2
matrixB = np.array([[0.5, 0.0, 0.5, 0.0],
                    [0.1, 0.8, 0.1, 0],
                    [0.0, 0.05, 0.85, 0.1],
                    [0.23, 0.07, 0, 0.7]])
print(matrixB)

# Initialize given lambda values for the question
lambdas = [0.9, 0.1, 0.8, 1] 

# Initialize given original opnions
opnionVectorB = np.array([0.9, 0.1, 0.8, 1])
 
# Get the diagnoal matrix of lambda values 
matrixDiag = np.diag(lambdas)
print("Matrix of diagonal lambda values:")
print(matrixDiag)

print("First step:\n", matrixB * matrixDiag)

# Show that our valeus will quickly converge and envetually get very close to 0, but not quite
# python ends up rounding to 0 after so long due to not being able to retain decmials values.
print(f"Matrixed rasied to the \'k-th\' ({k}):")
print(np.linalg.matrix_power(matrixB@matrixDiag, k))

# Now using method created above we perform the first of the Freidken Johnson modle
print("Executing first step of Friedkin-Johnson model:\n", friedkin_johnsen(matrixDiag, matrixB, opnionVectorB, 10))

# Question 4
##############################################################################################
# Part (b)

# Q: Where do we find values that are the most different onions when passed different susbtibaliity 
#    values we call lambda.



