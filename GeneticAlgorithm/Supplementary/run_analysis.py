import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


'''
Automatically get all csv file from the directory (".csv" and "_generalisation.csv") and returns a lineplot using data from the ".csv" file and a boxplot using data from "_generalisation.csv".

Input :
    str : path to folder containing the results

Output :
    png : lineplot of the fitness over time
    png : box plot of the fitness score
    
'''

# Add path to folder
path = "../Results_select"

os.chdir(path)

# Get all files
list_files = os.listdir()
prefix = list(dict.fromkeys([i.split('_')[1] for i in list_files]))

# Create dataframe with the average score of each rule and the parameter being tested
generalisation_table = pd.DataFrame()
data_table = pd.DataFrame(columns=['Rep', 'generation', 'fitness', 'param'])

# For each set of parameter
for p in prefix:
    fitness_files=[i for i in list_files if p in i and '.csv' in i and not 'generalisation' in i]
    generalisation_files= [i for i in list_files if p in i and 'generalisation.csv' in i]

    # Average the fitness score for each rule
    generalisation_mean = []
    for file in generalisation_files:
        generalisation_data = pd.read_csv(file)
        generalisation_mean.extend(list(generalisation_data.mean(axis=1)))
        print(len(generalisation_mean))
    generalisation_table[str(p)] = generalisation_mean

    # Average fitness score for each generation
    rep = 0
    for file in fitness_files:
        rep = rep + 1
        fitness_data = pd.read_csv(file, index_col=0)
        columns = [column for column in df.columns if column.startswith('rule')]
        fitness_data = fitness_data[columns].T
        fitness_mean = fitness_data.mean()
        fitness_mean.name = 'fitness'
        fitness_subset = fitness_mean.reset_index()
        fitness_subset['Rep'] = rep
        fitness_subset['param'] = p
        data_table = pd.concat([data_table, fitness_subset], ignore_index=True)

# Plots
boxplotgeneralisation = plt.figure()
boxplotgeneralisation = sns.boxplot(data=generalisation_table)
boxplotgeneralisation.figure.savefig('BoxplotGeneralisation.png')

lineplot_fitness = plt.figure()
lineplot_fitness = sns.lineplot(data=data_table, x='generation', y='fitness', hue='param')
lineplot_fitness.figure.savefig('LineplotFitness.png')

    


