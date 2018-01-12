"""

inter-promo project
group n°8

author: nicolas paillier
checked by: meryem rejouany

this program aims:
    - to read a json file containing the whole of relevant terms
        and their sum of term frequencies per day
    - to apply a linear regression ; ie. to calculate the coefficient and
        the intercept value of the regression line
    - to display the line plot depicting the evolution of the sum_tf
        over time ; and the regression line
    - to define the trend (rise, drop) according to the coefficient value

"""

#packages
import json
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.api import OLS
#from statsmodels.graphics.regressionplots import abline_plot

#dataset (example)
#words and their sum of tf per day
data_tmp = {"trump" : [0, 1, 1, 3, 2, 4, 5, 5, 6, 8, 7, 9, 11, 10, 11, 13, 13, 15],
            "macron" : [17, 15, 14, 15, 13, 12, 10, 9, 9, 8, 8, 7, 8, 6, 5, 4, 3, 2],
            "ceremonie" : [0, 0, 2, 1, 3, 4, 5, 6, 6, 5, 4, 4, 3, 3, 2, 1, 1, 0],
            "aeroport" : [3, 3, 2, 3, 3, 4, 2, 2, 4, 3, 3, 3, 4, 4, 2, 3, 2, 2],
            "tempete" : [5, 5, 5, 4, 5, 4, 4, 5, 5, 6, 6, 5, 5, 4, 4, 4, 5, 4],
            "impot" : [20, 18, 19, 17, 16, 16, 15, 13, 13, 12, 10, 9, 10, 8, 6, 5, 3, 2]}

#write the json file
with open('H:/SID Toulouse/Projet inter-promo/code/data_tmp.json', 'w', encoding = "utf-8") as file:
    data_tmp = json.dump(data_tmp, file, indent = 4)

#read the json file
with open('H:/SID Toulouse/Projet inter-promo/code/data_tmp.json', 'r') as file:
    data_tmp = json.load(file)

#extract keys and values from the json file
#input: json
def extract_keys_values(data_tmp):
    #initialisation of the "keys" and "values" lists
    keys = []
    values = []
    
    #for each entry in the json file
    for k, v in data_tmp.items():
        keys.append(k)
        values.append(v)
    
    return(keys, values)

keys, values = extract_keys_values(data_tmp)

#line plot depicting the sum of tf per day for each word
for i in range(len(data_tmp)):
    print(keys[i])
    plt.plot(values[i], color = 'r', lw = 2)
    plt.figure()

#multiple lines (all words existing in the json file)
plt.plot(np.transpose(values))

#linear regression
def linear_regression(data_tmp):
    reg_coeff = []
    reg_intercept = []
    dict_linreg = {}
    
    #intercept value and coefficient calculation
    #addition of the regression line on the plot
    for k, v in data_tmp.items():
        mat_x = np.ones((len(v), 2))
        mat_x[:,1] = np.arange(0, len(v))
        
        reg = OLS(v, mat_x)
        results = reg.fit()
        
        reg_coeff.append(results.params[1])
        reg_intercept.append(results.params[0])
        
        dict_linreg[k] = [results.params[1], results.params[0]]
        
        #fig = abline_plot(model_results = results, color = 'r', lw = 2)
        
        #reg_plot = fig.axes[0]
        #reg_plot.plot(mat_x[:,1], values[i], color = 'b')
        #reg_plot.margins(.1)

    return(dict_linreg)

dict_linreg = linear_regression(data_tmp)

#trend (increase, decrease) according to the coefficient value
def trend():
    dict_trend = {}
    dict_linreg = linear_regression(data_tmp)
    for k, v in dict_linreg.items():
        for j in range(1, len(v)):
            if v[j] > 0:
                dict_trend[k] = "rise"
            else:
                dict_trend[k] = "drop"
    return(dict_trend)

#kendall test
#(...)