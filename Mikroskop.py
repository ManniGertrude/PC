import matplotlib.pyplot as plt
import scipy.optimize as opt
import scipy.odr as odr
from scipy.optimize import curve_fit
from scipy.integrate import quad
import numpy as np
import os
import pandas as pd
from scipy.interpolate import make_interp_spline
from sklearn.metrics import r2_score
import os


ax, plt = plt.subplots()
path = "C:\\Users\\kontr\\Desktop\\Github\\PC"  # PC
# path = 'C:\\Users\\Surface Pro 7 Manni\\Desktop\\Code Dateien\\P5\\525\\Messungen\\csv' # Surface

Anteil = [0.122, 0.199, 0.290, 0.430, 0.500, 0.600, 0.700, 0.800, 0.900, 0.000, 0.122, 0.199, 0.290, 0.430, 0.500, 0.600, 0.700, 0.800, 0.900, 1.000]
Anteile = ['E122', 'E199', 'E290', 'E430', 'E500', 'E600', 'E700', 'E800', 'E900', 'L000', 'L122', 'L199', 'L290', 'L430', 'L500', 'L600', 'L700', 'L800', 'L900', 'E1000']

Dateien = ['Mikroskop_WS_22-23', 'Mikroskop_SS_23', 'Mikroskop_WS_23-24', 'Mikroskop_SS_24']# , 'Mikroskop_WS_24-25'
Bezeichnung = ['WS 22-23', 'SS 23', 'WS 23-24', 'SS 24']# , 'WS 24-25'
colortable = ['sienna', 'darkgoldenrod', 'darkolivegreen', 'steelblue', 'orchid']

WS2223 = np.zeros(len(Anteile))
SS23 = np.zeros(len(Anteile))
WS2324 = np.zeros(len(Anteile))
SS24 = np.zeros(len(Anteile))
WS2425 = np.zeros(len(Anteile))

xWerte = np.linspace(0, 1, 100)
Menge = []
Mittelwertliste = np.array([WS2223, SS23, WS2324, SS24]) # , WS2425
Sigma = np.array([WS2223, SS23, WS2324, SS24]) # , WS2425

def Plot(data, Name, yError, Farbe):
    plt.grid()
    plt.errorbar(Anteil, data, xerr=0.01, yerr=yError, color = Farbe, capsize=3, linestyle='none')
    # plt.set(xlabel='Kanalnummer', ylabel='Anzahl an Messergebnissen')
    plt.legend()
    ax.savefig(f'{path}\\{Name}.png')
    ax.show
    plt.cla()


def lin(Para, x): 
    return Para[0] + x*Para[1] - x*Para[1]


def fit(func, x, y, Name, yError, Farbe, labeln):
    model = odr.Model(func)
    mydata = odr.RealData(x, y, sx= 0.01, sy=yError)
    myodr = odr.ODR(mydata, model, beta0=[80.0, 0], maxit=1000)
    out = myodr.run()
    fy = func(out.beta, xWerte)
    # rsquared = r2_score(y, fy)
    # out.pprint()
    # print('$Parameter:', out.beta, out.sd_beta,  '$')
    # print('$R_{lin}^2 =',rsquared, '$')
    if labeln == True:
        plt.plot(xWerte, fy, label = f'{out.beta[0]:.1f} $^\circ C$', alpha=0.65, color=Farbe)
    else:
        plt.plot(xWerte, fy, label = Name, alpha=0.65, color=Farbe)
    return out


for i in range(len(Dateien)):
    Data = pd.read_csv(f'{path}\\{Dateien[i]}.csv', sep="\t",header=0, names=Anteile).astype(np.float64)
    temp = 0
    for j in Anteile:
        Mittelwert = sum(Data[j])/len(Data[j])
        SigmaTemp = 0
        for k in Data[j]:
            SigmaTemp = SigmaTemp + (k-Mittelwert)**2
        Sigma[i][temp] = np.sqrt(SigmaTemp/len(Data[j]))
        Mittelwertliste[i][temp] = Mittelwert
        temp += 1
    fit(lin, Anteil[:9], Mittelwertliste[i][:9], Dateien[i][10:], Sigma[i][:9], colortable[i], True)
    plt.set(xlabel='Stoffkonzentration $x_A$', ylabel='Temperatur in $^\circ C$')
    plt.set_title(f'{len(Data[j])} Messungen {Bezeichnung[i]}')
    plt.set_ylim(68, 132)
    plt.set_xlim(-0.02, 1.02)
    Menge.append(len(Data[j]))
    # X_Y_Spline = make_interp_spline(Anteil[9:], Mittelwertliste[i][9:])
    # Y_ = X_Y_Spline(xWerte)
    # plt.plot(xWerte, Y_, color=colortable[i], alpha=0.5)
    Plot(Mittelwertliste[i], Dateien[i], Sigma[i], colortable[i])


for i in range(len(Dateien)):
    fit(lin, Anteil[:9], Mittelwertliste[i][:9], None, Sigma[i][:9], colortable[i], False)
    plt.errorbar(Anteil, Mittelwertliste[i], xerr=0.01, yerr=Sigma[i], color=colortable[i], capsize=3, linestyle='none', label=Bezeichnung[i])
    X_Y_Spline = make_interp_spline(Anteil[9:], Mittelwertliste[i][9:])
    Y_ = X_Y_Spline(xWerte)
    plt.plot(xWerte, Y_, color=colortable[i], alpha=0.8)
plt.set_title(f'{sum(Menge)} Messungen von {Bezeichnung[0]} bis {Bezeichnung[-1]}')
plt.set(xlabel='Stoffkonzentration $x_A$', ylabel='Temperatur in $^\circ C$')
plt.set_ylim(68, 132)
plt.set_xlim(-0.02, 1.02)
plt.legend()
plt.grid()
ax.savefig(f'{path}\\Alle.png')
ax.show
plt.cla()


Gesamtdurchschnitt = np.zeros(len(Anteile))
Gesamtsigma = np.zeros(len(Anteile))
for i in range(len(Mittelwertliste)):
    Gesamtdurchschnitt = Gesamtdurchschnitt + Mittelwertliste[i]*(Menge[i]/sum(Menge))
    Gesamtsigma = Gesamtsigma + Sigma[i]*(Menge[i]/sum(Menge))
plt.errorbar(Anteil, Gesamtdurchschnitt, xerr=0.01, yerr=Gesamtsigma[i], color='black', capsize=3, linestyle='none', label=None)
fit(lin, Anteil[:9], Gesamtdurchschnitt[:9], None, Gesamtsigma[:9], 'black', True)
plt.set_title(f'{sum(Menge)} Messungen von {Bezeichnung[0]} bis {Bezeichnung[-1]}')
plt.set(xlabel='Stoffkonzentration $x_A$', ylabel='Temperatur in $^\circ C$')
plt.set_ylim(68, 132)
plt.set_xlim(-0.02, 1.02)
plt.legend()
plt.grid()
ax.savefig(f'{path}\\Gesamt.png')
ax.show()