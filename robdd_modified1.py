
## minterms are represented as a list
## '0' represents bit 0
## '1' represents bit 1
## 'x' represents bit that can take any value

from copy import deepcopy
import sys # to use the constant 'sys.maxsize' which is the largest integer value in Python. Constant used in top_variable() method....

bit_one = 1
bit_zero = 0
bit_both = -1
var_not_there = '-' # to indicate that a variable is not there in the minterm
index_zero = 0
no_child = sys.maxsize
#NOTE: tautology is defined in the function main() in accordance with the number of variables in expression

#NOTE: fallacy is defined in the function main() 


bdd = {} # BDD data structure (dictionary)

def to_list(minterm, numvars):
    mask, l = 1 << (numvars - 1), []
    while mask > 0:
        if mask & minterm:
            l.append(bit_one)
        else:
            l.append(bit_zero)
        mask >>= 1
    return (l)


# function to compute the top-variable for the set of functions f,g,h

def top_variable(f,g,h,var_order): #f,g,h are of the form [[1,0,-,0],[1,0,1,1]...]... NOTE: decisions taken as part of implementation force the length of the lists f,g,h to be same at all times
	top_var_pos = sys.maxsize # this gives the max integer value in Python. Used only for initialization
	for minterm in f :
		for i in minterm:
			if i==bit_one or i==bit_zero:
				top_var_pos =  min(minterm.index(i),top_var_pos)
	for minterm in g :
		for i in minterm:
			if i==bit_one or i==bit_zero:
				top_var_pos =  min(minterm.index(i), top_var_pos) 
	for minterm in h :
		for i in minterm:
			if i==bit_one or i==bit_zero:
				top_var_pos = min(minterm.index(i), top_var_pos)  

	top_var = var_order[top_var_pos+1]
	return (top_var)

# ITE-operator - CONVENSION: ite(I,T,E) T is high child and E is low child
# Entry in Unique_Table - < uid, index, low_child_id, high_child_id > . 
# Caution:: the order of specifying low child and high child is opposite in the two. Be careful !!

def ITE(bdd,f,g,h,var_order): 


    #base case(incorrect termination condition)
    #if bdd['tautology'] in f  : return g # checking for a tautology. It  is the function '1'
    #if f == bdd["fallacy"] : return h   #fallacy is the function '0'
    #if g == h : return g 
    v = top_variable(f,g,h,var_order) # finding the top_variable for the set of functions {f,g,h}

    if bdd['tautology'] in f:
          r = ITE_mk(bdd,v,g,bdd["fallacy"],var_order)
          return r
    if f == bdd["fallacy"] :
          r = ITE_mk(bdd,v,g,h,var_order) 
          return r
    if g == h : # and f is a primary variable
          r = ITE_mk(bdd,v,g,g,var_order) 
          return r
    if bdd['tautology'] in g:
          r = ITE_mk(bdd,v,f,bdd["fallacy"],var_order) 
          return r
    

    # pseudo code for base condition
    #
    # if(terminal condition is reached) : 
    #    return ITE_mk (bdd, v, <list corresponding to low_child function>, <list corresponding to low_child function> )
    #
    
   # print ("ITE top variable =",v)
    f1 = deepcopy(f)
    g1 = deepcopy(g)
    h1 = deepcopy(h)
  #positive cofactor of f,g,h w.r.t. v
    f_v =  cofactor(f1, v, True, var_order) # splitting 'f' on the top variable 'v'
    g_v =  cofactor(g1, v, True, var_order) 
    h_v =  cofactor(h1, v, True, var_order) 

 
 #do deepcopy of f before passing it to the function
        
    f1 = deepcopy(f)
    g1 = deepcopy(g)
    h1 = deepcopy(h)

# negative cofactor of f,g,h w.r.t. v
    f_v_ =  cofactor(f1, v, False, var_order) # splitting 'f' on the top variable 'v'
    g_v_ =  cofactor(g1, v, False, var_order) 
    h_v_ =  cofactor(h1, v, False, var_order) 
     
    T = ITE(bdd,f_v,g_v,h_v,var_order) # f_v, g_v, h_v are the positive cofactors of f,g,h 
			   # w.r.t. variable 'v' . T is the high child 
    E = ITE(bdd,f_v_,g_v_,h_v_,var_order) # f_v_, g_v_, h_v_ are the negative cofactors of f,g,h w.r.t 'v'. E is the low child
    
    if T == E : return T  # reduction: captures the notion of merging identical nodes
  
    # Find the entry or create a new entry  in the Unique_Table with variable 'v' and children T and E
    r = ITE_mk(bdd,v,E,T,var_order) # 'r' is the 'unique id' which is assigned to each row of the Unique Table
#    print (r)
    return r  
   
### structure of Unique_Table is <id:(index,low_child,high_child)>
# index is associated with a level of the tree. All nodes at the same level have the same index. The leaf nodes have the highest index. The index keeps decreasing as we go to the root. The index of root node is 1. 

