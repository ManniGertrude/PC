import matplotlib.pyplot as plt
import scipy.odr as odr
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline
import statistics as st

path = "C:\\Users\\kontr\\Desktop\\Github\\PC"  # PC
# path = 'C:\\Users\\Surface Pro 7 Manni\\Desktop\\Code Dateien\\P5\\525\\Messungen\\csv' # Surface

Anteil = ['0.122', '0.199', '0.290', '0.430', '0.500', '0.600', '0.700', '0.800', '0.900', '0.000', '0.122', '0.199', '0.290', '0.430', '0.500', '0.600', '0.700', '0.800', '0.900', '1.000']
Anteile = ['Gruppe', 'E122', 'E199', 'E290', 'E430', 'E500', 'E600', 'E700', 'E800', 'E900', 'L000', 'L122', 'L199', 'L290', 'L430', 'L500', 'L600', 'L700', 'L800', 'L900', 'E1000']

Dateien = ['Mikroskop_WS_22-23', 'Mikroskop_SS_23', 'Mikroskop_WS_23-24', 'Mikroskop_SS_24']# , 'Mikroskop_WS_24-25'
Bezeichnung = ['WS 22-23', 'SS 23', 'WS 23-24', 'SS 24']# , 'WS 24-25'

NamenE = ['0.122', '0.199', '0.290', '0.430', '0.500', '0.600', '0.700', '0.800', '0.900']
NamenL = ['0.000', '0.122', '0.199', '0.290', '0.430', '0.500', '0.600', '0.700', '0.800', '0.900', '1.000']

AnteileE = ['E122', 'E199', 'E290', 'E430', 'E500', 'E600', 'E700', 'E800', 'E900']
AnteileL = ['L000', 'L122', 'L199', 'L290', 'L430', 'L500', 'L600', 'L700', 'L800', 'L900', 'E1000']


Text = []

for i in range(len(Bezeichnung)):
    DataE = pd.read_csv(f'{path}\\Daten\\{Dateien[i]}.csv', sep=",",header=0, names=Anteile, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    DataL = pd.read_csv(f'{path}\\Daten\\{Dateien[i]}.csv', sep=",",header=0, names=Anteile, usecols=[0, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    
    
    Text.append(f'\\section*{"{"}{Bezeichnung[i]}{"}"}\n\\begin{"{"}table{"}"}[h]\n\\centering ') 
    Text.append(DataE.to_latex(index=False,formatters={"name": str.upper},float_format="{:.1f}".format,)) 
    Text.append(f'\\caption{"{"}Messdaten aus dem {Bezeichnung[i]} durch verschiedene 1/1000 Anteile Acetanilid zu Benzamid\\\\mit unterer- bzw. Eutektikum-Schmelztemperatur in Celsius{"}"}\n\\end{"{"}table{"}"}\n') 
    Text.append(f'\\begin{"{"}table{"}"}[h]\n\\centering ')
    Text.append(DataL.to_latex(index=False,formatters={"name": str.upper},float_format="{:.1f}".format,))
    Text.append(f'\\caption{"{"}Messdaten aus dem {Bezeichnung[i]} durch verschiedene 1/1000 Anteile Acetanilid zu Benzamid\\\\mit oberer- bzw. Liquidus-Schmelztemperatur in Celsius{"}"}\n\\end{"{"}table{"}"}\n\\newpage') 

with open(f'{path}\\Daten\\DatenPDF\\DatenPDFTab.tex', 'w') as datei:
    datei.write(''.join(Text))
