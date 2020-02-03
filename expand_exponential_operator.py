
# Use this to take a LaTeX string of an exponential operator with Paulis 
# in the exponent and convert it into CX, an rotation and Cliffords.

# General comment: we are not treating the sign in the exponent right now. 
# This can probably be done by just flippnig the sign of the angle, 
# which should happen automatically in the optimization I guess.

def parse_exp_str(exp_str):
    # We want to extract all the important information from the exponent, 
    # removing as much of the unnecessary stuff as possible.
    exponent = exp_str.split('e^')[1].strip()
    
    # We want to find two things:
    #  1-The rotation angle
    #  2-The operator in the exponent
    numerator = None
    denominator = None
    operator = None

    frac_idx = exponent.find(r'\frac{')
    
    open_brackets = 1
    start_pos = len(r'\frac{') + frac_idx
    pos = start_pos
    while open_brackets > 0:
        if exponent[pos] == r'{':
            open_brackets += 1
        elif exponent[pos] == r'}':
            open_brackets -= 1
        pos += 1
    numerator = exponent[start_pos:pos-1]

    open_brackets = 1
    start_pos = pos + 1
    pos = start_pos
    while open_brackets > 0:
        if exponent[pos] == r'{':
            open_brackets += 1
        elif exponent[pos] == r'}':
            open_brackets -= 1
        pos += 1
    
    denominator = exponent[start_pos:pos-1]

    operator = exponent[pos:-1]

    # Strong assumption that the angle is only in the numerator! Users beware...
    angle = numerator

    return operator, angle

def expand_exp_operator(operator, angle):
    # Now I would like to entangle as few times as possible
    # Let's first find the largest index which has to be changed,
    # add the rotation there and then work our way backwards to 
    # entangle as few qubits as possible.

    target = operator
    gate_sequence = ''

    pos = len(operator) - 1
    while target[pos] == 'I':
        pos -= 1

    # Add the rotational gate "in the middle"
    gate_sequence = f"R_{{X, {pos}}}({angle}) "

    previous = pos
    for i in range(pos-1, -1, -1):
        if target [i] != 'I':
            gate_sequence = f"CX_{{{i}, {previous}}} " + gate_sequence + f"CX_{{{i}, {previous}}} "
            previous = i

    # Now we have a lot of X gates, but we will probably have to 
    # change them into something else by applying some Cliffords.
    for i in range(pos, -1, -1):
        if target[i] == 'Y':
            gate_sequence = f"S_{{{i}}} " +  gate_sequence + f"S^\dagger_{{{i}}} "
        elif target[i] == 'Z':
            gate_sequence = f"H_{{{i}}} " +  gate_sequence + f"H_{{{i}}} "

    return gate_sequence

def expand_exp_operator_qasm(operator, angle, add_barriers=False):
    # Now I would like to entangle as few times as possible
    # Let's first find the largest index which has to be changed,
    # add the rotation there and then work our way backwards to 
    # entangle as few qubits as possible.
    def surround_with_barriers(gate_sequence, n_qubits):
        barrier_qasm = 'barrier '
        for i in range(n_qubits):
            barrier_qasm += f'q[{i}],'
        barrier_qasm = barrier_qasm[:-1] + ';\n'

        return barrier_qasm + gate_sequence + barrier_qasm

    target = operator
    gate_sequence = ''

    pos = len(operator) - 1
    while target[pos] == 'I':
        pos -= 1

    # Add the rotational gate "in the middle"
    gate_sequence = f"rx({angle}) q[{pos}];\n"
    if add_barriers: gate_sequence = surround_with_barriers(gate_sequence, len(operator))

    previous = pos
    for i in range(pos-1, -1, -1):
        if target [i] != 'I':
            gate_sequence = f"cx q[{i}],q[{previous}];\n" + gate_sequence + f"cx q[{i}],q[{previous}];\n"
            previous = i
    if add_barriers: gate_sequence = surround_with_barriers(gate_sequence, len(operator))

    # Now we have a lot of X gates, but we will probably have to 
    # change them into something else by applying some Cliffords.
    for i in range(pos, -1, -1):
        if target[i] == 'Y':
            gate_sequence = f"s q[{i}];\n" +  gate_sequence + f"sdg q[{i}];\n"
        elif target[i] == 'Z':
            gate_sequence = f"h q[{i}];\n" +  gate_sequence + f"h q[{i}];\n"
    if add_barriers: gate_sequence = surround_with_barriers(gate_sequence, len(operator))

    return gate_sequence

if __name__ == "__main__":
    tex_strs = []
    with open('example_gate_expansion.txt', 'r') as input_file:
        tex_strs = input_file.readlines()

    for tex_str in tex_strs:
        operator, angle = parse_exp_str(tex_str)
        # print(operator)
        # gate_sequence = expand_exp_operator(operator, angle)
        gate_sequence = expand_exp_operator_qasm(operator, 'pi/2', add_barriers=True)
        print(gate_sequence)