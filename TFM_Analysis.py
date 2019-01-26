# Script to take existing TFM variable values, and compute with them
import re
from plot_labels import *

# Color options: SkyBlue, DarkSalmon, RoyalBlue, DarkViolet, Tomato, IndianRed
#https://matplotlib.org/examples/color/named_colors.html
color = "RoyalBlue"

#plot_list = ["REM","RES","RET","REP","REE","REH","REA","REMI","REF"] # Resources
#plot_list = ["TB","TSP","TPL","TM","TA","TPO","TJ","TEA","TC","TEV","TV","TW"] # Tags
#plot_list = ["ROXX2","ROXX4","ROXX5","ROXX6","ROXX7","ROXX8","ROXX9"] # Max Oxygen Requirements
#plot_list = ["ROXN2","ROXN4","ROXN5","ROXN6","ROXN7","ROXN8","ROXN9","ROXN11","ROXN13"] # Min Oxygen Requirements
#plot_list = ["PRM","PRS","PRT","PRP","PRE","PRH"] # Your resource production
#plot_list = ["DA1","DA2","DSP2","DSP4","DEA3","DV2"] # Discounts
#plot_list = ["GOX","GTE","GV","GTR"] # Global Parameters
#plot_list = ["PLC","PLOC","PLG","PLT","PLTA","PLCO","PLCOO"] # Placing Tiles
#plot_list = ["PO","GTR"]
#plot_list = ["PET","INS","WRM","DCP","RBW","SFL"] # which form of life is best?
plot_list = ["CD","CDPT","INV"] # card draw actions
with open("Test_log_final.txt") as f:
    content = f.readlines()

vars = []
means = {}
stds = {}

for line in content:
    content2 = re.sub("\s+",",",line.strip()).split(',')
    var = content2[0][:-1]
    vars.append(var)
    means[var] = content2[1]
    stds[var] = content2[3]
true_names = var_true_names()
plotter(plot_list, means, stds, true_names, "y", color)
