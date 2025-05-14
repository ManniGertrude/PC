import matplotlib.pyplot as plt
import scipy.odr as odr
import numpy as np
import pandas as pd
import scipy.stats as st
from sklearn.metrics import r2_score
from matplotlib.ticker import MultipleLocator
import os


global ax, fig
fig, ax = plt.subplots()
fig.set_size_inches(6, 4)
path = os.path.dirname(os.path.abspath(__file__))
CTable = ['deeppink', 'purple', 'indigo', 'blue', 'cornflowerblue', 'cadetblue', 'lightseagreen', 'seagreen', 'darkorange', 'coral', 'crimson' ]


#Einlesen der Daten und Definition der Gruppen und Stoffe
Data = pd.read_table(f'{path}\\Daten\\Wasser_SS_25.csv', sep=",", header=0, index_col=0)
# Data_ideal = pd.read_table(f'{path}\\Daten\\Ideal_SS_25.csv', sep=",", header=0, index_col=0)
Gruppen = ['A1', 'A2', 'A3', 'A4', 'A5','A6', 'A7', 'B1', 'B2', 'B3', 'B4', 'B5','B6']
Stoffe = ['Benzoe', 'Salicyl']


# Definition der Ausgleichsfunktion
def lin(Para, x):
    return Para[0]*x + Para[1]


# Konfidenzintervall 95%
def ConfidenceInterval(x, out, alpha=0.95):
    n = len(x)
    p = len(out.beta)
    dof = max(0, n - p)
    tval = st.t.ppf(1.0 - alpha / 2., dof)
    ci = []
    for i in range(p):
        ci.append([out.beta[i] - tval * out.sd_beta[i], out.beta[i] + tval * out.sd_beta[i]])
    return np.array(ci)


# Ersetzen von . durch , für die Ausgabe
def Replacer(Text):
    Text = Text.replace('.', ',')
    return Text


# ODR-Regression 
def Fit(x,y,sx,sy):
    model = odr.Model(lin)
    mydata = odr.RealData(x, y, sx=sx, sy=sy)
    myodr = odr.ODR(mydata, model, beta0=[-4000, 5], maxit=1000)
    out = myodr.run()
    return out
    

# Plot der Auswertung samt Konfidenzintervall und Regression
def FitPlot(Rez_T, ln_x_B, Rez_T_Error, ln_x_B_Error, H_mLinf, H_mLinf_Error, Mischenthalpie, Mischenthalpie_Error, Gruppe, Stoff, out, plot=True):
    if plot == True:
        ax.errorbar(Rez_T, ln_x_B, xerr=Rez_T_Error, yerr=ln_x_B_Error, color='navy', capsize=1, linestyle='none', label='Messwerte')
    # Konfidenzintervalle berechnen
    xValues = np.linspace(min(Rez_T), max(Rez_T), len(Rez_T))
    ci = ConfidenceInterval(xValues, out)
    ci_lower = lin(ci[:, 0], xValues)
    ci_upper = lin(ci[:, 1], xValues)
    ax.fill_between(xValues, ci_lower, ci_upper, color='lightblue', alpha=0.3, label='95% Konfidenzintervall')
    ax.plot(xValues, ci_lower, color='navy', alpha=0.2)
    ax.plot(xValues, ci_upper, color='navy', alpha=0.2)
    # Fit-Funktion plotten
    fy = lin(out.beta, xValues)
    ax.plot(xValues, fy, c='crimson',label = Replacer(f'({out.beta[0]:.0f}$\pm${out.sd_beta[0]:.0f}$) \cdot T^-$$^1 + $({out.beta[1]:.2f}$\pm${out.sd_beta[1]:.2f}) mit $R^2 =${r2_score(ln_x_B, lin(out.beta, Rez_T)):.3f}'))
    # Reihenfolge der Legende ändern
    handles, labels = ax.get_legend_handles_labels() 
    handles = handles[2:] + handles[:2]
    labels = labels[2:] + labels[:2]
    # Plot Parameter
    plt.xlim(min(Rez_T)-0.000005, max(Rez_T)+0.000005)
    plt.ylim(min(ln_x_B)-0.05, max(ln_x_B)+0.05)
    ax.set(xlabel='Reziproke Temperatur / $ K^{-1}$', ylabel='Stoffmengen-Logarithmus')
    fig.suptitle(Replacer(f'1. mol. Lösungsenthalpie $\Delta_LH_B^\infty$ = ({H_mLinf:.0f} $\pm$ {H_mLinf_Error:.0f}) J/mol'), fontsize=12)
    ax.set_title(Replacer(f'Mischenthalpie $\Delta_MH_B =$ ({Mischenthalpie:.0f} $\pm$ {Mischenthalpie_Error:.0f}) J/mol'))
    ax.legend(handles, labels, loc='lower left', framealpha=0.2, fontsize=8.5)
    ax.grid()
    ax.xaxis.set_major_locator(MultipleLocator(0.00005))
    ax.xaxis.set_minor_locator(MultipleLocator(0.00001))
    fig.savefig(f'{path}\\PNG\\WS2425 Wasser\\Wasser {Gruppe} {Stoff}.png', dpi=300)
    plt.cla()


