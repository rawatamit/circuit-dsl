## minterms are represented as a list
## '0' represents bit 0
## '1' represents bit 1
## 'x' represents bit that can take any value
bit_one = 1
bit_zero = 0
bit_both = -1

def to_list(minterm, numvars):
    mask, l = 1 << (numvars - 1), []
    while mask > 0:
        if mask & minterm:
            l.append(bit_one)
        else:
            l.append(bit_zero)
        mask >>= 1
    return l

def is_different(bit1, bit2):
    return not bit1 == bit2

# assume m1 and m2 are the same size
def differ_by_one(m1, m2):
    count, index = 0, -1
    for i in range(len(m1)):
        if is_different(m1[i], m2[i]):
            count += 1
            index = i
    return count == 1, index

# combine m1 and m2
# index is the position where they differ
# CAUTION: m1 and m2 should only differ by one
def combine(m1, m2, index):
    l = m1[:]
    l[index] = bit_both
    return l

def can_cover(rminterm, minterm):
    for i in range(len(minterm)):
        if rminterm[i] != bit_both and is_different(rminterm[i], minterm[i]):
            return False
    return True

# True if any element in rminterms can cover minterm
def can_set_cover(rminterms, minterm):
    for rminterm in rminterms:
        if can_cover(rminterm, minterm):
            return True
    return False

def is_set_cover(rminterms, minterms):
    for minterm in minterms:
        if not can_set_cover(rminterms, minterm):
            return False
    return True

def find_smallest_set_cover(rminterms, minterms):
    for i in range(1, 2 ** len(rminterms)):
        index = len(rminterms) - 1
        subset, mask = [], 1 << index
        while mask > 0:
            if mask & i:
                subset.append(rminterms[index])
            mask >>= 1
            index -= 1
        if is_set_cover(subset, minterms):
            return subset

def get_signature(minterms):
    primes = [2,3,5,7,11,13,17,19,23,29]
    signature, index = 1, 0
    for term in sorted(minterms):
        signature += primes[index] * term
        index += 1
    return signature

def make_table_entry(nval, minterm):
    return [nval], minterm

def get_minterms(entry):
    return entry[0]

def get_reduced_minterm(entry):
    return entry[1]

def set_minterms(entry, new_minterms):
    entry[0] = new_minterms

def set_reduced_minterm(entry, reduced_minterms):
    entry[1] = reduced_minterms

def combination_pairs(table):
    xtable, modified, added = [], set(), set()
    changed = False
    for i in range(len(table)):
        m1 = get_reduced_minterm(table[i])
        for j in range(len(table)):
            m2 = get_reduced_minterm(table[j])
            # check if the two entries differ by a single bit
            byone, index = differ_by_one(m1, m2)
            if byone:
                terms = get_minterms(table[i]) + get_minterms(table[j])
                csign = get_signature(terms)
                added.add(i) # i has been used
                added.add(j) # j too
                # if these minterms are not already in the set
                if csign not in modified:
                    changed = True
                    modified.add(csign)
                    xtable.append((terms, combine(m1, m2, index)))
    
    for i in range(len(table)):
        if i not in added:
            xtable.append(table[i])
    return changed, xtable

def essential_primes(minterms, variables):
    numvars = len(variables)
    table = [make_table_entry(nval, minterm) for nval, minterm in minterms]
    changed = True
    while changed:
        changed, table = combination_pairs(table)
    return find_smallest_set_cover([get_reduced_minterm(entry) for entry in table],
                                   [mterm for _, mterm in minterms])

def main():
    minterms = [(x, to_list(x, 3)) for x in [1,4,5,6,7]]
    variables = ['A','B','C']
    #find_smallest_set_cover([1,2,3,4], [['1','0']], ['A','B'])
    print(essential_primes(minterms, variables))

if __name__ == '__main__':
    main()
