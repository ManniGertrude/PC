import matplotlib.pyplot as plt
import scipy.odr as odr
import numpy as np
import pandas as pd
import math
from sklearn.metrics import r2_score


fig, ax = plt.subplots()
# path = "C:\\Users\\kontr\\Desktop\\Github\\PC"  # PC
path = 'C:\\Users\\Surface Pro 7 Manni\\Desktop\\Code Dateien\\PC' # Surface

#Einlesen der Daten und Definition der Gruppen und Stoffe
Data = pd.read_csv(f'{path}\\Daten\\Wasser_WS_24-25.csv', sep=",", header=0).astype(np.float64)
Data_ideal = pd.read_table(f'{path}\\Daten\\Ideal_WS_24-25.csv', sep=",", header=0, index_col=0)
Gruppen = ['A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5']
Stoffe = ['Benzoe', 'Salicyl']

# Definition der Ausgleichsfunktion
def lin(Para, x):
    return Para[0]*x + Para[1]

# Ausrechnung der wässrigen Lösungen 
def Auswertung(Gruppe, Stoff):
    C = 0.1                                                           # Molarität M = mol/L
    C_Error = 0.03*C                                                # M
    T_Data = np.array(Data[f'T({Gruppe}_{Stoff[:1]})'].values)+273.15   # K
    V_Data = np.array(Data[f'V({Gruppe}_{Stoff[:1]})'].values)          # mL
    T_Error = np.array([0.2]*len(T_Data))                               # K     (geraten)*
    V_Error = np.array([0.1]*len(V_Data))                               # mL    (gemessen)
    n_B = 1e-4*V_Data                                                   # mol
    n_B_Error = np.sqrt((1e-3*V_Data*C_Error)**2+(1e-3*V_Error*C)**2)   # mol
    n_A = 1.387                                                         # mol
    x_B = n_B/(n_A - n_B)                                               # Einheitenlos
    x_B_Error = n_A*n_B_Error/(n_A - n_B)**2                            # Einheitenlos
    ln_x_B = np.log(x_B)                                                # Einheitenlos
    ln_x_B_Error = abs(x_B_Error/x_B)                                   # Einheitenlos
    Rez_T = 1/T_Data                                                    # 1/T
    Rez_T_Error = T_Error/T_Data**2                                     # 1/T
    
    # Regression
    model = odr.Model(lin)
    mydata = odr.RealData(Rez_T, ln_x_B, sx=Rez_T_Error, sy=ln_x_B_Error)
    myodr = odr.ODR(mydata, model, beta0=[-4000, 5], maxit=1000)
    out = myodr.run()
    fy = lin(out.beta, Rez_T)
    rsquared = r2_score(ln_x_B, fy)
    
    # Lösungsenthalpie
    H_mLinf = -out.beta[0]*8.314                                        # J
    H_mLinf_Error = out.sd_beta[0]*8.314                                # J
    if Stoff == 'Salicyl':
        # Mischenthalpie
        Mischenthalpie = H_mLinf - 14500
        Mischenthalpie_Error = H_mLinf_Error
        # Abweichung Mischenthalpie zu Schmelzenthalpie
        AbweichungReal = (H_mLinf - 14500)/14500
        AbweichungReal_Error = H_mLinf_Error/14500
        # Ideale Löslichkeit
        x_B_id = np.exp(-27100/8.31446*(1/(T_Data)-1/431.4))
        x_B_id_Error = abs(x_B_id*27100*T_Error/(8.31446*(T_Data)**2))
    elif Stoff == 'Benzoe':
        # Mischenthalpie
        Mischenthalpie = H_mLinf - 13800
        Mischenthalpie_Error = H_mLinf_Error
        # Ideale Löslichkeit
        x_B_id = np.exp(-18000/8.31446*(1/(T_Data)-1/395.5))
        x_B_id_Error = abs(x_B_id*18000*T_Error/(8.31446*(T_Data)**2))
        

    
    print(f'Gruppe: {Gruppe}, Stoff: {Stoff}')
    print(f'Die Lösungsenthalpie beträgt: ({H_mLinf:.0f} \pm {H_mLinf_Error:.0f}) J/mol')
    print(f'Die Mischenthalpie beträgt: ({Mischenthalpie:.0f} \pm {Mischenthalpie_Error:.0f}) J/mol')
    print(f'Die ideale Löslichkeit beträgt: ')
    for i in range(len(x_B_id)):
        print(f'({x_B_id[i]:.4f} \pm {x_B_id_Error[i]:.4f}) bei ({T_Data[i]:.2f} \pm {T_Error[i]:.2f}) K')
    print()

    # Plot
    ax.plot(Rez_T, fy, c='red',label = f'({out.beta[0]:.0f}$\pm${out.sd_beta[0]:.0f}$) \cdot T^-$$^1 + ${out.beta[1]:.1f}$\pm${out.sd_beta[1]:.1f} mit $R^2 =${rsquared:.3f}' )     
    ax.errorbar(Rez_T, ln_x_B, xerr=Rez_T_Error, yerr=ln_x_B_Error, color='navy', capsize=3, linestyle='none', label='Messwerte')
    ax.set(xlabel='Reziproke Temperatur $^\circ C^{-1}$', ylabel='Stoffmengen-Logarithmus')
    fig.suptitle(f'Bestimmung der 1. mol. Lösungsenthalpie $\Delta_LH_B^\infty$ = {H_mLinf:.0f} J/mol', fontsize=12)
    ax.legend()
    ax.grid()
    ax.set_xticks(np.linspace(0.0031, 0.0033, 5))
    ax.set_xticks(np.linspace(0.0031, 0.0033, 21), minor=True)
    fig.savefig(f'{path}\\PNG\\WS2425 Wasser\\Wasser {Gruppe} {Stoff}.png')
    fig.show()
    plt.cla()


