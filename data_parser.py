import re
import numpy as np

# There are 263 variables in the card equations, including one "D" for draft fee

########## Get variables from the file var_ID.txt
def get_vars():
    with open("var_ID.txt") as f:
        content = f.readlines()

    content2 = []
    for line in content:
        content2.append(re.sub("\s+",",",line.strip()).split(',')[0])

    var_ids = content2[334:]
    var_ids.append('D')
    return sorted(var_ids)

def parse_eqs():
    with open("TFM_cards.data") as f:
        content = f.readlines()

    equation_matrix = []
    for line in content:
        if "=" in line:
            line2 = line.strip().split(' ')
            #print(line2)
            line3 = []
            for piece in line2:
                if len(piece) > 1:
                    if ("ID" not in piece):
                        line3.append(piece)
                    if piece == "IDC":
                        line3.append(piece)
            equation_matrix.append(line3)
    #print(equation_matrix)
    # Remove semicolons from last value
    for equation in equation_matrix:
        equation[-1] = equation[-1][:-1]
    #print(equation_matrix)
    return equation_matrix

def var_dict(vars):
    var_dict = {k: v for v, k in enumerate(vars)}
    return var_dict

def vectorize_eq(sing_eq,var_inds):
    eq_write = np.zeros(len(var_inds)+1,dtype=int)
    for tag in sing_eq[:-1]:
        if "*" in tag:
            tag2 = tag.split("*")
            val = float(tag2[0])
            tag_name = tag2[1]
        else:
            val = 1
            tag_name = tag
        # Find correct index for this tag, and place val there
        indice = var_inds[tag_name.upper()]
        eq_write[indice] = val
    eq_write = list(eq_write)
    eq_write.append(int(sing_eq[-1]))
    return eq_write


def main():
    vars = get_vars()
    #print(vars)

    var_inds = var_dict(vars)
    #print(var_inds)

    equations = parse_eqs()
    #print(equations)
    processed_equations = []
    for eq in equations:
        print(eq)
        eq_write = vectorize_eq(eq,var_inds)
        processed_equations.append(eq_write)
        print(eq_write)



if __name__ == "__main__":
    main()
