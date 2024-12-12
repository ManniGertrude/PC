import os
import pandas as pd

path = os.path.dirname(os.path.dirname(__file__))

# Einlesen der Daten
Anteil = ['0.122', '0.199', '0.290', '0.430', '0.500', '0.600', '0.700', '0.800', '0.900', '0.000', '0.122', '0.199', '0.290', '0.430', '0.500', '0.600', '0.700', '0.800', '0.900', '1.000']
Anteile = ['Gruppe', 'E122', 'E199', 'E290', 'E430', 'E500', 'E600', 'E700', 'E800', 'E900', 'L000', 'L122', 'L199', 'L290', 'L430', 'L500', 'L600', 'L700', 'L800', 'L900', 'E1000']

Dateien = ['Mikroskop_WS_22-23', 'Mikroskop_SS_23', 'Mikroskop_WS_23-24', 'Mikroskop_SS_24']# , 'Mikroskop_WS_24-25'
Bezeichnung = ['WS 22-23', 'SS 23', 'WS 23-24', 'SS 24']# , 'WS 24-25'

NamenE = ['0.122', '0.199', '0.290', '0.430', '0.500', '0.600', '0.700', '0.800', '0.900']
NamenL = ['0.000', '0.122', '0.199', '0.290', '0.430', '0.500', '0.600', '0.700', '0.800', '0.900', '1.000']

AnteileE = ['E122', 'E199', 'E290', 'E430', 'E500', 'E600', 'E700', 'E800', 'E900']
AnteileL = ['L000', 'L122', 'L199', 'L290', 'L430', 'L500', 'L600', 'L700', 'L800', 'L900', 'E1000']

# Erstellen der Tabellen
Text = []
for i in range(len(Bezeichnung)):
    # Einlesen der Daten
    DataE = pd.read_csv(f'{path}\\{Dateien[i]}.csv', sep=",",header=0, names=Anteile, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    DataL = pd.read_csv(f'{path}\\{Dateien[i]}.csv', sep=",",header=0, names=Anteile, usecols=[0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    
    # Umbenennen der Spalten
    Text.append(f'\\section*{"{"}{Bezeichnung[i]}{"}"}\n\\begin{"{"}table{"}"}[h]\n\\centering ') 
    Text.append(DataE.to_latex(index=False,formatters={"name": str.upper},float_format="{:.1f}".format,)) 
    Text.append(f'\\caption{"{"}Messdaten aus dem {Bezeichnung[i]} durch verschiedene 1/1000 Anteile Acetanilid zu Benzamid\\\\mit unterer- bzw. Eutektikum-Schmelztemperatur in Celsius{"}"}\n\\end{"{"}table{"}"}\n') 
    Text.append(f'\\begin{"{"}table{"}"}[h]\n\\centering ')
    Text.append(DataL.to_latex(index=False,formatters={"name": str.upper},float_format="{:.1f}".format,))
    Text.append(f'\\caption{"{"}Messdaten aus dem {Bezeichnung[i]} durch verschiedene 1/1000 Anteile Acetanilid zu Benzamid\\\\mit oberer- bzw. Liquidus-Schmelztemperatur in Celsius{"}"}\n\\end{"{"}table{"}"}\n\\newpage') 

# Speichern der Tabellen
with open(f'{path}\\DatenPDF\\DatenPDFTab.tex', 'w') as datei:
    datei.write(''.join(Text))