# Abfrage für alle Gruppen, Wasser
def AlleAbfragen():
    for i in Gruppen:
        for j in Stoffe:
            if f'T({i}_{j[:1]})' in Data:
                if math.isnan(Data[f'T({i}_{j[:1]})'].values[0]):
                    quit
                else:
                    Auswertung(i, j)

# Abfrage für eine Gruppe, Wasser
def EineAbfrage(Gruppe, Stoff):
    if f'T({Gruppe}_{Stoff[:1]})' in Data:
        if math.isnan(Data[f'T({Gruppe}_{Stoff[:1]})'].values[0]):
            quit
        else:
            Auswertung(Gruppe, Stoff)

# Ideale Löslichkeit für eine Gruppe
def Ideal(Gruppe):
    if Gruppe in Data_ideal.index:
        IdealData = Data_ideal.loc[Gruppe].values
        T_ideal = IdealData[0] + 273.15     # K
        M_Tara = IdealData[1]               # g
        M_brutto = IdealData[2]             # g
        V_ideal = IdealData[3]*1e-3         # L
        C_ideal = 0.5                       # mol/L
        M_A = 56.29                         # g/mol
        M_B = 122.12                        # g/mol
        n_B = C_ideal * V_ideal             # Einheitenlos
        m_B = M_B*n_B                       # g
        m_A = M_brutto-M_Tara-m_B           # g
        b_B = n_B/m_A                       # mol/g
        n_A = m_A/M_A                       # mol
        x_B = n_B/(n_A + n_B)               # Einheitenlos
        x_B_lit = np.exp(-14750/8.31446*(1/(T_ideal)-1/395.5))
        Abweichung_ideal = (x_B - x_B_lit)/x_B_lit
    
        V_Error = 0.0002
        T_Error = 0.50
        C_Error = 0.05*C_ideal # <<<------ Sehr stark von diesem Fehler abhängig <- Überprüfen
        n_B_Error = np.sqrt((C_Error*V_ideal)**2 + (C_ideal * V_Error)**2)
        m_B_Error = M_B*n_B_Error
        M_brutto_Error = 0.01
        M_Tara_Error = 0.01
        m_A_Error = np.sqrt(M_brutto_Error**2 + M_Tara_Error**2 + m_B_Error**2)
        n_A_Error = m_A_Error/M_A
        x_B_Error = np.sqrt((n_A*n_B_Error/(n_A + n_B)**2)**2 + (n_A_Error*n_B/(n_B + n_A)**2)**2)
        x_B_lit_Error = abs(T_Error*14750/(T_ideal**2*8.3145) *np.exp(-14750/8.3145*(1/(T_ideal)-1/395.5)))
        Abweichung_Ideal_Error = np.sqrt((x_B_lit_Error/x_B)**2 + (x_B_Error *x_B_lit/x_B**2 )**2)
        print()
        print(f'Organisches Lösungsmittel der Gruppe {Gruppe}')
        print(f'Die Ideale Löslichkeit beträgt: {x_B_lit:.4g} \pm {x_B_lit_Error:.2g}')
        print(f'Die exp. Löslichkeit beträgt:   {x_B:.4g} \pm {x_B_lit:.2g}')
        print(f'Die Abweichung des exp. Werts vom Literaturwert beträgt ({100*Abweichung_ideal:.1f} \pm {100*Abweichung_Ideal_Error:.1f})%')
        print()



# AlleAbfragen()
EineAbfrage('A1', 'Salicyl'), 
Ideal('A1')
