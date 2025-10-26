import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


# Versuchsteil 1: Absorptionsspektrum zw. 390 nm und 700 nm
data1 = pd.read_csv(os.path.dirname(__file__) + 'Absorptionsspektrum.csv', sep=';', decimal=',', header=0)
wavelength1 = data1['Wellenlänge (nm)']
absorption1 = data1['Absorption']
plt.figure(figsize=(10, 6))
plt.plot(wavelength1, absorption1, label='Absorptionsspektrum', color='blue')
plt.title('Absorptionsspektrum zwischen 390 nm und 700 nm')
plt.xlabel('Wellenlänge (nm)')
plt.ylabel('Absorption')
plt.grid()
plt.legend()
plt.savefig(os.path.dirname(__file__) + 'Absorptionsspektrum.png')
