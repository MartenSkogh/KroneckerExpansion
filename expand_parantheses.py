

def parse_tex_str(tex_str):

    subs = {'-Q^+': '-X+iY',
            'Q^+': 'X+-iY',
            '-Q^-': '-X+-iY',
            'Q^-': 'X+iY'}

    tex_str = tex_str.replace('^+', '^+,')
    tex_str = tex_str.replace('^-', '^-,')

    for key in subs:
        tex_str = tex_str.replace(key, subs[key])

    if tex_str[-1] == ',':
        tex_str = tex_str[:-1]

    return tex_str.split(',')

def expand_addition(arr):
    expanded_terms = arr[0].split('+')
    for term in arr[1:]:
        new_terms = []
        sub_terms = term.split('+')
        for sub_term in sub_terms:
            for exp_term in expanded_terms:
                new_terms.append(exp_term + sub_term)
        
        expanded_terms = new_terms

    return expanded_terms

def clean_up_imaginary(elem):
    nbr_i = elem.count('i')
    if nbr_i % 4 == 0:
        imaginary = ''
    elif nbr_i % 4 == 3:
        imaginary = '-i'
    elif nbr_i % 4 == 2:
        imaginary = '-'
    elif nbr_i % 4 == 1:
        imaginary = 'i'

    elem = elem.replace('i', '')
    elem = imaginary + elem

    return elem

def clean_up_sign(elem):
    nbr_minus = elem.count('-')
    if nbr_minus % 2 == 0:
        sign = ''
    elif nbr_minus % 2 == 1:
        sign = '-'

    elem = elem.replace('-', '')
    elem = sign + elem

    return elem

def clean_up(arr):
    clean_arr = []
    for elem in arr:
        elem = clean_up_imaginary(elem)
        elem = clean_up_sign(elem)
        clean_arr.append(elem)

    return clean_arr

if __name__ == "__main__":
    tex_strs = []
    with open('input_terms.txt', 'r') as input_file:
        tex_strs = input_file.readlines()

    for tex_str in tex_strs:
        tex_str = tex_str.strip()
        #print(tex_str)

        parsed_str = parse_tex_str(tex_str)
        #print(parsed_str)

        expanded_terms = expand_addition(parsed_str)
        #print(expanded_terms)

        cleaned_terms = clean_up(expanded_terms)
        print(' + '.join(cleaned_terms).replace('+ -','- '))
