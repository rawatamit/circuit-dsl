class tree:
    and_, or_, circuit_ = 1, 2, 3
    
    def and_node(left_node, right_node):
        self.node_type = and_
        self.left_node = left_node
        self.right_node = right_node
    
    def or_node(left_node, right_node):
        self.node_type = or_
        self.left_node = left_node
        self.right_node = right_node
   
    def circuit_node(circuit):
        self.node_type = circuit_
        self.circuit = circuit
    
    def get_left_node(self):
        return self.left_node
    
    def get_right_node(self):
        return self.right_node
    
    def get_circuit(self):
        return self.circuit
    
    def is_and(self):
        return self.node_type == and_
    
    def is_or(self):
        return self.node_type == or_
    
    def is_circuit(self):
        return self.node_type == circuit_

def make_circuit_node(circuit):
    return tree.ckt_node(circuit)

def make_and_node(left_node, right_node):
    return tree.and_node(tree.and_, left_node, right_node)

def make_or_node(left_node, right_node):
    return tree.or_node(tree.or_, left_node, right_node)
