import matplotlib.pyplot as plt
import scipy.odr as odr
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline
import statistics as st
import os

path = os.path.dirname(os.path.abspath(__file__))

# Anteile Acetanilid - Benzamid
Anteil = [0.122, 0.199, 0.290, 0.430, 0.500, 0.600, 0.700, 0.800, 0.900, 0.000, 0.122, 0.199, 0.290, 0.430, 0.500, 0.600, 0.700, 0.800, 0.900, 1.000]
Anteile = ['E122', 'E199', 'E290', 'E430', 'E500', 'E600', 'E700', 'E800', 'E900', 'L000', 'L122', 'L199', 'L290', 'L430', 'L500', 'L600', 'L700', 'L800', 'L900', 'L1000']
# Anteile Acetanilid - Benzil
Anteil2 = [0.067, 0.176, 0.301, 0.392, 0.491, 0.600, 0.660, 0.750, 0.851, 0.000, 0.067, 0.176, 0.301, 0.392, 0.491, 0.600, 0.660, 0.750, 0.851, 1.000]	
Anteile2 = ['E067', 'E176', 'E301', 'E392', 'E491', 'E600', 'E660', 'E750', 'E851', 'L000', 'L067', 'L176', 'L301', 'L392', 'L491', 'L600', 'L660', 'L750', 'L851', 'L1000']

# Daten einlesen
Dateien = ['Mikroskop_WS_22-23', 'Mikroskop_SS_23', 'Mikroskop_WS_23-24', 'Mikroskop_SS_24', 'Mikroskop_WS_24-25']
Bezeichnung = ['WS 22-23', 'SS 23', 'WS 23-24', 'SS 24', 'WS 24-25']
colortable = ['sienna', 'darkgoldenrod', 'darkolivegreen', 'steelblue', 'darkmagenta']

# Listen für die Werte
WS2223 = np.zeros(len(Anteile))
SS23 = np.zeros(len(Anteile))
WS2324 = np.zeros(len(Anteile))
SS24 = np.zeros(len(Anteile))
WS2425 = np.zeros(len(Anteile))
Mittelwertliste = np.array([WS2223, SS23, WS2324, SS24, WS2425])
Sigma = np.array([WS2223, SS23, WS2324, SS24, WS2425 ])

ax, plt = plt.subplots()
xWerte = np.linspace(0, 1, 100)
Menge = []


def Plotparams(Name, Titel):
    plt.set_ylim(68, 132)
    plt.set_xlim(-0.02, 1.02)
    plt.set(xlabel='Stoffkonzentration $x_B$', ylabel='Temperatur in$^\circ C$')
    plt.legend()
    plt.grid()
    plt.set_title(Titel)
    ax.savefig(f'{path}\\PNG\\Mikroskop\\{Name}.png')
    ax.show()
    plt.cla()

# Lineare Funktion
def lin(Para, x): 
    return Para[0] + x*Para[1] - x*Para[1]


# Fitfunktion
def fit(func, x, y, Name, yError, Farbe, labeln):
    model = odr.Model(func)
    mydata = odr.RealData(x, y, sx= 0.01, sy=yError)
    myodr = odr.ODR(mydata, model, beta0=[80.0, 0], maxit=1000)
    out = myodr.run()
    fy = func(out.beta, xWerte)
    if labeln == True:
        plt.plot(xWerte, fy, label = f'[{out.beta[0]:.1f}$\pm${np.sqrt(out.sd_beta[0]**2 + st.mean(yError)**2):.1f}]$^\circ C$', alpha=0.65, color=Farbe)
    else:
        plt.plot(xWerte, fy, label = Name, alpha=0.65, color=Farbe)
    return out


