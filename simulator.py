import wire
import agenda
import basics
import utils

def inverter_test(the_agenda):
    a = wire.wire()
    b = wire.wire()
    inv = basics.inverter(a, b, the_agenda)
    utils.probe("a", a, the_agenda)
    utils.probe("b", b, the_agenda)

def and_gate_test(the_agenda):
    in1 = wire.wire()
    in2 = wire.wire()
    out = wire.wire()
    andg = basics.and_gate(in1, in2, out, the_agenda)
    utils.probe("in1", in1, the_agenda)
    utils.probe("in2", in2, the_agenda)
    utils.probe("out", out, the_agenda)

def half_adder_test(the_agenda):
    in1 = wire.wire()
    in2 = wire.wire()
    sum = wire.wire()
    carry = wire.wire()
    basics.half_adder(in1, in2, sum, carry, the_agenda)
    in1.set_signal(1)
    utils.probe("sum", sum, the_agenda)
    utils.probe("carry", carry, the_agenda)
    utils.propagate(the_agenda)
    in2.set_signal(1)
    utils.propagate(the_agenda)

def test_function(the_agenda):
    import qm, builder
    minterms = [4,8,9,10,11,12,14,15]
    variables = ['A','B','C','D']
    numvars = len(variables)
    minterms = [(minterm, qm.to_list(minterm, numvars)) for minterm in minterms]
    primes = qm.essential_primes(minterms, variables)
    wires, circuit = builder.make_circuit(primes, variables, the_agenda)
    wires['B'].set_signal(1)
    utils.probe('ckt', circuit, the_agenda)
    utils.propagate(the_agenda)

# entry into the simulator
def main():
    the_agenda = agenda.agenda()
    test_function(the_agenda)

if __name__ == '__main__':
    main()
