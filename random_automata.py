from networkx.classes.digraph import DiGraph
from random import sample, randint, choice, shuffle
from random_choose import choose
from cycle_detection import TarjansAlgorithm, is_self_loop, JohnsonsAlgorithm

def random_automata(
    num_states,
    num_events,
    num_symbols,
    min_trans_per_state=0,
    max_trans_per_state=None,
    num_init=1,
    num_secret=0,
    num_uo=0,
    num_faultevent=0
):
    generator = randomAutomata(
        num_states,
        num_events,
        num_symbols,
        min_trans_per_state,
        max_trans_per_state,
        num_init,
        num_secret,
        num_uo,
        num_faultevent
    )

    success = False
    while not success:
        generator.generate_automaton()

        generator.all_state_reachable()
        
        generator.generate_mask()
        #print("mask generated!")
        
        success = generator.has_no_unobservable_loops()
        #success = True
        print(success)

        

    print("automaton generated!")
    generator.generate_fault_events()

    return generator

class randomAutomata(DiGraph):
    def __init__(
        self,
        num_states,
        num_events,
        num_symbols,
        min_trans_per_state,
        max_trans_per_state,
        num_init,
        num_secret,
        num_uo,
        num_faultevent
    ):
        self.num_states = num_states
        self.num_events = num_events
        self.num_symbols = num_symbols
        self.min_trans_per_state = min_trans_per_state
        if max_trans_per_state:
            self.max_trans_per_state = max_trans_per_state
        else:
            self.max_trans_per_state = num_events

        self.num_init = num_init
        self.num_secret = num_secret
        self.num_uo = num_uo
        self.num_faultevent = num_faultevent


        DiGraph.__init__(self, initial=set())
        for i in range(self.num_states):
            self.add_node(str(i))

        self.event_names = list()
        self.generate_event_names()

        self.symbol_names = list()
        self.generate_symbol_names()

        self.mask = dict()

        self.secret_states = list()
        self.generate_secret()

        self.fault_states = list()
        self.fault_states_set = set()

    def all_state_reachable(self):
        tarjan = TarjansAlgorithm(self)
        all_scc = tarjan.strongly_connected_components(list(self.nodes)[0])

        initial_scc = list()
        for scc in all_scc:
            states_of_scc = list()
            for node in scc:
                states_of_scc.append(node[0])
            for initial_state in list(self.graph['initial']):
                if initial_state in states_of_scc:
                    initial_scc.append(scc)

        already_set = set()
        todo_list = list()

        for initial_state in list(self.graph['initial']):
            todo_list.append(initial_state)

        while len(todo_list) != 0:
            state = todo_list.pop()
            already_set.add(state)

            for next_state in self.successors(state):
                if next_state not in already_set:
                    todo_list.append(next_state)

        not_reachable_states = list()
        for state in list(self.nodes):
            if state not in already_set:
                not_reachable_states.append(state)

        for scc in all_scc:
            states_of_scc = list()
            for node in scc:
                states_of_scc.append(node[0])
            for state in not_reachable_states:
                if state in states_of_scc:
                    state_to_connect = choice(states_of_scc)
                    event_to_connect = choice(self.event_names)

                    initial_scc_chosen = choice(initial_scc)
                    predecessor_chosen = choice(initial_scc_chosen)[0]

                    self.add_edge(predecessor_chosen, state_to_connect, event=event_to_connect)

    def reachable_satisfied(self):
        already_set = set()
        todo_list = list()

        for initial_state in list(self.graph['initial']):
            todo_list.append(initial_state)

        while len(todo_list) != 0:
            state = todo_list.pop()
            already_set.add(state)

            for next_state in self.successors(state):
                if next_state not in already_set:
                    todo_list.append(next_state)

        not_reachable_states = list()
        for state in list(self.nodes):
            if state not in already_set:
                not_reachable_states.append(state)

        if not not_reachable_states:
            print("all reachable!")
        else:
            print("not_reachable_states:", not_reachable_states)

    def generate_fault_events(self):
        #print('initial states:', self.graph['initial'])
        unobservable_events = list()
        #print('mask:', self.mask)
        for event in self.event_names:
            if self.mask[event] == 'epsilon':
                unobservable_events.append(event)
        fault_events = sample(unobservable_events, self.num_faultevent)
        #print('fault events:', fault_events)

        for state in self.nodes:    
            self.nodes[state]['fault'] = 'nf'

        todo_list = list()
        already_set = set()
        for initial_state in self.graph['initial']:
            todo_list.append(initial_state)

        while len(todo_list)!=0:
            #print("todo_list:", todo_list)
            state = todo_list.pop()
            state_neighbors = list(self.successors(state))
            for successor in state_neighbors:
                if self.edges[(state, successor)]['event'] in fault_events:
                    self.mark_fault_states(successor)
            already_set.add(state)

            for next_state in state_neighbors:
                if next_state not in already_set:
                    todo_list.append(next_state)

        self.fault_states = list(self.fault_states_set)
        #print('fault states:', self.fault_states)

    def mark_fault_states(self, state):
        tomark_list = list()
        already_mark_set = set()
        tomark_list.append(state)
        while len(tomark_list) != 0:
            fault_state = tomark_list.pop()
            already_mark_set.add(fault_state)
            self.nodes[fault_state]['fault'] = 'f'
            self.fault_states_set.add(fault_state)

            fault_state_neighbors = self.successors(fault_state)
            for next_state in fault_state_neighbors:
                if next_state not in already_mark_set:
                    tomark_list.append(next_state)

    

    def generate_secret(self):
        states_to_label = list(self.nodes)
        secret_states = sample(states_to_label, self.num_secret)
        self.secret_states = secret_states
        for state in secret_states:
            self.nodes[state]['secret'] = 's'
        for state in secret_states:
            states_to_label.remove(state)
        for state in states_to_label:
            self.nodes[state]['secret'] = 'ns'

    def generate_mask(self):
        events_to_label = self.event_names.copy()

        events_unobs = sample(events_to_label, self.num_uo)
        for item in events_unobs:
            events_to_label.remove(item)
        for event in events_unobs:
            self.mask[event] = 'epsilon'
        
        observation_list = choose(self.num_events-self.num_uo, self.num_symbols)
        for i in range(len(observation_list)):
            events_for_obs_i = sample(events_to_label, observation_list[i])
            for item in events_for_obs_i:
                events_to_label.remove(item)
            for event in events_for_obs_i:
                self.mask[event] = self.symbol_names[i]
        for edge in self.edges:
            self.edges[edge]['obs'] = self.mask[self.edges[edge]['event']]



    def generate_event_names(self):
        for i in range(self.num_events):
            name = 'e' + str(i+1)
            self.event_names.append(name)


    def generate_symbol_names(self):
        for i in range(self.num_symbols):
            name = 'o' + str(i+1)
            self.symbol_names.append(name)

    def make_successors(self, state, is_init):
        num_transitions = randint(self.min_trans_per_state, self.max_trans_per_state)

        if is_init and num_transitions == 0:
            num_transitions =1

        avail_states = list(self.nodes)
        avail_events = list(self.event_names)

        for _ in range(num_transitions):
            event_name = None
            next_state = None

            while next_state is None:
                if avail_events:
                    event_name = choice(avail_events)
                    avail_events.remove(event_name)
                if event_name is None:
                    continue

                avail_states = list(self.nodes)
                for successor in self.successors(state):
                    t = (state, successor)
                    if self.edges[t]['event'] == event_name and successor in avail_states:
                        avail_states.remove(successor)
                if avail_states:
                    next_state = choice(avail_states)
                else:
                    avail_events.remove(event_name)

            self.add_edge(state, next_state, event=event_name)

        self.already_set.add(state)

        if state in self.todo_set:
            self.todo_set.remove(state)

    def save_todo_successors(self, state):
        for successor in self.successors(state):
            if successor != state and successor not in self.already_set:
                self.todo_successors.add(successor)


    def generate_automaton(self):
        self.todo_set = set(self.nodes)
        self.already_set = set()
        self.todo_successors = set()
        self.already_successors = set()
        
        if self.num_init == 1:
            self.graph['initial'].add(list(self.nodes)[0])
        else:
            ids = sample(range(self.num_states), self.num_init)
            for i in ids:
                self.graph['initial'].add(list(self.nodes)[i])

        for state in self.graph['initial']:
            self.make_successors(state, True)
            self.save_todo_successors(state)

        
        while True:
            while self.todo_successors:
                state = self.todo_successors.pop()
                self.make_successors(state, False)
                self.already_successors.add(state)

            if not self.todo_set:
                break

            while self.already_successors:
                state = self.already_successors.pop()
                self.save_todo_successors(state)

            if not self.todo_successors or len(self.already_set) == self.num_states:
                break


        while self.todo_set:
            state = self.todo_set.pop()
            if not self.predecessors(state):
                candidate_predecessors = list(self.already_set)

                okay_predecessor = None
                good_predecessor = None
                event = None

                while True:
                    okay_predecessor = choice(candidate_predecessors)
                    candidate_predecessors.remove(okay_predecessor)

                    if len(self.successors(okay_predecessor)) < self.max_trans_per_state:
                        good_predecessor = okay_predecessor
                        event = choice(self.find_unused_events(good_predecessor))
                        
                        break

                    if not candidate_predecessors:
                        break

                if good_predecessor in None:
                    unused_events = self.find_unused_events(self, okay_predecessor)
                    if unused_events:
                        event = choice(unused_events)
                    else:
                        candidate_predecessors = list(self.already_set)
                        shuffle(candidate_predecessors)
                        for okay_predecessor in candidate_predecessors:
                            unused_events = self.find_unused_events(okay_predecessor)
                            if unused_events:
                                event = choice(unused_events)
                                break

                    if event is not None:
                        self.add_edge(okay_predecessor, state, event=event)
                        
            self.make_successors(state, False)


    def has_no_unobservable_loops(self):
        johnson = JohnsonsAlgorithm(self)
        all_cycles = johnson.simple_cycles(self)

        for cycle in all_cycles:
            binary_for_cycle = list()
            for i in range(len(cycle)-1):
                if self.edges[(cycle[i], cycle[i+1])]['obs'] == 'epsilon':
                    binary_for_cycle.append(True)
                else:
                    binary_for_cycle.append(False)

            if all(binary_for_cycle):
                return False
        return True

    def find_unused_events(self, state):
        events = self.event_names.copy()
        for successor in self.successors(state):
            if self.edges[(state, successor)]['event'] in events:
                events.remove(self.edges[(state, successor)]['event'])
        return events
        




        

        
