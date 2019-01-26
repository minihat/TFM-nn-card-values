with open("TFM_cards.data") as f:
    content = f.readlines()

cc = open("TFM_cards_new.data",'w')
for line in content:
    if '=' in line:
        line1, line2 = line.split('=')
        rhs = int(line2.strip()[:-1]) + 3
        write_line = str(line1) + "= " + str(rhs) + ";\n"
        cc.write(write_line)
    else:
        cc.write(line)
