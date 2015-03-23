import wire
import utils

inverter_delay = 2
and_gate_delay = 3
or_gate_delay = 3

def logical_not(x):
    if x == 0: return 1
    elif x == 1: return 0
    else: raise ValueError("invalid signal: {}".format(x))

def logical_and(x, y):
    if x in (0, 1) and y in (0, 1):
        if x == 1 and y == 1:
            return 1
        else:
            return 0
    else:
        raise ValueError("invalid signals: {} {}".format(x, y))

def logical_or(x, y):
    if x in (0, 1) and y in (0, 1):
        if x == 1 or y == 1:
            return 1
        else:
            return 0
    else:
        raise ValueError("invalid signals: {} {}".format(x, y))

def inverter(input, output, the_agenda):
    def invert_input():
        new_val = logical_not(input.get_signal())
        utils.after_delay(inverter_delay,
                          lambda : output.set_signal(new_val),
                          the_agenda)
    input.add_action(invert_input)

def and_gate(in1, in2, output, the_agenda):
    def and_action():
        new_val = logical_and(in1.get_signal(), in2.get_signal())
        utils.after_delay(and_gate_delay,
                          lambda : output.set_signal(new_val),
                          the_agenda)
    in1.add_action(and_action)
    in2.add_action(and_action)

def or_gate(in1, in2, output, the_agenda):
    def or_action():
        new_val = logical_or(in1.get_signal(), in2.get_signal())
        utils.after_delay(or_gate_delay,
                          lambda : output.set_signal(new_val),
                          the_agenda)
    in1.add_action(or_action)
    in2.add_action(or_action)

def half_adder(in1, in2, sum, carry, the_agenda):
    d = wire.wire()
    e = wire.wire()
    or_gate(in1, in2, d, the_agenda)
    and_gate(in1, in2, carry, the_agenda)
    inverter(carry, e, the_agenda)
    and_gate(d, e, sum, the_agenda)
