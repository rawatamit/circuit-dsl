import qm
import wire
import basics
import agenda

def get_wire(variable, bit_val, wires, the_agenda):
    in_wire = wire.wire()
    output_wire = in_wire
    
    # check whether the bit corresponding to the
    # variable is turned on or not
    if bit_val == qm.bit_one:
        strvar = variable
    else: # bit_zero
        strvar = '~' + variable
        output_wire = wire.wire()
        basics.inverter(in_wire, output_wire, the_agenda)
    
    # cache the wires to avoid duplicating inputs
    if strvar not in wires:
        wires[strvar] = output_wire
    return wires[strvar]

def build_circuitry(wires, the_agenda, gate):
    ckt_output = wires.pop()
    while len(wires) > 0:
        cur_output = wire.wire()
        cur_wire = wires.pop()
        gate(ckt_output, cur_wire, cur_output, the_agenda)
        ckt_output = cur_output
    return ckt_output

def build_and_circuitry(wires, the_agenda):
    return build_circuitry(wires, the_agenda, basics.and_gate)

def build_or_circuitry(wires, the_agenda):
    return build_circuitry(wires, the_agenda, basics.or_gate)

def build_minterm(minterm, variables, wires, the_agenda):
    index, mwires = len(variables) - 1, []
    for i in range(len(minterm)-1, -1, -1):
        if minterm[i] != qm.bit_both: # don't need to add a wire for a bit not needed
            mwires.append(get_wire(variables[index], minterm[i], wires, the_agenda))
        index -= 1
    return build_and_circuitry(mwires, the_agenda)

def make_circuit(minterms, variables, the_agenda):
    wires = {}
    mckts = [build_minterm(minterm, variables, wires, the_agenda)
             for minterm in minterms]
    return wires, build_or_circuitry(mckts, the_agenda)

def all_subsets(variables, wires, circuit, the_agenda):
    import utils
    index, numvars = 0, len(variables)
    for subset in range(0, 2 ** numvars):
        mask = 1 << (numvars - 1)
        index = 0
        while mask > 0:
            variable = variables[index]
            if mask & subset:
                try:
                    wires[variable].set_signal(1)
                    print(variable, 1, end=' ')
                except Exception: pass
            else:
                try:
                    wires[variable].set_signal(0)
                    print(variable, 0, end=' ')
                except Exception: pass
            mask >>= 1
            index += 1
        print("\n===========================================")
        utils.propagate(the_agenda)

def main():
    import utils
    variables = ['A','B','C','D']
    minterms = [[-1, 1, 0, 0], [1, -1, 1, -1], [1, 0, -1, -1]]
    the_agenda = agenda.agenda()
    wires, circuit = make_circuit(minterms, variables, the_agenda)
    print(wires, circuit)
    utils.probe('ckt', circuit, the_agenda)
    wires['B'].set_signal(1)
    utils.propagate(the_agenda)
    #all_subsets(variables, wires, circuit, the_agenda)

if __name__ == '__main__':
    main()
