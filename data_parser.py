import re
import numpy as np
import tensorflow as tf
from tensorflow import keras
from plot_labels import var_true_names
import matplotlib.pyplot as plt
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


def single_run():
    # Preprocessing to get all of the card info from files, set up datasets
    vars = get_vars()
    #print(vars)

    var_inds = var_dict(vars)
    #print(var_inds)

    equations = parse_eqs()
    #print(equations)
    processed_equations = []
    for eq in equations:
        #print(eq)
        eq_write = vectorize_eq(eq,var_inds)
        processed_equations.append(eq_write)
        #print(eq_write)

    # Set up simple neural network architecture with Keras
    t_epochs = 10
    T_DATA = []
    T_LBLS = []
    for line in processed_equations:
        T_DATA.append(line[:-1])
        T_LBLS.append(line[-1])
    T_DATA = np.array(T_DATA)
    T_LBLS = np.array(T_LBLS)
    #print(T_DATA)
    #quit()
    model = keras.Sequential([
        keras.layers.Dense(263, activation=tf.nn.relu),
        keras.layers.Dense(400, activation=tf.nn.relu),
        keras.layers.Dense(50, activation=tf.nn.relu),
        keras.layers.Dense(1, activation=tf.nn.relu)
    ])

    model.compile(optimizer=tf.train.AdamOptimizer(),
    loss=keras.losses.mean_squared_error)

    model.fit(T_DATA, T_LBLS, epochs=t_epochs)

    train_loss = model.evaluate(T_DATA, T_LBLS)
    print("Train Loss", train_loss)

    # Now that we have a good model that can reproduce the card values, check
    #  what values were assigned to single attributes
    single_dict = {}
    for var in vars:
        simulated_eq = [var, 69]
        eq_test = vectorize_eq(simulated_eq,var_inds)
        prediction = model.predict(np.array([eq_test[:-1]]), verbose=1, steps=None)
        print(var, prediction, "\n")
        single_dict[var] = prediction[0][0]

    print(single_dict)
    return single_dict

def var_plotter(var_list, compute_dict, true_names, sl):
    vars = var_list
    means = []
    stds = []
    super_labels = []
    for var in vars:
        means.append(np.mean(compute_dict[var]))
        stds.append(np.std(compute_dict[var]))
        super_labels.append(true_names[var])
    # Make some plots with the results
    # First, a plot of all var values, with labels
    ind = np.arange(len(vars))
    width = 0.35

    fig, ax = plt.subplots()
    rects = ax.bar(ind, means, width, yerr=stds, color='SkyBlue', label='Vars')

    ax.set_ylabel("Single Input Activation Score (Likely Cost Correlate)")
    ax.set_title("NN Computed Variable Values")
    ax.set_xticks(ind)
    if sl == "y":
        ax.set_xticklabels(super_labels)
    else:
        ax.set_xticklabels(vars)
    ax.legend()

    plt.show()


def main():
    num_runs = 2
    vars = get_vars()
    # Do the first run to get a baseline dictionary
    compute_dict = {}
    for var in vars:
        compute_dict[var] = []
    for i in range(num_runs):
        single_dict = single_run()
        for var in vars:
            compute_dict[var].append(single_dict[var])

    # Write a file with the result of this run
    with open("Test_log.txt","w") as f:
        for var in vars:
            mean = np.mean(compute_dict[var])
            std = np.std(compute_dict[var])
            f.write(var,": ",mean," +- ",std,"\n")

    # Get a dictionary with variable name to actual name mapppings
    true_names = var_true_names()
    # Plot list for personal resource values
    plot_list = ["REM","RES","RET","REP","REE","REH","REA","REMI","REF"]
    var_plotter(plot_list,compute_dict,true_names,"n")


if __name__ == "__main__":
    main()
