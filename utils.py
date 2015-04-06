import qm
import wire
import agenda
import builder

def probe(name, awire, the_agenda):
    awire.add_action(
        lambda : print("{} {} new-value = {}".format(name,
                                                     the_agenda.get_curtime(),
                                                     awire.get_signal())))

# add this action after the specified delay
def after_delay(delay, action, the_agenda):
    the_agenda.add_action(action, delay + the_agenda.get_curtime())

def propagate(the_agenda):
    while not the_agenda.is_empty():
        first_action = the_agenda.remove_first_action()
        first_action() # execute this action

# create a circuit with the given minterms and don't care values
# FIXME: fix this function
def make_minterm_circuit(the_agenda, variables, minterms=[], dc=[]):
    minterms += dc
    numvars = len(variables)
    rep_minterms = [(minterm, qm.to_list(minterm, numvars)) for minterm in minterms]
    primes = qm.essential_primes(rep_minterms, variables)
    return builder.make_circuit(primes, variables, the_agenda)

# create a circuit with the given maxterms and don't care values
def make_maxterm_circuit(the_agenda, variables, maxterms=[], dc=[]):
    terms = set(range(1, (2 ** len(variables)) - 1))
    minterms = [maxterms[i] for i in range(len(maxterms)) if not maxterms[i] in terms]
    return make_minterm_circuit(the_agenda, variables, minterms, dc)
