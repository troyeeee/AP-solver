import numpy as np

numberOfRows = 3;
numberOfColumns = 3;


np_arr_2 = np.array([
    [20, 58, 52],
    [79, 57, 69],
    [71, 1, 37]
])
theSolution = "THE SOLUTION : \n"
# Creating Temporary array of zeros
temp_arr = np.zeros(numberOfRows * numberOfColumns,dtype=int)
temp_arr = temp_arr.reshape(numberOfRows, numberOfColumns )
#



temp_arr_2 = np.zeros(numberOfRows * numberOfColumns,dtype=int)
temp_arr_2 = temp_arr_2.reshape(numberOfRows, numberOfColumns )



print(temp_arr_2)
'''
temp_arr = np.invert(np_arr_2) + temp_arr_2

theSolution += "Negate all values : \n"
theSolution += "Because the objective is to maximize the total cost we negate all elements:\n"
theSolution += str(temp_arr) + '\n'
theSolution += '\n'

temp_arr_2 = np.zeros(numberOfRows * numberOfColumns,dtype=int)
temp_arr_2 = temp_arr_2.reshape(numberOfRows, numberOfColumns )

theSolution += "Make the Matrix non negative\n"
theSolution += "we add the maximum value to each entry to make the cost matrix non negative:\n"
maxNumber = np.amax(np_arr_2)

for i in range(0,numberOfRows):
    temp_arr_2[:,i] = maxNumber

temp_arr = temp_arr + temp_arr_2
theSolution += str(temp_arr) + '\n'

theSolution += '\n'
theSolution += "Subtract Minimum Row Values\n"

temp_arr_2 = np.zeros(numberOfRows * numberOfColumns,dtype=int)
temp_arr_2 = temp_arr_2.reshape(numberOfRows, numberOfColumns )

row_minima = np.amin(temp_arr,axis = 1)

for i in range(0,len(row_minima)):
    temp_arr_2[i,:] = row_minima[i]

temp_arr = temp_arr - temp_arr_2
theSolution += str(temp_arr) + '\n'


theSolution += '\n'
theSolution += "Subtract Minimum Column Values" + '\n'

temp_arr_2 = np.zeros(numberOfRows * numberOfColumns,dtype=int)
temp_arr_2 = temp_arr_2.reshape(numberOfRows, numberOfColumns )

col_minima = np.amin(temp_arr,axis = 0)

for i in range(0,len(col_minima)):
    temp_arr_2[:,i] = col_minima[i]

temp_arr = temp_arr - temp_arr_2
theSolution += str(temp_arr) + '\n'

print(theSolution)
'''