# Auswertung der wässrigen Lösungen 
def Auswertung(Gruppe, Stoff, Print=True):
    C = 0.1                                                             # Molarität M = mol/L
    C_Error = 0.005*C                                                   # M
    T_Data = Data.loc[f'T({Gruppe}_{Stoff[:1]})'].dropna().values+273.15         # K
    V_Data = Data.loc[f'V({Gruppe}_{Stoff[:1]})'].dropna().values                # mL
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
    out = Fit(Rez_T, ln_x_B, Rez_T_Error, ln_x_B_Error)
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
    FitPlot(Rez_T, ln_x_B, Rez_T_Error, ln_x_B_Error, H_mLinf, H_mLinf_Error, Mischenthalpie, Mischenthalpie_Error, Gruppe, Stoff, out)
    if Print == True:
        print()
        print(f'Gruppe: {Gruppe}, Stoff: {Stoff}')
        print(f'Die Lösungsenthalpie beträgt: ({H_mLinf:.0f} \pm {H_mLinf_Error:.0f}) J/mol')
        print(f'Die Mischenthalpie beträgt: ({Mischenthalpie:.0f} \pm {Mischenthalpie_Error:.0f}) J/mol')
        print(f'Die ideale Löslichkeit beträgt: ')
        for i in range(len(x_B_id)):
            print(f'({x_B_id[i]:.4f} \pm {x_B_id_Error[i]:.4f}) bei ({T_Data[i]:.2f} \pm {T_Error[i]:.2f}) K')
        print()
    
    return [Rez_T, ln_x_B, Rez_T_Error, ln_x_B_Error, H_mLinf, H_mLinf_Error, Mischenthalpie, Mischenthalpie_Error, Gruppe]



# Ideale Löslichkeit für eine Gruppe 
def Ideal(Gruppe, Print=True):
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
        if Print==True:
            print()
            print(f'Organisches Lösungsmittel der Gruppe {Gruppe}')
            print(f'Die Ideale Löslichkeit beträgt: {x_B_lit:.4g} \pm {x_B_lit_Error:.2g}')
            print(f'Die exp. Löslichkeit beträgt:   {x_B:.4g} \pm {x_B_lit:.2g}')
            print(f'Die Abweichung des exp. Werts vom Literaturwert beträgt ({100*Abweichung_ideal:.1f} \pm {100*Abweichung_Ideal_Error:.1f})%')
            print()


# Abfrage für alle Gruppen
def AlleAbfragen(Print = True):
    Salicyl = []
    Benzoe = []
    for i in Gruppen:
        for j in Stoffe:
            if f'T({i}_{j[:1]})' in Data.index:
                Output = Auswertung(i, j, Print)
                if j == 'Salicyl':
                    Salicyl.append(Output)
                elif j == 'Benzoe':
                    Benzoe.append(Output)
        Ideal(i, Print)
    # Plot für alle Messwerte, Wasser
    Name = ['Salicyl', 'Benzoe']
    for j in range(2):
        if j == 0:
            Stoff = Salicyl
        elif j == 1:
            Stoff = Benzoe
        for i in range(len(Stoff)):
            plt.errorbar(Stoff[i][0], Stoff[i][1], xerr=Stoff[i][2], yerr=Stoff[i][3], capsize=1.5, linestyle='none', label=f'{Stoff[i][8]}', color=CTable[i])
        ln_x_B = np.concatenate([Stoff[i][1] for i in range(len(Stoff))])
        ln_x_B_Error = np.concatenate([Stoff[i][3] for i in range(len(Stoff))])
        Rez_T = np.concatenate([Stoff[i][0] for i in range(len(Stoff))])
        Rez_T_Error = np.concatenate([Stoff[i][2] for i in range(len(Stoff))])
        out = Fit(Rez_T, ln_x_B, Rez_T_Error, ln_x_B_Error)
        H_mLinf = -out.beta[0]*8.314
        H_mLinf_Error = out.sd_beta[0]*8.314
        if j == 0:
            Mischenthalpie = H_mLinf - 14500
        elif j == 1:
            Mischenthalpie = H_mLinf - 13800
        Mischenthalpie_Error = H_mLinf_Error
        FitPlot(Rez_T, ln_x_B, Rez_T_Error, ln_x_B_Error, H_mLinf, H_mLinf_Error, Mischenthalpie, Mischenthalpie_Error, 'Zusammen', Name[j], out, False)
        
    

# Abfrage für eine Gruppe, Wasser
def EineAbfrage(Gruppe, Stoff, Print):
    if f'T({Gruppe}_{Stoff[:1]})' in Data.index:
        Auswertung(Gruppe, Stoff, Print)
    else:
        print(f'Keine Daten für Gruppe {Gruppe} und Stoff {Stoff} vorhanden')
        print()


# Abfrage für eine Gruppe für beide Stoffe und die ideale Lösung
def EineGruppe(Gruppe, Print):
    for i in Stoffe:
        EineAbfrage(Gruppe, i, Print)
    Ideal(Gruppe, Print)





# # Mögliche Auswertmethoden:

EineAbfrage('A5', 'Benzoe', True) # Einzelne Gruppe und einzelner Stoff
# EineGruppe('A1') # Eine Gruppe und beide Stoffe sowie die ideale Lösung
# Ideal('A1') # Ideale Lösung für eine Gruppe

# AlleAbfragen()  # Alle Gruppen und Stoffe. Optional Print=True/False für Ausgabe der Ergebnisse

