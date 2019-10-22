import random

class Note:
    def __init__(self, pitch, timestamp, duration ):
        self.pitch = pitch
        self.timestamp = timestamp
        self.duration = duration

class Bar:
    def __init__(self):
        self.keys = []

    def generate(self):
        return True
    def add_key(self,key):
        self.keys.append(key)


class Automate:
    def __init__(self, initial_state, final_state):
        self.states=[]
        self.initial_state = initial_state
        self.final_state = final_state
        self.current_state = self.initial_state

    def __str__(self):
        string_to_return = ""
        string_to_return+="Initial State: "
        string_to_return+= self.initial_state.name
        string_to_return+="\n"
        string_to_return+="Final State: "
        string_to_return+=self.final_state.name
        string_to_return+="\n"
        for state in self.states:
            string_to_return+= state.name
            string_to_return += "\n"
            for transition in state.transitions_list:
                string_to_return +="\t"
                string_to_return +=transition.__str__()
            string_to_return += "\n"
        return string_to_return

    def __repr__(self):
        return self.__str__()

    def add_state(self,state):
        self.states.append(state)

    def has_finished(self):
        return self.current_state == self.final_state

    def next_state(self):
        #print( type(self.current_state.transitions_list[1].destination_state))
        self.current_state = self.current_state.transitions_list[1].destination_state
        print(self.current_state)


class Transition:
    def __init__(self, original_state, destination_state, symbol):
        self.original_state = original_state
        self.destination_state = destination_state
        self.symbol = symbol

    def __str__(self):
        return str(self.destination_state)

    def __repr__(self):
        return self.__str__()




class State:
    def __init__(self, name):
        self.name = name
        self.transitions_list = []

    def __str__(self):
        return  self.name

    def __repr__(self):
        return self.__str__()

    def add_transition(self, transition):
        self.transitions_list.append(transition)


initial_state = State("Initial State ")
state_8 = State("State 8 ")
state_16 = State("State 16 ")
state_24 = State("State 24 ")
state_32 = State("State 32 ")

transisition_0_8 = Transition(initial_state,state_8, 8)
initial_state.add_transition(transisition_0_8)

transisition_0_16 = Transition(initial_state,state_16, 16)
initial_state.add_transition(transisition_0_16)

transisition_0_24 = Transition(initial_state,state_24, 24)
initial_state.add_transition(transisition_0_24)

transisition_0_32 = Transition(initial_state,state_32, 32)
initial_state.add_transition(transisition_0_32)



transisition_8_16 = Transition(state_8 ,state_16, 8)
state_8.add_transition(transisition_8_16)

transisition_8_24 = Transition(state_8 ,state_24, 16)
state_8.add_transition(transisition_8_24)

transisition_8_32 = Transition(state_8 ,state_32,24)
state_8.add_transition(transisition_8_32)



transisition_16_24 = Transition(state_16 ,state_24, 8)
state_16.add_transition(transisition_16_24)

transisition_16_32 = Transition(state_16 ,state_32, 16)
state_16.add_transition(transisition_16_32)


transisition_24_32 = Transition(state_24 ,state_32, 8)
state_24.add_transition(transisition_24_32)

automate = Automate(initial_state,state_32)
automate.add_state(state_8)
automate.add_state(state_16)
automate.add_state(state_24)


print(automate)
while (automate.has_finished()==False):
    automate.next_state()
