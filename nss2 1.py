import datetime
import pandas as pd 
from sqlalchemy import create_engine
import pyodbc
import os
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import time
from dur_yield import * 


result = find_dur_and_yield()


def nelson_siegel(tau, beta0, beta1, beta2, beta3, tau1, tau2):
    """
    Nelson-Siegel-Svensson yield curve model.

    Parameters:
    - tau: Time to maturity (can be a scalar or an array)
    - beta0, beta1, beta2, tau1, tau2: Model parameters

    Returns:
    - Yield curve values corresponding to the given parameters and time to maturity
    """
    return beta0 + beta1 * ((1 - np.exp(-tau / tau1)) / (tau / tau1)) + beta2 * ((1 - np.exp(-tau / tau1)) / (tau / tau1) - np.exp(-tau / tau1)) + beta3 * ((1 - np.exp(-tau / tau2)) / (tau / tau2)-np.exp(-tau/tau2))

def nelson_siegel_residuals(params, tau, observed_yields, regularization_strength=0.01):
    beta0, beta1, beta2, beta3, tau1, tau2 = params
    predicted_yields = nelson_siegel(tau, beta0, beta1, beta2, beta3, tau1, tau2)
    residuals = predicted_yields - observed_yields
    regularization_term = regularization_strength * np.sum(params**2)  # L2 regularization term
    return np.sum(residuals**2) + regularization_term


def fit_nelson_siegel(tau, observed_yields, regularization_strength, initial_guess=None, inequality_constraints=None):
    if initial_guess is None:
        initial_guess = [0.02, 0.02, 0.02, 2.0, 2.0]

    result = minimize(nelson_siegel_residuals, initial_guess, args=(tau, observed_yields, regularization_strength), method =  'TNC', constraints = inequality_constraints)
    return result.x

def compute_rmse(tau, observed_yields, fitted_params, regularization_strength):
    predicted_yields = nelson_siegel(tau, *fitted_params)
    residuals = predicted_yields - observed_yields
    mse = np.mean(residuals**2)
    rmse = np.sqrt(mse)
    return rmse

