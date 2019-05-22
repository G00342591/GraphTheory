# Shunting yard algorithm

def shunt(infix):
    """ The Shunting Yard Algorithm for converting infix regular expressions
        to postfix."""

    # Special characters for regular expressions and their precedence
    specials = {'*':3, '.':2,'|':1} 

    #Eventually be the output
    pofix = ""
    # Operator Stack
    stack = ""

    # Loop Through the string a character at a time
    for c in infix:
        # If open bracket push to the stack
        if c == '(':
            stack = stack + c
        # If a clvosting bracket, pop from stack, pish to output until open bracket
        elif c == ')':
            while stack[-1] != '(':
                pofix = pofix + stack[-1]
                stack = stack[:-1]
            stack = stack[:-1]
        # If its an operator, push to the stack after popping lower or equal precedence
        # operators from top of stack into output
        elif c in specials:
            while stack and specials.get(c,0) <= specials.get(stack[-1],0):
                pofix,stack = pofix + stack[-1], stack[:-1]
            stack = stack + c
        # Regular characters are pushed immediately to the output
        else:
            pofix = pofix + c

    # Pop all remaining operators from stack to output
    while stack:
        pofix,stack = pofix + stack[-1], stack[:-1]

    # Return postfix regex
    return pofix

#prints ab.c*d.|
##print(shunt("(a.b)|(c*.d)"))

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
    """Compiles a poftfix regular expression into an NFA"""

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


def followes(state):
    """ Return the set of states that can be reached from state following e arrows."""
    # Create a new set, with state as its only member
    states = set()
    states.add(state)

    # Check if state has arrows labelled e from it
    if state.label is None:
        # Check if edge1 is a state
        if state.edge1 is not None:
            # If there's an edge1, follow it.
            states |= followes(state.edge1)
        # Check if edge1 is a state
        if state.edge2 is not None:
            # If there's an edge2, follow it
            states |= followes(state.edge2)

    # Return the set of states.
    return states

def match(infix,string): 
    """ Matches string to infix regular expression,"""
    # Shunt and compile the regular expression.
    postfix = shunt(infix)
    nfa = compile(postfix)

    # The Current set of states and the enxt set of states.
    current = set()
    next = set()

    # Add the initial state to the current set.
    current |= followes(nfa.initial)

    # Loop through each character in the string.
    for s in string:
        # Loop through the current set of states.
        for c in current:
            # Check if that state is labelled s.
            if c.label == s:
                # Add the edge1 state to the next set.
                next |= followes(c.edge1)
        # set current to next, and clear out next
        current = next 
        next = set()

    # Check if the accept state is in the set of current states
    return(nfa.accept in current)



# Tests
#infixesTest = ["a.b.c*", "a.b(b|d).c*", "(a.b(b|d))*", "a.(b.b)*.c"]
#stringsTest = [ "", "abc", "abbc", "abcc", "abad", "abbbc"]
#for i in infixesTest:
#    for s in stringsTest:
#        print(match( i, s), i, s)

matchesNumber = input('Enter number of matches you wish to attempt: ')

infixes = []
strings = []

while matchesNumber != 0:
    infixInput = raw_input('Enter an infix: ')
    stringInput = raw_input('Enter an string: ')
    infixes.append(infixInput)
    strings.append(stringInput)
    matchesNumber -= 1

for i in infixes:
    for s in strings:
        print(match( i, s), i, s)   