# Jedes Semester einzeln in einem Plot
def Jedes_semester_ein_plot():
    for i in range(len(Dateien)):
        if i < 4:
            SpezAnteil = Anteil
            SpezAnteile = Anteile
        else:
            SpezAnteil = Anteil2
            SpezAnteile = Anteile2
        Data = pd.read_csv(f'{path}\\Daten\\{Dateien[i]}.csv', sep=",",header=0, names=SpezAnteile)
        temp = 0
        for j in SpezAnteile:
            Mittelwert = st.mean(Data[j])
            SigmaTemp = 0
            for k in Data[j]:
                SigmaTemp = SigmaTemp + (k-Mittelwert)**2
            Sigma[i][temp] = np.sqrt(SigmaTemp/len(Data[j]))
            Mittelwertliste[i][temp] = Mittelwert
            temp += 1
        if i < 4:
            Menge.append(len(Data))
        fit(lin, SpezAnteil[:9], Mittelwertliste[i][:9], Dateien[i][10:], Sigma[i][:9], colortable[i], True)
        plt.errorbar(SpezAnteil, Mittelwertliste[i], xerr=0.01, yerr=Sigma[i], color = colortable[i], capsize=3, linestyle='none')
        Plotparams(Dateien[i], f'{len(Data[j])} Messungen {Bezeichnung[i]}')


# Semester 1-4 in einen Plot übereinander gelegt
def Benzamid_zusammengefasst_einzeln():
    for i in range(4):
        fit(lin, Anteil[:9], Mittelwertliste[i][:9], None, Sigma[i][:9], colortable[i], False)
        plt.errorbar(Anteil, Mittelwertliste[i], xerr=0.01, yerr=Sigma[i], color=colortable[i], capsize=3, linestyle='none', label=Bezeichnung[i])
        X_Y_Spline = make_interp_spline(Anteil[9:], Mittelwertliste[i][9:])
        Y_ = X_Y_Spline(xWerte)
        plt.plot(xWerte, Y_, color=colortable[i], alpha=0.8)
    Plotparams('Alle', f'{sum(Menge)} Messungen von {Bezeichnung[0]} bis {Bezeichnung[-1]}')


# Alle Werte Semester 1-4 in zusammengefasst in einem Plot
def Benzamid_zusammengefasst_zusammen():
    Gesamtdurchschnitt = np.zeros(len(Anteile))
    Gesamtsigma = np.zeros(len(Anteile))
    for i in range(4):
        Gesamtdurchschnitt = Gesamtdurchschnitt + Mittelwertliste[i]*(Menge[i]/sum(Menge))
        Gesamtsigma = Gesamtsigma + Sigma[i]*(Menge[i]/sum(Menge))
    plt.errorbar(Anteil, Gesamtdurchschnitt, xerr=0.01, yerr=Gesamtsigma[i], color='black', capsize=3, linestyle='none', label=None)
    fit(lin, Anteil[:9], Gesamtdurchschnitt[:9], None, Gesamtsigma[:9], 'black', True)
    Plotparams('Gesamt', f'{sum(Menge)} Messungen von {Bezeichnung[0]} bis {Bezeichnung[-1]}')

def JedeGruppeEinPlot():
    for i in range(len(Dateien)):
        Zieldata = pd.read_csv(f'{path}\\Daten\\{Dateien[i]}.csv', sep=",",header=0, names=Anteile)
        for index, row in Zieldata.iterrows():
            RowData = row.to_list()
            plt.errorbar(Anteil2[9:], RowData[9:], xerr=0.01, yerr=1, color='navy', capsize=3, linestyle='none', label='Liquidus')
            plt.errorbar(Anteil2[:9], RowData[:9], xerr=0.01, yerr=1, color='red', capsize=3, linestyle='none', label='Eutektikale')
            fit(lin, Anteil[:9], RowData[:9], None, [0.1]*9, 'purple', True)
            Plotparams(f'{Bezeichnung[i]}\\{index} Mikroskop', f'Daten der Gruppe {index}')


Jedes_semester_ein_plot()
# Benzamid_zusammengefasst_zusammen()
# Benzamid_zusammengefasst_einzeln()
JedeGruppeEinPlot()