import matplotlib.pyplot as plt
import scipy.odr as odr
import numpy as np
import pandas as pd
import statistics as st
from sklearn.metrics import r2_score


fig, ax = plt.subplots()
path = "C:\\Users\\kontr\\Desktop\\Github\\PC"  # PC
# path = 'C:\\Users\\Surface Pro 7 Manni\\Desktop\\Code Dateien\\P5\\525\\Messungen\\csv' # Surface

Data_WB = pd.read_csv(f'{path}\\Daten\\Wasser-Benzoe_WS_24-25.csv', sep=",", header=0).astype(np.float64)
Data_WS = pd.read_csv(f'{path}\\Daten\\Wasser-Salicyl_WS_24-25.csv', sep=",", header=0).astype(np.float64)

def lin(Para, x):
    return Para[0]*x + Para[1]

def Auswertung(Data, Gruppe):
    TData = np.array(Data[f'T({Gruppe})'].values)
    VData = np.array(Data[f'V({Gruppe})'].values)
    n_B = 1e-4*VData
    n_A = 1.387
    x_B = n_B/(n_A - n_B)
    ln_x_B = np.log(x_B)
    Rez_T = 1/(TData+273.15)
    
    
    model = odr.Model(lin)
    mydata = odr.RealData(Rez_T, ln_x_B)
    myodr = odr.ODR(mydata, model, beta0=[-4000, 5], maxit=1000)
    out = myodr.run()
    fy = lin(out.beta, Rez_T)
    rsquared = r2_score(ln_x_B, fy)
    ax.plot(Rez_T, fy, c='red',label = f'({out.beta[0]:.0f}$\pm${out.sd_beta[0]:.0f}$) \cdot T^-$$^1 + ${out.beta[1]:.1f}$\pm${out.sd_beta[1]:.1f} mit $R^2 =${rsquared:.3f}' )
    H_mLinf = -out.beta[0]*8.314
    
    ax.scatter(Rez_T, ln_x_B, marker='x', c='navy', label = 'Messwerte')
    ax.set(xlabel='Reziproke Temperatur $^\circ C^{-1}$', ylabel='Stoffmengen-Logarithmus')
    ax.set_title(f'Bestimmung der Lösungsenthalpie $H_m^\infty$ = {H_mLinf:.0f} J/mol K')
    ax.legend()
    ax.grid()
    ax.set_xticks(np.linspace(0.0031, 0.0033, 5))
    ax.set_xticks(np.linspace(0.0031, 0.0033, 21), minor=True)
    fig.savefig(f'{path}\\PNG\\WS2425\\Wasser {Gruppe}.png')
    fig.savefig(f'{path}\\PDF\\WS2425\\Wasser {Gruppe}.pdf')
    fig.show()
    plt.cla()
    
    
    
    
    
    
    

    
    
Auswertung(Data_WB, 'AX')