def bdd_initialize(var_order, tautology, fallacy): # initializing the bdd for some pre fixed variable order
    Unique_Table = {0 : ((len(var_order)+1),no_child,no_child) , 1 : ((len(var_order)+1), no_child,no_child)}

    bdd = {"u"              : 1             ,
           # "Computed_Table" : {}            ,
            'Unique_Table'   : Unique_Table ,
            'tautology'      : tautology,
             'fallacy'       : fallacy  }
#    print ("Unique Table: ", Unique_Table,"\n") 
    return bdd
# here "u" means unique id given to row

#ITE_mk function takes care of Unique table and Computed Table.... 
def ITE_mk(bdd,v_top,t,e,var_order):
    i = list(var_order.keys())[list(var_order.values()).index(v_top)] #index of the top-variable

 #checking if a particular entry is already there, by checking in the Computed Table
 #   if (i,t,e) in bdd["Computed_Table"]: return bdd["Computed_Table"][(i,t,e)]
   
 # Creating a new entry in the unique_table and the computed_table
    
    u = bdd["u"] + 1  # generating a new unique id for the new entry in the bdd  
#    bdd["Computed_Table"][(i,t,e)] = u
    try:
       value = bdd["Unique_Table"][u] 
       print ("\nvalue_bdd:",value,"\n")
       return (value)
    except KeyError:
    # Key is not present
       bdd["Unique_Table"][u] = (i,t,e)
       pass
   # if bdd["Unique_Table"][u]: (i,t,e)
    bdd["u"] = u
    
    return u



#The procedure cofactor(..) returns the cofactor of 'f' w.rt. the splitting 
#variable 'split_var' whose value is 'value'

#value is True for positive cofactor and False for negative cofactor

def cofactor(boolean_func, split_var, value, var_order): 

    result = []
    result = boolean_func[:] # creating a copy of the original list into result
    index_split_var_var_order = list(var_order.keys())[list(var_order.values()).index(split_var)]  # getting the key for the specified value in the dictionary  
    index_split_var_var_order =  index_split_var_var_order - 1
    #for i in range(0,len(boolean_func)): # the i implicant/minterm
    i = 0
    while i < len(result) :
        if result[i] == []: 
              i += 1 #this is done to skip the [], which is representative of a minterm which is not there in the SoP statement
              continue # continue transfers the control to the beginning if the while loop.
        if (result[i][index_split_var_var_order] == bit_one and  value is True ) or ( result[i][index_split_var_var_order] == bit_zero and  value is False ) :
           result[i][index_split_var_var_order] =  var_not_there	# put '-' for variable that has been forced to 1.
        elif (result[i][index_split_var_var_order] == bit_zero and  value is True)  or ( result[i][index_split_var_var_order] == bit_one and  value is False ) : 
           result[i] = [] #represent minterms, that are zero, with [].
        i += 1
    return (result)


def main():
    minterms = [2,3]
    main_boolean_func = [] # the original Boolean expression to be modified
    var_order = {} # stores the mapping <index for variable : variable>. index will determine the prefixed order. the index will also give the position of the variable in a minterm
    i = 1
    variables = ['A','B','C'] # these are the primary variables and are expected to to entered in accordence with the variable order. eg. ['B','C','A','D'] would imply that the variable order is B,C,A,D with B being the
                                  # top variable
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

# defining the minterm which represents the function ONE for the given expression (SoP)
    tautology  = ['-' for literal in variables]

    #print(tautology)

# defining the minterm which represents the function ZERO  for the given expression (SoP)
    fallacy = [[] for x in minterms]  

# get primary variable for the original function
    top_var = top_variable(main_boolean_func,fallacy,fallacy,var_order) 

# generate the top variable as list from original function
    top_var_transformed = [[] for i in range(0,len(minterms))]
    top_var_transformed[index_zero] = ['-' for literal in variables]
    top_var_transformed[index_zero][variables.index(top_var)] = bit_one
    #print(top_var_transformed) 

#########################################################################################################
   # print ("Original boolean expression: ", main_boolean_func)
   # print ("variable order :",var_order) 
#creating a copy of main_boolean_func before it is passed as argument at any place
    boolean_copy = []
    boolean_copy = deepcopy(main_boolean_func) #deepcopy causes the change in boolean_copy to not affect main_boolean_func. So the original function is intact in main_boolean_func.

    pos_cofactor = cofactor(boolean_copy, top_var, True, var_order) # splitting on 'A'

    boolean_copy = deepcopy(main_boolean_func)

    neg_cofactor = cofactor(boolean_copy, top_var, False, var_order)
    
   # print ("Positive cofactor :",pos_cofactor)
   # print ("Negative cofactor :",neg_cofactor)

   
## intializing bdd
    bdd = bdd_initialize(var_order, tautology, fallacy)

#invoking ITE operator on the original function
    ite_result = ITE(bdd,top_var_transformed,pos_cofactor,neg_cofactor,var_order)
   # print (ite_result)
    print(bdd) 

if __name__ == '__main__':
    main()

