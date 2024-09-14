import matplotlib.pyplot as plt
import scipy.odr as odr
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline
import statistics as st

path = "C:\\Users\\kontr\\Desktop\\Github\\PC"  # PC
# path = 'C:\\Users\\Surface Pro 7 Manni\\Desktop\\Code Dateien\\P5\\525\\Messungen\\csv' # Surface

Anteil = [0.122, 0.199, 0.290, 0.430, 0.500, 0.600, 0.700, 0.800, 0.900, 0.000, 0.122, 0.199, 0.290, 0.430, 0.500, 0.600, 0.700, 0.800, 0.900, 1.000]
Anteile = ['E122', 'E199', 'E290', 'E430', 'E500', 'E600', 'E700', 'E800', 'E900', 'L000', 'L122', 'L199', 'L290', 'L430', 'L500', 'L600', 'L700', 'L800', 'L900', 'E1000']

Dateien = ['Mikroskop_WS_22-23', 'Mikroskop_SS_23', 'Mikroskop_WS_23-24', 'Mikroskop_SS_24']# , 'Mikroskop_WS_24-25'
Bezeichnung = ['WS 22-23', 'SS 23', 'WS 23-24', 'SS 24']# , 'WS 24-25'
colortable = ['sienna', 'darkgoldenrod', 'darkolivegreen', 'steelblue', 'darkmagenta']

WS2223 = np.zeros(len(Anteile))
SS23 = np.zeros(len(Anteile))
WS2324 = np.zeros(len(Anteile))
SS24 = np.zeros(len(Anteile))
WS2425 = np.zeros(len(Anteile))
Mittelwertliste = np.array([WS2223, SS23, WS2324, SS24])# , WS2425
Sigma = np.array([WS2223, SS23, WS2324, SS24])# , WS2425 

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
    ax.savefig(f'{path}\\PNG\\{Name}.png')
    ax.savefig(f'{path}\\PDF\\{Name}.pdf')
    ax.show()
    plt.cla()

def lin(Para, x): 
    return Para[0] + x*Para[1] - x*Para[1]

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
for i in range(len(Dateien)):
    Data = pd.read_csv(f'{path}\\Daten\\{Dateien[i]}.csv', sep=",",header=0, names=Anteile)
    temp = 0
    for j in Anteile:
        Mittelwert = st.mean(Data[j])
        SigmaTemp = 0
        for k in Data[j]:
            SigmaTemp = SigmaTemp + (k-Mittelwert)**2
        Sigma[i][temp] = np.sqrt(SigmaTemp/len(Data[j]))
        Mittelwertliste[i][temp] = Mittelwert
        temp += 1
    Menge.append(len(Data[j]))
    fit(lin, Anteil[:9], Mittelwertliste[i][:9], Dateien[i][10:], Sigma[i][:9], colortable[i], True)
    plt.errorbar(Anteil, Mittelwertliste[i], xerr=0.01, yerr=Sigma[i], color = colortable[i], capsize=3, linestyle='none')
    Plotparams(Dateien[i], f'{len(Data[j])} Messungen {Bezeichnung[i]}') # Dateien[i]

# Alle Semester in einen Plot übereinander gelegt
for i in range(len(Dateien)):
    fit(lin, Anteil[:9], Mittelwertliste[i][:9], None, Sigma[i][:9], colortable[i], False)
    plt.errorbar(Anteil, Mittelwertliste[i], xerr=0.01, yerr=Sigma[i], color=colortable[i], capsize=3, linestyle='none', label=Bezeichnung[i])
    X_Y_Spline = make_interp_spline(Anteil[9:], Mittelwertliste[i][9:])
    Y_ = X_Y_Spline(xWerte)
    plt.plot(xWerte, Y_, color=colortable[i], alpha=0.8)
Plotparams('Alle', f'{sum(Menge)} Messungen von {Bezeichnung[0]} bis {Bezeichnung[-1]}')

# Alle Werte in zusammengefasst in einem Plot
Gesamtdurchschnitt = np.zeros(len(Anteile))
Gesamtsigma = np.zeros(len(Anteile))
for i in range(len(Mittelwertliste)):
    Gesamtdurchschnitt = Gesamtdurchschnitt + Mittelwertliste[i]*(Menge[i]/sum(Menge))
    Gesamtsigma = Gesamtsigma + Sigma[i]*(Menge[i]/sum(Menge))
plt.errorbar(Anteil, Gesamtdurchschnitt, xerr=0.01, yerr=Gesamtsigma[i], color='black', capsize=3, linestyle='none', label=None)
fit(lin, Anteil[:9], Gesamtdurchschnitt[:9], None, Gesamtsigma[:9], 'black', True)
Plotparams('Gesamt', f'{sum(Menge)} Messungen von {Bezeichnung[0]} bis {Bezeichnung[-1]}')

# Datenüberprüfung einer einzelnen Messung
Zieldata = pd.read_csv(f'{path}\\Daten\\{Dateien[3]}.csv', sep=",",header=0, names=Anteile)
Zieldata = Zieldata.iloc[-1].values
plt.errorbar(Anteil[10:], Zieldata[10:], xerr=0.01, yerr=1, color='navy', capsize=3, linestyle='none', label='Liquidus')
plt.errorbar(Anteil[:9], Zieldata[:9], xerr=0.01, yerr=1, color='red', capsize=3, linestyle='none', label='Eutektikale')
fit(lin, Anteil[:9], Zieldata[:9], None, [1]*11, 'purple', True)


Plotparams('WS2425\\Mikroskop AX', 'Daten der Gruppe AX')