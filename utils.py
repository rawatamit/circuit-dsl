import wire
import agenda

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