def nss_main():
    now = datetime.now()

    dags = f'{now.day}-{now.month}-{now.year}'
    inequality_constraints = [{'type': 'ineq', 'fun': lambda x: x[1]},  # beta1 > 0
                          {'type': 'ineq', 'fun': lambda x: x[1] + x[2]}] # beta1 + beta2 > 0
    # Sample data
    conn_str = (r'DRIVER={SQL Server};'
    r'SERVER=dbdeli;'
    r'DATABASE=VBR;'
    r'Trusted_Connection=yes;'
    r'TrustServerCertificate=yes;')

    conn = pyodbc.connect(conn_str)

    engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(conn_str))

    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    for i in ['Verðtryggt', 'Óverðtryggt']:
        if i == 'Verðtryggt':
            query = "select R.Dagsetning as Dagsetning, Gildi1 as Krafa, liftimi as dur, audkenni as Tikker, Lokadagur as Gjalddagur from dbo.Runur R join Flokkur F on F.flokkurid = R.FlokkurId where R.Dagsetning >= dateadd(month, -1.5, getdate()) and f.audkenni LIKE '%RIKS%'  and f.heiti NOT LIKE '%Vísitala%' and VirkurOvirkur = 'V' order by Dagsetning, dur"
            dic = {}
            for key in result.keys(): 
                if key in ["RIKS 26 0216", "RIKS 30 0701", "RIKS 33 0321", "RIKS 37 0115"]:
                    if key not in dic.keys():
                        dic[key] = {}
                    dic[key]['dur'] = result[key][0]
                    dic[key]['Krafa'] = result[key][1]
            data2 = pd.DataFrame.from_dict(dic)
            data2 = data2.T
        else:
            query = "select R.Dagsetning as Dagsetning, Gildi1 as Krafa, liftimi as dur, audkenni as Tikker, Lokadagur as Gjalddagur from dbo.Runur R join Flokkur F on F.flokkurid = R.FlokkurId where R.Dagsetning >= dateadd(month, -1.5, getdate()) and f.audkenni LIKE '%RIKB%' and f.heiti NOT LIKE '%Vísitala%' and VirkurOvirkur = 'V' order by Dagsetning, dur"
            dic = {}
            for key in result.keys(): 
                if key in ["RIKB 24 0415", "RIKB 25 0612", "RIKB 26 1015", "RIKB 28 1115", "RIKB 31 0124", "RIKB 42 0217"]:
                    if key not in dic.keys():
                        dic[key] = {}
                    dic[key]['dur'] = result[key][0]
                    dic[key]['Krafa'] = result[key][1]
            data2 = pd.DataFrame.from_dict(dic)
            data2 = data2.T

        data = pd.read_sql(query, cnxn)

        taul = data['dur'].values 
        yields = data['Krafa'].values
        x_values_data2 = data2['dur'].values
        y_values_data2 = data2['Krafa'].values

        tau = np.array(taul)
        observed_yields = np.array(yields)
        opti = []
        regularization_strengths = np.linspace(0.0, 1.0, 100)
        rmse_values = []

        longtermrate = yields[-1]/100
        if i != 'Verðtryggt':
            print(y_values_data2)
            b1 = y_values_data2[-1]/100-y_values_data2[0]/100
            print(b1)
            b2 = -y_values_data2[0]/100+2*((y_values_data2[-3]+y_values_data2[-2])/2/100)-y_values_data2[-1]/100
            b3 = y_values_data2[-1]/100 - ((y_values_data2[-3]+y_values_data2[-2])/2)/100
            lambda1 = data2['dur'][-1]
            lambda2 = data2['dur'][-2]
        else:
            print(y_values_data2)
            b1 = y_values_data2[-1]/100-y_values_data2[0]/100
            print(b1)
            b2 = -y_values_data2[0]/100+2*y_values_data2[1]/100-y_values_data2[-1]/100
            b3 = y_values_data2[-1]/100 - y_values_data2[-3]/100
            lambda1 = data2['dur'][-1]
            lambda2 = (data2['dur'][-2]+data2['dur'][-3])/2
        
        
        initial = [longtermrate, b1, b2, b3, lambda2, lambda1]
        print(initial)
        for reg in regularization_strengths:
            fitted_params = fit_nelson_siegel(tau, observed_yields, reg, initial)
            rmse = compute_rmse(tau, observed_yields, fitted_params, reg)
            rmse_values.append(rmse)

        min_rmse_index = np.argmin(rmse_values)
        best_regularization = regularization_strengths[min_rmse_index]
        best_rmse = rmse_values[min_rmse_index]
        fitted_params = fit_nelson_siegel(tau, observed_yields, 0, initial, inequality_constraints)
        x_values_data2 = data2['dur'].values
        y_values_data2 = data2['Krafa'].values
        fitted_params = [fitted_params[0], fitted_params[1], fitted_params[2], fitted_params[3], fitted_params[4] , fitted_params[5]]  # Replace with your fitted parameters
        tau_plot = np.linspace(0, 15, 100, endpoint = True)  # Time to maturity from 0.1 to 15 years
        # Calculate yield curve using the fitted parameters
        yield_curve = nelson_siegel(tau_plot, *fitted_params)
        x_values_to_mark = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        # Calculate the corresponding y-values on the yield_curve for these x-values
        y_values_to_mark = nelson_siegel(x_values_to_mark, *fitted_params)
        #Reikna núverandi yield kúrfu
        fitted_params2 = fit_nelson_siegel(x_values_data2, y_values_data2, 0, initial, inequality_constraints) 
        fitted_params2 = [fitted_params2[0], fitted_params2[1], fitted_params2[2], fitted_params2[3], fitted_params2[4], fitted_params[5]] 
        print(fitted_params)
        print(fitted_params2)
        yield_curve2 = nelson_siegel(tau_plot, *fitted_params2)


        # plt.plot(tau_plot, yield_curve, label=f'Nálgun á kúrfu - síðasti mánuður')
        # plt.plot(tau_plot, yield_curve2, label=f'Kúrfa í dag')
        # plt.scatter(x_values_data2, y_values_data2, color='red', marker='x', label='Nýjustu kröfur')
        # # Plot red data points (markers) at the specified x, y coordinates

        # # Add data labels (annotations) to specific x, y values
        # for x, y in zip(x_values_data2, y_values_data2):
        #     plt.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
        # for x, y in zip(x_values_to_mark, y_values_to_mark):
        #     plt.annotate(f'{y:.2f}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')
        


        # # Add data labels (annotations) to specific x values
        # for i, txt in enumerate(y_values_to_mark):
        #     plt.annotate(f'{txt:.2f}', (x_values_to_mark[i], y_values_to_mark[i]), textcoords="offset points", xytext=(0,10), ha='center')  
        
        # # Plot the yield curve
        # plt.xlabel('Duration (years)')
        # plt.ylabel('Ávöxtunarkrafa')
        # plt.title(f'Nelson-Siegel-Svensson Yield Curve ')
        # plt.legend()
        # plt.grid(True)
        # plt.show()
        if i == 'Verðtryggt':
            riks = {}
            riks['Í dag'] = [tau_plot, yield_curve2]
            riks['Síðasti mánuður'] = [tau_plot, yield_curve]
        else:
            data = {}
            data['RIKB'] =  {'x': tau_plot, 'y': yield_curve2}
            # rikb['Síðasti mánuður'] = [tau_plot, yield_curve]
    return data
            

# Útskýring: Skilar dictionary fyrir báða ferla, þar inni eru array, fyrsti array eru x gildi, hinn er y gildi (kröfur)