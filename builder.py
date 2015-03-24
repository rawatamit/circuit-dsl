import wire
import tree
def Builder(tr, primary_var):
	# base case (to be written)
	if isLiteral(tr, primary_var):
		make_circuit_node(tr)
		return tr 
	# recursive case
	elif (tr.is_and() and (not tr.is_circuit())):
#		temp_out = chr(ord(temp_out)+1) #the temporary output variable 
		gate_str = "and_gate" 
		in1 = Builder(tr.get_left_node(), primary_var)
		in2 = Builder(tr.get_right_node(), primary_var)
                make_and_gate(in1, in2)
		make_circuit_node(tr)
	#	out = gate_str + "(" + str(in1) + "," + str(in2) + "," + temp + ",the_agenda)" 
		
         #       return out

        elif (tr.is_or() and (not tr.is_circuit())):
		gate_str = "or_gate" 
		in1 = Builder(tr.get_left_node(), primary_var)
		in2 = Builder(tr.get_right_node(), primary_var)
                make_or_gate(in1, in2)
		make_circuit_node(tr)
	#	out = gate_str + "(" + str(in1) + "," + str(in2) + "," + temp + ",the_agenda)" 
        #        return out

	return tr
def isLiteral(node, primary_var):
	for var in primary_var:
		if node == var or node == (not var):
			return True

def main():
	tr = tree()
	primary_var = ['A', 'B', 'C', 'D']
        primary_var += ['OUT'] 
        S1 = ""
	S4 = "the_agenda):"
        S = "def circuit("
        new_line = "\n"
        for var in primary_var:
		S1+= (str(var)+',')
        S5 = S + S1 + S4 + new_line
        print (S5) 
	Builder(tr, primary_var)

if __name__ == '__main__':
    main()
             
