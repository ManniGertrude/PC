import matplotlib.pyplot as plt
import scipy.odr as odr
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score


fig, ax = plt.subplots()
path = "C:\\Users\\kontr\\Desktop\\Github\\PC"  # PC
# path = 'C:\\Users\\Surface Pro 7 Manni\\Desktop\\Code Dateien\\P5\\525\\Messungen\\csv' # Surface


Data = pd.read_csv(f'{path}\\Daten\\Wasser_WS_24-25.csv', sep=",", header=0).astype(np.float64)
Gruppen = ['A1']
Stoffe = ['Benzoe', 'Salicyl']
C_Error = 0.01

def lin(Para, x):
    return Para[0]*x + Para[1]

def Auswertung(Gruppe, Stoff):
    T_Data = np.array(Data[f'T({Gruppe}_{Stoff[:1]})'].values)+273.15
    V_Data = np.array(Data[f'V({Gruppe}_{Stoff[:1]})'].values)
    T_Error = np.array([0.2]*len(T_Data))
    V_Error = np.array([0.2]*len(V_Data))
    n_B = 1e-4*V_Data
    n_B_Error = np.sqrt((1e-3*V_Data*C_Error)**2+(1e-4*V_Error)**2)
    n_A = 1.387
    x_B = n_B/(n_A - n_B)
    x_B_Error = n_A*n_B_Error/(n_A - n_B)**2
    ln_x_B = np.log(x_B)
    ln_x_B_Error = abs(x_B_Error/x_B)
    Rez_T = 1/T_Data
    Rez_T_Error = T_Error/T_Data**2
    
    
    model = odr.Model(lin)
    mydata = odr.RealData(Rez_T, ln_x_B, sx=Rez_T_Error, sy=ln_x_B_Error)
    myodr = odr.ODR(mydata, model, beta0=[-4000, 5], maxit=1000)
    out = myodr.run()
    fy = lin(out.beta, Rez_T)
    rsquared = r2_score(ln_x_B, fy)
    ax.plot(Rez_T, fy, c='red',label = f'({out.beta[0]:.0f}$\pm${out.sd_beta[0]:.0f}$) \cdot T^-$$^1 + ${out.beta[1]:.1f}$\pm${out.sd_beta[1]:.1f} mit $R^2 =${rsquared:.3f}' )
    H_mLinf = -out.beta[0]*8.314
    if Stoff == 'Salicyl':
        AbweichungReal = (H_mLinf - 14500)/14500
    elif Stoff == 'Benzoe':
        AbweichungReal = (H_mLinf - 13800)/13800
    
        
    ax.errorbar(Rez_T, ln_x_B, xerr=Rez_T_Error, yerr=ln_x_B_Error, color='navy', capsize=3, linestyle='none', label='Messwerte')
    ax.set(xlabel='Reziproke Temperatur $^\circ C^{-1}$', ylabel='Stoffmengen-Logarithmus')
    ax.set_title(f'Bestimmung der Lösungsenthalpie $H_m^\infty$ = {H_mLinf:.0f} J/mol K')
    ax.legend()
    ax.grid()
    ax.set_xticks(np.linspace(0.0031, 0.0033, 5))
    ax.set_xticks(np.linspace(0.0031, 0.0033, 21), minor=True)
    fig.savefig(f'{path}\\PNG\\WS2425\\Wasser {Gruppe} {Stoff}.png')
    fig.savefig(f'{path}\\PDF\\WS2425\\Wasser {Gruppe} {Stoff}.pdf')
    fig.show()
    plt.cla()
    print(f'Abweichung Real: {100*AbweichungReal:.2f}%')
    
    
    
    
    
    

    
for i in Gruppen:
    for j in Stoffe:
        
        Auswertung(i, j)