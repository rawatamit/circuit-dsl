# combine minterms
def combine(m1, m2):
    if m1[1] == m2[1]:
        y = m1[0] ^ m2[0]
        if power_of_two(y):
            return (m1[0] & m2[0], m1[1] | y)
    return None

# number of bits set in x
def countbits(x):
    count = 0
    while x > 0:
        count += x & 1
        x >>= 1
    return count

# is x a power of two
def power_of_two(x):
    return x == (x & (~x + 1))

# cost of the minterms
def cost(minterms, numvars):
    res = 0 if len(minterms) == 1 else len(minterms)
    mask = (1 << numvars) - 1
    for minterm in minterms:
        tmask = ~minterm[1] & mask
        tcost = countbits(tmask)
        tcost = 0 if tcost == 1 else tcost
        res += tcost + countbits(~minterm[0] & tmask)
    return res

# find all the prime implicants
def all_primes(indices, numvars):
    sigma = [set() for i in range(numvars + 1)]
    for index in indices:
        sigma[countbits(index)].add((index, 0))
    
    primes = set()
    while sigma:
        tsigma = []
        redundant = set()
        for c1, c2 in zip(sigma[:-1], sigma[1:]):
            tc = set()
            for a in c1:
                for b in c2:
                    mx = combine(a, b)
                    if mx != None:
                        tc.add(mx)
                        redundant |= set([a, b])
            tsigma.append(tc)
        primes |= set(index for indices in sigma for index in indices) - redundant
        sigma = tsigma
    return list(primes)

# find the essential prime implicants
def essential_primes(primes, ones, numvars):
    table = []
    for one in ones:
        col = []
        for i in range(len(primes)):
            if primes[i][0] == (one & ~primes[i][1]):
                col.append(i)
        table.append(col)
    
    # we will modify this table until we get a reasonably small subset
    # that covers all of the terms in the function
    essentials = []
    if len(table) > 0:
        essentials = [set([i]) for i in table[0]]
    for i in range(1, len(table)):
        tessentials = []
        for essential in essentials:
            for pindex in table[i]:
                tx = set(essential)
                tx.add(pindex)
                add = True
                for j in range(len(tessentials) - 1, -1, -1):
                    if tx <= tessentials[j]:
                        del tessentials[j]
                    elif tx > tessentials[j]: # skip this
                        add = False
                if add:
                    tessentials.append(tx)
        essentials = tessentials
    
    mcost = 1<<30
    for essential in essentials:
        coverprimes = [primes[index] for index in essential]
        pcost = cost(coverprimes, numvars)
        if pcost < mcost:
            mcost = pcost
            res = coverprimes
    
    return mcost, res

# string representation of function from the minterms
# and the variables given as input
def function_to_str(minterms, variables):
    if isinstance(minterms,str):
        return minterms
    def parentheses(glue, array):
        if len(array) > 1:
            return ''.join(['(',glue.join(array),')'])
        else:
            return glue.join(array)
    or_terms = []
    for minterm in minterms:
        and_terms = []
        for j in range(len(variables)):
            if minterm[0] & 1<<j:
                and_terms.append(variables[j])
            elif not minterm[1] & 1<<j:
                and_terms.append('(not %s)' % variables[j])
        or_terms.append(parentheses(' and ', and_terms))
    return parentheses(' or ', or_terms)

def quine_mccluskey(variables, ones, dontcare):
    numvariables = len(variables)
    
    # does this function evaluate to true or false
    if len(ones) == 0:
        return 0, '0'
    if len(ones) + len(dontcare) == 1 << numvariables:
        return 0, '1'
    
    primes = all_primes(ones + dontcare, numvariables)
    return essential_primes(primes, ones, numvariables)

# for testing purposes
def main():
    variables = ['A', 'B']
    reduced = quine_mccluskey(variables,[3],[])[1]
    print(reduced)
    print(function_to_str(reduced, variables))

if __name__ == '__main__':
    main()
