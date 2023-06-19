import os

def transform(KS):
    nodes_dict = dict()
    nodes_ks = list(KS.nodes)
    for i in range(len(nodes_ks)):
        nodes_dict[nodes_ks[i]] = str(i)

    obs_dict = dict()
    symbols = KS.symbol_names
    for i in range(len(symbols)):
        obs_dict[symbols[i]] = str(i+1)
    obs_dict['epsilon'] = '0'
    obs_dict['tau'] = '-1'


    with open("text.smv", "w") as file:
        file.write("MODULE main\n")
        file.write("VAR\n")
        file.write("\tstate:")
        file.write(' ')
        file.write('0..')
        
        file.write(str(len(nodes_ks)-1))
        file.write(';\n')

        file.write("ASSIGN\n")
        file.write("\tinit(state) :=")
        file.write('{')

        for initial_node in KS.graph['initial']:
            file.write(nodes_dict[initial_node])
            file.write(', ')

        file.seek(file.tell() - 2, os.SEEK_SET)
        file.write('};')

        file.write("\n\tnext(state) :=\n")
        file.write("\t\tcase\n")

        for state in nodes_ks:
            file.write("\t\t\t(state=")
            file.write(nodes_dict[state])
            file.write("): {")
            for neighbor in KS.successors(state):
                file.write(nodes_dict[neighbor])
                file.write(', ')
            file.seek(file.tell() - 2, os.SEEK_SET)
            file.write('};\n')
        file.write("\t\tesac;")
        file.write("\n")

        file.write("DEFINE\n")
        file.write("\tstate_output :=\n")
        file.write("\t\tcase\n")

        for state in nodes_ks:
            file.write("\t\t\t(state=")
            file.write(nodes_dict[state])
            file.write("): ")
            file.write(state[0])
            file.write(";\n")
        file.write("\t\tesac;")
        file.write("\n\n")

        file.write("\tobs_output :=\n")
        file.write("\t\tcase\n")

        for state in nodes_ks:
            file.write("\t\t\t(state=")
            file.write(nodes_dict[state])
            file.write("): ")
            file.write(obs_dict[state[1]])
            file.write(";\n")
        file.write("\t\tesac;")
        file.write("\n\n")

        if KS.secret_states:
            file.write("\tsecret := ")
            for item in KS.secret_states:
                file.write("(state_output = ")
                file.write(item)
                file.write(") | ")
            file.seek(file.tell() - 2, os.SEEK_SET)
            file.write(';\n')

        file.write("\tinitial := ")
        for initial_state in KS.initial_states:
            file.write("(state_output = ")
            file.write(initial_state)
            file.write(") | ")
        file.seek(file.tell() - 2, os.SEEK_SET)
        file.write(';\n')

        file.write("\ttau := (obs_output=-1);")
        file.write("\n")

        if KS.fault_states:
            file.write("\tfault := ")
            for item in KS.fault_states:
                file.write("(state_output = ")
                file.write(item)
                file.write(") | ")
            file.seek(file.tell() - 2, os.SEEK_SET)
            file.write(';\n')

        
