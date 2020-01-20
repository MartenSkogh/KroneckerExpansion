products = {'X*Y': 'iZ',
            'Y*Z': 'iX',
            'Z*X': 'iY',
            'X*Z': '-iY',
            'Z*Y': '-iX',
            'Y*Z': '-iZ',
            'X*X': 'I',
            'Y*Y': 'I',
            'Z*Z': 'I', 
            'I*I': 'I',
            'X*I': 'X',
            'I*X': 'X',
            'Y*I': 'Y',
            'I*Y': 'Y',
            'Z*I': 'Z',
            'I*Z': 'Z',
            'I*Qp': 'Qp',
            'Qp*I': 'Qp',
            'I*Qm': 'Qm',
            'Qm*I': 'Qm',
            'Qp*Z': 'Qp',
            'Z*Qp': '-Qp',
            'Z*Qm': 'Qm',
            'Qm*Z': '-Qm',
            'Qp*Qm': '1/2*(I-Z)',
            'Qm*Qp': '1/2*(I+Z)'}
    
def read_my_tex_kron(tex_str):
    symbs = ['I', 'Z', 'Qp', 'Qm']
    subs = {'Q^+': 'Qp',
            'Q^-': 'Qm'}
    kron_prods = tex_str.split(' ')
    kron_strs = []
    for kron_term in kron_prods:
        for key in subs:
            kron_term = kron_term.replace(key, subs[key])
        if kron_term[0] == '(' and kron_term[-1] == ')':
            kron_term = kron_term[1:-1]
        for sym in symbs:
            kron_term = kron_term.replace(sym, sym + ',')
        if kron_term[-1] == ',':
            kron_term = kron_term[:-1]
        kron_strs.append(kron_term)
        
    return [read_kron_str(kron_str) for kron_str in kron_strs]
    
def kron_to_tex(kron_arr):
    subs = {'Qp': 'Q^+',
            'Qm': 'Q^-'}
    tex_str = ''
    for elem in kron_arr:
        for key in subs:
            elem = elem.replace(key, subs[key])
        tex_str += elem
    return tex_str

def read_kron_str(k_str):
    return k_str.split(',')

def multiply(A, B):
    product = []
    for a,b in zip(A,B):
        product.append(a + '*' + b)

    return product

def substitute(kron_prod):
    substituted = []
    for kron_term in kron_prod:
        new_term = ''
        for key in products:
            if key in kron_term:
                if new_term != '':
                    #new_term += '*'
                    pass
                kron_term = kron_term.replace(key, products[key])
        substituted.append(kron_term)
    
    return substituted

def expand_kron(kron_prod):
    expanded = []
    for kron_term in kron_prod:
        pass

if __name__ == "__main__":
    my_tex_str = "(IIIQ^+) (IIQ^+Z) (Q^-ZZZ) (IQ^-ZZ)"
    terms = read_my_tex_kron(my_tex_str)
    print(terms)

    prod = terms[0]
    for term in terms[1:]:
        print(term)
        prod = multiply(prod, term)
    print(prod)
    subs = substitute(prod)
    print(subs)

    print(kron_to_tex(subs))
