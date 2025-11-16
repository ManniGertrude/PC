import matplotlib.pyplot as plt
import scipy.odr as odr
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline
import statistics as st
import os

# Pfad und Plot initialisieren
path = os.path.dirname(os.path.abspath(__file__))
fig, ax = plt.subplots()
xWerte = np.linspace(0, 1, 100)
colortable = ['sienna', 'darkgoldenrod', 'darkolivegreen', 'steelblue', 'darkmagenta', 'crimson']


# Stoffmengenanteile Acetanilid - Benzamid (x-Achse)
Anteil_Bd = [0.122, 0.199, 0.290, 0.430, 0.500, 0.600, 0.700, 0.800, 0.900, 0.000, 0.122, 0.199, 0.290, 0.430, 0.500, 0.600, 0.700, 0.800, 0.900, 1.000]
# Stoffmengenanteile Acetanilid - Benzil (x-Achse)
Anteil_Bl = [0.067, 0.176, 0.301, 0.392, 0.491, 0.600, 0.660, 0.750, 0.851, 0.000, 0.067, 0.176, 0.301, 0.392, 0.491, 0.600, 0.660, 0.750, 0.851, 1.000]	

Anteile = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'L0', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'LX']

# Dateinamen und Bezeichnungen
Dateien = []
for files in os.listdir(f'{path}\\Daten'):
    if files[:10] == 'Mikroskop_':
        Dateien.append(files[:-4])
Bezeichnung = [Dateien[i][10:] for i in range(len(Dateien))]


data_dict = {}
for Datei in Dateien:
    Data = pd.read_csv(f'{path}\\Daten\\{Datei}.csv', sep=",", header=0, names=Anteile)
    for index, row in Data.iterrows():
        index = index.replace('Bl', 'Benzil').replace('Bd', 'Benzamid')
        data_dict.update({f'{Datei[10:]}_{index}': row.to_list()})


def get_mean_std():
    mean_std = {key: {Stoff: [[],[], 0]for Stoff in ['Benzamid', 'Benzil']} for key in Bezeichnung}
    for semester in range(len(Bezeichnung)):
        for Stoff in ['Benzamid', 'Benzil']:
            semester_list = []
            for Data in data_dict:
                index = Data.split('_')
                if f'{index[0]}_{index[1]}' == Bezeichnung[semester] and index[3] == Stoff:
                    semester_list.append(data_dict[Data])
            if len(semester_list) != 0:
                mean_std[Bezeichnung[semester]][Stoff][0] = list(np.mean(semester_list, axis=0))
                mean_std[Bezeichnung[semester]][Stoff][1] = list(np.std(semester_list, axis=0))
                mean_std[Bezeichnung[semester]]['len'] = len(semester_list)
    return mean_std


# Plotparameter
def Plotparams(Name, Titel, minmax = [68, 132], legend=True):
    plt.ylim(minmax[0]-3, minmax[1]+3)
    plt.xlim(-0.02, 1.02)
    plt.xlabel('Stoffkonzentration $x_B$')
    plt.ylabel('Temperatur in$^\\circ C$')
    plt.legend()
    plt.grid()
    plt.title(Titel)
    plt.savefig(f'{path}\\PNG\\Mikroskop\\{Name}.png')
    plt.cla()


# Konstante Funktion für die Eutektikale
def lin(Para, x): 
    return Para * np.ones(len(x))


# Fitfunktion mit Fehler für die Eutektikale
def fit(func, x, y, Name, yError, Farbe, labeln):
    model = odr.Model(func)
    mydata = odr.RealData(x, y, sx= 0.01, sy=yError)
    myodr = odr.ODR(mydata, model, beta0=[80.0], maxit=1000)
    out = myodr.run()
    fy = func(out.beta, xWerte)
    if labeln == True:
        plt.plot(xWerte, fy, label = f'[{out.beta[0]:.1f}$\\pm${np.sqrt(out.sd_beta[0]**2 + st.mean(yError)**2):.1f}]$^\\circ C$', alpha=0.65, color=Farbe)
    else:
        plt.plot(xWerte, fy, label = Name, alpha=0.65, color=Farbe)
    return out


def eine_gruppe_ein_plot(Semester, Gruppe):
    for Stoff in ['Benzil', 'Benzamid']:
        if f'{Semester}_{Gruppe}_{Stoff}' in data_dict:
            Data = data_dict[f'{Semester}_{Gruppe}_{Stoff}']
        else: 
            continue
        if Stoff == 'Benzil':
            Anteil = Anteil_Bl
        elif Stoff == 'Benzamid':
            Anteil = Anteil_Bd
        plt.errorbar(Anteil[9:], Data[9:], xerr=0.01, yerr=1, color='navy', capsize=3, linestyle='none', label='Liquidus')
        plt.errorbar(Anteil[:9], Data[:9], xerr=0.01, yerr=1, color='red', capsize=3, linestyle='none', label='Eutektikale')
        fit(lin, Anteil[:9], Data[:9], None, [0.1]*9, 'purple', True)
        Plotparams(f'{Semester[0:2]} {Semester[3:]}\\{Gruppe}_{Stoff}_Mikroskop', f'Daten der Gruppe {Gruppe} aus dem {Semester}\nAcetanilid - {Stoff}')


