import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import math.h as m

df = pd.read_excel("serii-timp.xlsx")
df.head(8)

# Evolutie
x1 = (df['Luna'])
y = df['yi']

plt.plot(x1, y)
plt.ylim(6000, 18000)
plt.grid
plt.xlabel('Luna', fontsize=20, color='orange')
plt.ylabel('Productie', fontsize=20, color='orange')
plt.show()

modificare_abs_baza_fixa = []
for i in range(len(df)):
    x = df["yi"][i] - df["yi"][0]
    modificare_abs_baza_fixa.append(x)

print(modificare_abs_baza_fixa)
x1 = pd.DataFrame(modificare_abs_baza_fixa, index=range(0, len(df)))
x1.columns = ["Modificare abosluta baza fixa"]
df = df.join(x1)

indice_dinamica_baza_fixa = []
for i in range(len(df)):
    x = df["yi"][i] / df["yi"][0]
    indice_dinamica_baza_fixa.append(x)

print(indice_dinamica_baza_fixa)
x2 = pd.DataFrame(indice_dinamica_baza_fixa)
x2.columns = ["indice_dinamica_baza_fixa"]
df = df.join(x2)

indice_dinamica_baza_lant = []
for i in range(1, len(df)):
    x = df["yi"][i] / df["yi"][i - 1]
    indice_dinamica_baza_lant.append(x)

print(indice_dinamica_baza_lant)
x3 = pd.DataFrame(indice_dinamica_baza_lant)
x3.columns = ["indice_dinamica_baza_lant"]
x3.index += 1
df = df.join(x3)

ritm_modificare_baxa_fixa = []
for i in indice_dinamica_baza_fixa:
    ritm_modificare_baxa_fixa.append(i * 100 - 100)
print(ritm_modificare_baxa_fixa)
x4 = pd.DataFrame(ritm_modificare_baxa_fixa)
x4.columns = ["ritm_modificare_baxa_fixa"]
df = df.join(x4)

ritm_modificare_baxa_lant = []
for i in range(0, len(indice_dinamica_baza_lant)):
    ritm_modificare_baxa_lant.append(indice_dinamica_baza_lant[i] * 100 - 100)
print(ritm_modificare_baxa_lant)
x5 = pd.DataFrame(ritm_modificare_baxa_lant)
x5.columns = ["ritm_modificare_baxa_lant"]
x5.index += 1
df = df.join(x5)

# valoare absoluta a unui procent din ritmul de modificare cu baza fixa
val_abs = [i / 100 for i in df["yi"]]
x6 = pd.DataFrame(val_abs)
x6.columns = ["val abs"]
df = df.join(x6)

df.to_excel("serii de timp.xlsx", index=False)

print("Indicatorii medii:")
print("Nivelul mediu al seriei cronologice = ", np.sum(df["yi"]))
modificare_medie_abs = modificare_abs_baza_fixa[len(df) - 1] / (len(df) - 1)
print("Modificarea medie absoluta = ", modificare_medie_abs)
indice_mediu_modificare = pow(indice_dinamica_baza_fixa[len(df) - 1], 1 / len(df))
print("Indicele mediu de modificare = ", indice_mediu_modificare)
print("Productia a crescuti in medie de la o luna la alta de", indice_mediu_modificare)
print("Ritmul mediu de modificare = ", (pow(indice_dinamica_baza_fixa[len(df) - 1], 1 / len(df)) - 1) * 100)
print("Productia a crescut in medie, de la o luna la alta cu",
      (pow(indice_dinamica_baza_fixa[len(df) - 1], 1 / len(df)) - 1) * 100)

df_ajust = pd.read_excel("serii-timp.xlsx", index=False)

yt_ajustatMMA = []
for i in range(1, len(df_ajust)):
    yt_ajustatMMA.append(df_ajust["yi"][0] + (i - 1) * modificare_medie_abs)
print(yt_ajustatMMA)
xa1 = pd.DataFrame(yt_ajustatMMA)
xa1.columns = ["yt_ajustatMMA"]
df_ajust = df_ajust.join(xa1)
df_ajust.iloc[df_ajust.shape[0] - 1, df_ajust.shape[1] - 1] = df_ajust.iloc[
    df_ajust.shape[0] - 1, df_ajust.shape[1] - 2]

yt_ajustatMIM = []
for i in range(1, len(df_ajust)):
    yt_ajustatMIM.append(df_ajust["yi"][0] * pow(indice_mediu_modificare, i - 1))
print(yt_ajustatMIM)
xa2 = pd.DataFrame(yt_ajustatMIM)
xa2.columns = ["yt_ajustatMIM"]
df_ajust = df_ajust.join(xa2)
df_ajust.iloc[df_ajust.shape[0] - 1, df_ajust.shape[1] - 1] = df_ajust.iloc[
    df_ajust.shape[0] - 1, df_ajust.shape[1] - 2]
df_ajust.to_excel("Ajustare-MetMecanice1.xlsx", index=False)




