import re
# Make dictionary where card ID looks up name, equation, true cost
normalizer = 1.864

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
        if ("!" in line) and (";" in line):
            card_name = line[1:-2]
            card_name = card_name.strip()
            names_matrix.append(card_name)
    #print(equation_matrix)
    # Remove semicolons from last value
    for equation in equation_matrix:
        equation[-1] = equation[-1][:-1]
    #print(equation_matrix)
    return equation_matrix, names_matrix

# Print the equation matrix
equation_matrix, names_matrix = parse_eqs()

# Get dictionary of bit Values
with open("Test_log_final.txt") as f:
    content = f.readlines()
means = {}
for line in content:
    content2 = re.sub("\s+",",",line.strip()).split(',')
    var = content2[0][:-1]
    means[var] = content2[1]

# Evaluate the worth of cards
card_est_values = []
card_real_values = []
card_deal = []
for i, card in enumerate(names_matrix):
    cur_equation = equation_matrix[i]
    card_real_values.append(cur_equation[-1])
    est_val = 0.0
    for bit in cur_equation[:-1]:
        minus = 1.0
        mult = 1.0
        if "-" in bit:
            bit = bit[1:]
            minus = -1.0
        if "*" in bit:
            [mult, bit] = bit.split("*")
        add_bit = minus * float(mult) * float(means[str(bit).upper()])
        est_val += add_bit
        #print(bit)
        #print(add_bit)
    card_est_values.append(round(est_val/normalizer,2))


for i in range(len(names_matrix)):
    #print(card_est_values[i],card_real_values[i])
    card_deal.append(card_est_values[i] - float(card_real_values[i]))

list1, names_matrix, card_est_values, card_real_values = zip(*sorted(zip(card_deal,names_matrix,card_est_values,card_real_values),reverse=True))
f = open("card_results.txt",'w')
summed_error = 0
for i in range(len(names_matrix)):
    f.write(str(names_matrix[i]) + " Est: " + str(card_est_values[i]) + " Actual: " + str(card_real_values[i]) + " How Good: " + str(round(list1[i],2)) + "\n")
    summed_error += list1[i]
print("--------------")
print(summed_error)
