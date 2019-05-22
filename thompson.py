# Thompsons's construction

# Represents a state with two arrows, labbeled by label
# Use none for a label to represent e arrow
class state:
    label = None
    edge1 = None    
    edge2 = None

# An NFA is represented by it's initial and accept states
class nfa:
    initial = None
    accept = None

    def __init__(self, initial, accept):
        self.initial = initial  
        self.accept = accept

def compile(pofix):
    nfastack = []

    for c in pofix:
        if c == '.':
            # Pop two nfas off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # Connect first NFA's accept state to the second's initial
            nfa1.accept.edge1 = nfa2.initial
            # Push NFA to the stack  
            newnfa = nfa(nfa1.initial, nfa2.accept)
            nfastack.append(newnfa)

        elif c == '|':
            # Pop two NFA's off the stack
            nfa2 = nfastack.pop()
            nfa1 = nfastack.pop()
            # Create a new initial state, connect it to the initial state
            # of the two NFA's popped from the stack
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            ## Create a new accept state, connecting the accepting states
            # of the two NFA#s popped from the stack to the new st
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            # push new NFA to the stack
            newnfa = nfa(initial,accept)
            nfastack.append(newnfa)
        elif c == '*':
            # Pop a single nfa from the stack
            nfa1 = nfastack.pop()
            # Create new initial and accept states
            initial = state()
            accept = state()
            # Join the new initial state to the nfa1's initial state and the new accept state
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # join the old accept state to the new accept states and nfa1's initial state
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            #Push the new nfa to the stack
            newnfa = nfa(initial,accept)
            nfastack.append(newnfa)
        else:
            #create a new initial and accept states
            accept = state()
            initial = state()
            #Join the initial state and the accept state using an arrow labelled c
            initial.label = c
            initial.edge1 = accept
            # Push new NFA to the stack
            newnfa = nfa(initial, accept)
            nfastack.append(newnfa)

    # nfa stack should only have a single nfa on it at this point
    return nfastack.pop()

print(compile("ab.cd.|"))


