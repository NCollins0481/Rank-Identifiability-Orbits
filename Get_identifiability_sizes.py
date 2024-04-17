from collections import defaultdict

filename = "3_PSymmetric2_Decomp_data.txt"

identifiability_index = defaultdict()
with open(filename, 'r') as f:
    prev_rank = 2
    next(f)
    for line in f:
        A = line.split(": ")
        if 'Rank' in line:
            split_line = A[0].split(" ")[1]
            current_rank = int(split_line[:1])
            for ind in identifiability_index.keys():
                print(len(identifiability_index[ind]), "tensors of rank", prev_rank, "have index", ind)
            identifiability_index = defaultdict()
            prev_rank = current_rank

        if len(A) > 1:
            identifiability_num = A[1]
            identifiability_index.setdefault(identifiability_num, []).append(line)

for ind in identifiability_index.keys():
    print(len(identifiability_index[ind]), "tensors of rank", prev_rank, "have index", ind)