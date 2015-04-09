## DOUBT:: how to represent the functions being passed to f,g,h
## f,g,h are ite-operators themselves

## minterms are represented as a list
## '0' represents bit 0
## '1' represents bit 1
## 'x' represents bit that can take any value
from copy import deepcopy

bit_one = 1
bit_zero = 0
bit_both = -1
var_not_there = '-' # to indicate that a variable is not there in the minterm
tautology = [[]]
fallacy = [[]]

def to_list(minterm, numvars):
    mask, l = 1 << (numvars - 1), []
    while mask > 0:
        if mask & minterm:
            l.append(bit_one)
        else:
            l.append(bit_zero)
        mask >>= 1
    return (l)


"""
# Shannon expansion of a Boolean function about a specified variable

def expand_shannon(boolean_func, split_var): # shannon expansion can be implemented using ite-operator
	new_boolean_func = split_var  
"""

def ITE(f,g,h):

## base case for recursion
    if f is tautology : return g #tautology is the function '1'
    if f is fallacy : return h   #falacy is the function '0'
    if g == h : return g 

  #  if (Lookup_Computed_Table([f,g,h]) : #correct the syntax
    p = Lookup_Computed_Table([f,g,h])
    return p

    v = top_variable(f,g,h)
    f_n = ITE(f_v,g_v,h_v) # f_v, g_v, h_v are the positive cofactors of f,g,h 
			   # w.r.t. variable 'v' 
    g_n = ITE(f_v_,g_v_,h_v_) # f_v_, g_v_, h_v_ are the negative cofactors of f,g,h w.r.t 'v'
    
    if f_n == g_n : return g_n  # reduction
     
    if not Lookup_Unique_Table(v,f_n,g_n):
        p = create_entry(v,f_n,g_n) #the entry is created in the Unique Table

    insert_computed_table({p:[f,g,h]}) # this statement is psedo code. 
                                      # p has to entered into the computed table                                      # with hash key (f,g,h)
    return p

"""
The procedure cofactor(..) returns the cofactor of 'f' w.rt. the splitting 
variable 'split_var' whose value is 'value'
"""
#value is True for positive cofactor and False for negative cofactor

def cofactor(boolean_func, split_var, value, var_order): 

    result = []
    result = boolean_func[:] # creating a copy of the original list into result
    index_split_var_var_order = list(var_order.keys())[list(var_order.values()).index(split_var)]   
    index_split_var_var_order =  index_split_var_var_order - 1
    #for i in range(0,len(boolean_func)): # the i implicant/minterm
    i = 0
    while i < len(result) :
        if (result[i][index_split_var_var_order] == 1 and  value is True ) or ( result[i][index_split_var_var_order] == 0 and  value is False ) :
           result[i][index_split_var_var_order] =  var_not_there	# put '-' for variable that has been forced to 1.
        elif (result[i][index_split_var_var_order] == 0 and  value is True)  or ( result[i][index_split_var_var_order] == 1 and  value is False ) : 
           result.remove(result[i]) #remove the minterms that amount to 0 because the split_var is forced to 0.
           i = i -1 # to cause the value of i to remain unchanged at the end of the loop because after removal of certain elements of the list the index of the remaining elemets will decrease
        i += 1
         #  result = boolean_func
         #  result.remove(result[i])
    return (result)


def main():
    minterms = [1,6,7]
    main_boolean_func = [] # the original Boolean expression to be modified
    var_order = {} # stores the mapping <index for variable : variable>. index will determine the prefixed order. the index will also give the position of the variable in a minterm
    i = 1
    variables = ['A','B','C']
    for var in variables:
        var_order.update({i:var}) # top variable in the variable order
    				  # has index 1 
        i += 1

    numvars = len(variables)
## The boolean function being minimized is represented as list of 
#  implicants/minterms. Each implicant is a list of literals(complemented or 
#   uncomplemented variable)
    for minterm in minterms:
        main_boolean_func.append(to_list(minterm,numvars)) 

    print ("variable order :",var_order) 
    print ("Original boolean expression: ", main_boolean_func)
#creating a copy of main_boolean_func before it is passed as argument at any place
    boolean_copy = []
    boolean_copy = deepcopy(main_boolean_func) #deepcopy causes the change in boolean_copy to not affect main_boolean_func. however the original function is intact in main_boolean_func.

    pos_cofactor = cofactor(boolean_copy, 'A', True, var_order)

    boolean_copy = deepcopy(main_boolean_func)

    neg_cofactor = cofactor(boolean_copy, 'A', False, var_order)
    
    print ("Positive cofactor :",pos_cofactor)
    print ("Negative cofactor :",neg_cofactor)

    
#invoking ITE operator on the original function
#    ITE([['A','-','-','-']],pos_cofactor,neg_cofactor)

if __name__ == '__main__':
    main()