# Jede Gruppe in einem Plot
def jede_gruppe_ein_plot():
    for Data in data_dict:
        minmax = [min(data_dict[Data]), max(data_dict[Data])]
        index = Data.split('_')
        if index[3] == 'Benzil':
            Anteil = Anteil_Bl
        elif index[3] == 'Benzamid':
            Anteil = Anteil_Bd

        plt.errorbar(Anteil[9:], data_dict[Data][9:], xerr=0.01, yerr=1, color='navy', capsize=3, linestyle='none', label='Liquidus')
        plt.errorbar(Anteil[:9], data_dict[Data][:9], xerr=0.01, yerr=1, color='red', capsize=3, linestyle='none', label='Eutektikale')
        fit(lin, Anteil[:9], data_dict[Data][:9], None, [0.1]*9, 'purple', True)
        if not os.path.exists(f'{path}\\PNG\\Mikroskop\\{index[0]} {index[1]}'):
            os.makedirs(f'{path}\\PNG\\Mikroskop\\{index[0]} {index[1]}')
        Plotparams(f'{index[0]} {index[1]}\\{index[2]}_{index[3]}_Mikroskop', f'Daten der Gruppe {index[2]} aus dem {index[0]} {index[1]}\nAcetanilid - {index[3]}', minmax)



# Jedes Semester einzeln in einem Plot pro Stoff
def jedes_semester_ein_plot():
    for semester in range(len(Bezeichnung)):
        minmax = [100, 100]
        for Stoff in ['Benzamid', 'Benzil']:
            if mean_std[Bezeichnung[semester]][Stoff][0] != []:
                for Data in data_dict:
                    index = Data.split('_')
                    if Stoff == 'Benzamid':
                        Anteil = Anteil_Bd
                    elif Stoff == 'Benzil':
                        Anteil = Anteil_Bl
                    if f'{index[0]}_{index[1]}' == Bezeichnung[semester] and index[3] == Stoff:
                        plt.errorbar(Anteil[9:], data_dict[Data][9:], xerr=0.01, yerr=1, color='navy', capsize=3, linestyle='none')
                        plt.errorbar(Anteil[:9], data_dict[Data][:9], xerr=0.01, yerr=1, color='red', capsize=3, linestyle='none')
                        minmax[0] = min(minmax[0], np.min(data_dict[Data]))
                        minmax[1] = max(minmax[1], np.max(data_dict[Data]))
                # Berechnung des Mittelwerts und der Standardabweichung für jeden Wert   
                fit(lin, Anteil[:9], mean_std[Bezeichnung[semester]][Stoff][0][:9], None, mean_std[Bezeichnung[semester]][Stoff][1][:9], 'purple', True)
                Plotparams(f'{Bezeichnung[semester]}_{Stoff}', f'Daten des {Bezeichnung[semester]} Semesters\nAcetanilid - {Stoff}', minmax, False)



def jeder_stoff_ein_plot(Probegruppe = None):
    for Stoff in ['Benzamid', 'Benzil']:
        minmax = [100, 100]
        if Stoff == 'Benzamid':
            Anteil = Anteil_Bd
        elif Stoff == 'Benzil':
            Anteil = Anteil_Bl
        for Data in data_dict:
            index = Data.split('_')
            if index[3] == Stoff:
                plt.errorbar(Anteil[9:], data_dict[Data][9:], xerr=0.01, yerr=1, color='blue', capsize=3, linestyle='none', alpha=0.1, zorder = 2)
                plt.errorbar(Anteil[:9], data_dict[Data][:9], xerr=0.01, yerr=1, color='red', capsize=3, linestyle='none', alpha=0.1, zorder = 2)
                minmax[0] = min(minmax[0], np.min(data_dict[Data]))
                minmax[1] = max(minmax[1], np.max(data_dict[Data]))
        mean = []
        Sigma = []
        Len = 0
        for semester in range(len(Bezeichnung)):
            if mean_std[Bezeichnung[semester]][Stoff][0] != []:
                mean.append(mean_std[Bezeichnung[semester]][Stoff][0])
                Sigma.append(np.array(mean_std[Bezeichnung[semester]][Stoff][1])**2)
                Len += mean_std[Bezeichnung[semester]]['len']
        plt.errorbar(Anteil[9:], np.mean(mean, axis=0)[9:], xerr=0.01, yerr=np.sqrt(np.mean(Sigma, axis=0))[9:], color='navy',    capsize=4, linewidth = 1.5, linestyle='none', label='Liquidus', zorder = 6)
        plt.errorbar(Anteil[:9], np.mean(mean, axis=0)[:9], xerr=0.01, yerr=np.sqrt(np.mean(Sigma, axis=0))[:9], color='crimson', capsize=4, linewidth = 1.5, linestyle='none', label='Eutektikale', zorder = 6)
        fit(lin, Anteil[:9], np.mean(mean, axis=0)[:9], None, np.sqrt(np.mean(Sigma, axis=0))[:9], 'purple', True)
        if Probegruppe != None and f'{Probegruppe}_{Stoff}' in data_dict:
            Probegruppen_Data = data_dict[f'{Probegruppe}_{Stoff}']
            # print(Anteil, Probegruppen_Data)
            plt.errorbar(Anteil[9:], Probegruppen_Data[9:], xerr=0.01, yerr=1, linestyle='none', color='black', capsize=3, capthick=2, zorder = 12, label=f'Probegruppe {Probegruppe}')
            plt.errorbar(Anteil[:9], Probegruppen_Data[:9], xerr=0.01, yerr=1, linestyle='none', color='black', capsize=3, capthick=2, zorder = 12)
        Plotparams(f'Alle {Stoff}', f'{Len} Messungen\nAcetanilid - {Stoff}', minmax, True)


if __name__ == '__main__':
    # eine_gruppe_ein_plot('WS_25-26', 'B5')       # Beispiel für eine Gruppe
    # jede_gruppe_ein_plot()                     # Gibt für jede Gruppe einen Plot aus
    mean_std = get_mean_std()
    # jedes_semester_ein_plot()                  # Gibt für jedes Semester einen Plot aus
    jeder_stoff_ein_plot()                     # Gibt die Zusammenfassungen in einem Plot aus
