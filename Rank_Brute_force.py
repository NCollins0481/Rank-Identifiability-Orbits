from itertools import combinations
import multiprocessing as mp
from collections import defaultdict
from functools import partial

tensor_val = 3
field_characteristic = 2
# numcores = 1
numcores = mp.cpu_count()
tensor_type = "PSymmetric2" #Options are Normal(for Segre varieties), Symmetric(for Veronese varieties), or PSymmetrick(For Segre-Veronese varieties with k products symmetric)

def make_all_zero(valence):
    all_zero = []
    for i in range(0, 2**valence):
        all_zero.append(0)

    return tuple(all_zero)

def brute_force_mult(list1, list2):
    new_vec = []
    for j in range(0,len(list2)): #need these reversed to get ordering right
        for i in range(0,len(list1)):
                new_vec.append(list1[i]*list2[j])
    return tuple(new_vec)

def compute_normal_rank(elementary_components, tensor_val):
    current_comps = set()
    current_mult = 1
    last_comps = elementary_components #If Normal, Symmetric, Partially symmetric
    while current_mult < tensor_val:
            current_comps = set()
            for elt1 in last_comps:
                for elt2 in elementary_components:
                    current_comps.add(brute_force_mult(elt1, elt2))
            last_comps = current_comps
            current_mult += 1
    return current_comps

def compute_symmetric_rank(elementary_components, tensor_val):
    current_comps = set()
    for comp in elementary_components:
        current_mult = 1
        last_comp = comp
        while current_mult < tensor_val:
            current_comp = brute_force_mult(last_comp, comp)
            last_comp = current_comp
            current_mult += 1
        current_comps.add(current_comp)
    return current_comps


def compute_rank_one_tensors(tensor_val, tensor_type): #generate the [1,0], [0,1], [1,1] and brute force all multiplications of these. Remember that ab != ba
    elementary_components = ((1,0),(0,1),(1,1))
    if tensor_type == "Normal":
        current_comps = compute_normal_rank(elementary_components, tensor_val)
        
    elif tensor_type == "Symmetric":
        current_comps = compute_symmetric_rank(elementary_components, tensor_val)
            
    elif "PSymmetric" in tensor_type:
        num = int(tensor_type[-1]) #Only works for single digit right now
        sym_comps = compute_symmetric_rank(elementary_components, num)
        if tensor_val-num > 1:
            norm_comps = compute_normal_rank(elementary_components, tensor_val-num)
        else:
            norm_comps = elementary_components
        current_comps = set()
        for s in sym_comps:
            for n in norm_comps:
                comp = brute_force_mult(s, n)
                current_comps.add(comp)


    one_points = current_comps
    return one_points

def add_all(T, c): #add all the entries component-wise in the list
    current_sum = T[0]
    for j in range(1,len(T)):
        current_sum = tensor_add(current_sum, T[j], c)

    return (current_sum, T)

def tensor_add(T1, T2, char):
    sum_tensor = []
    for i in range(0,len(T1)):
        sum_tensor.append((T1[i] + T2[i]) % char)
    
    return tuple(sum_tensor)

def compute_higher_rank_tensors(prev_combos, rank_1_tensors, rank, char, numcores, zero_tensor, val):
    TensorDict = defaultdict(list)
    unique_combos = set(combinations(rank_1_tensors, rank)) #All n choose k combinations of rank 1 tensors

    # for T in unique_combos: #multiprocess this
    with mp.Pool(numcores) as p:
        add_partial = partial(add_all, c=char)
        rank_tensor_list = p.map(add_partial, unique_combos) #Want to append a list of the unique combos that map to this tensor
    
    p.close()
    p.join()

    for key, value in rank_tensor_list: #Idk how to remove this loop but it will be slow
        TensorDict.setdefault(key, []).append(value)

    # TensorDict = dict(rank_tensor_list)

    [TensorDict.pop(x, None) for x in prev_combos]
    TensorDict.pop(zero_tensor, None)

    return TensorDict

if __name__ == "__main__":

    # for tensor_val in range(3,10):

    rk1_set = compute_rank_one_tensors(tensor_val, tensor_type)

    current_combos = []
    current_combos += rk1_set
    print("There are:", len(rk1_set), "tensors of rank:", 1) #can try brute-forcing combos of rank 2 tensors with rank 1

    zero_tensor = make_all_zero(tensor_val)

    current_combos.append(zero_tensor)
    current_length = len(current_combos)
    i = 2
    higher_T = [zero_tensor] #With a better bound this can be []

    tensor_lim = 2**(2**tensor_val)

    with open(str(tensor_val)+"_"+tensor_type + "_Decomp_data.txt", 'w') as d:
        while current_length < tensor_lim and len(higher_T) > 0: #Second part can be removed with a better bound
            non_unique = 0
            current_combos += higher_T

            higher_T = compute_higher_rank_tensors(current_combos, rk1_set, i, field_characteristic, numcores, zero_tensor, tensor_val)
            current_length += len(higher_T)

            d.write("Rank " + str(i) + ":\n")
            for decomp in higher_T:
                if len(higher_T[decomp]) > 1:
                    non_unique += 1
                d.write(str(decomp) + ": ")
                d.write(str(len(higher_T[decomp])) + ": ")
                [d.write("[" + str(x) + "], ") for x in higher_T[decomp]]
                d.write("\n")
            
            print("There are:", len(higher_T), "tensors of rank:", i, ":", non_unique, "are not unique")
            i += 1
    d.close()