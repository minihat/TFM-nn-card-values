# Make dictionary where card ID looks up name, equation, true cost
def parse_eqs():
    with open("TFM_cards.data") as f:
        content = f.readlines()

    names_matrix = []
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

# Print the equation matrix
eq_matrix = parse_eqs()
print(eq_matrix)
