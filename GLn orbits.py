import multiprocessing as mp
import numpy as np

tensor_val = 3
field_characteristic = 2
# numcores = 4
numcores = mp.cpu_count()

#Idea: GL_2^(valence) acts on a tensor by hitting it with a matrix from each possible side. We want to count how many orbits there are
#           and how this corresponds to rank

## GL_2 is isomorphic to S3 and has elements [10\01](id), [11\01](Or2), [11\10](Or3), [01\10](Or2), [10\11](Or2), [01\11](Or3) so can brute force the orbits by
##          acting with one copy of GL_2 on all 3 sides then acting with the next copy on the larger set of images and repeat for each copy

##      Doing higher than 4 valent cant be tricky so let's answer this question with 3 and build our way up
##      To act on a side, can write such a k-valent tensor as a vector of length 2^k with indices indexed by k 0/1's or 1/2's.
##      Matrices will be built out of the entries with 1's in the same entry. Act on each sheet by multiplying the matrix and write new tensor from each sheet
id = np.array([[10],[01]])
GL2_O2 = [np.array([[11],[01]]), np.array([[01],[10]]), np.array([[10],[11]])]
GL2_O3 = [np.array([[11],[10]]), np.array([[01],[11]])]