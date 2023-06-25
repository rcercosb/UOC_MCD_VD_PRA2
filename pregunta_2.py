import pandas as pd
import numpy as np

def p2(verbose = False):
     # Font: https://ec.europa.eu/eurostat/databrowser/view/SDG_07_40/default/table?lang=en > Download > Full dataset [SDG_07_40] > TSV

     def conv(val): # En la columna 2004
          val = val.replace(" ", "") # Elimina espais
          
          if val == ":": # Substitueix els dos punts per res
               return np.nan
          else:
               return np.float64(val) # Converteix tots els valors numèrics (interpretats com una string) a float

     energy = pd.read_csv("sdg_07_40_tabular.tsv", sep = "\t", converters = {'2004 ': conv}) # Llegeix el fitxer TSV (Valors Separats per Tabulacions)

     energy.rename(columns = {"freq,nrg_bal,unit,geo\TIME_PERIOD": "PAÍS"}, inplace = True) # Canvia el nom de la primera columna: freq,nrg_bal,unit,geo\TIME_PERIOD -> PAÍS
     energy.columns = energy.columns.str.replace(' ', '') # Elimina els espais en blanc en el nom de les columnes: "2004 " -> "2004"

     e = {"REN": "Total", "REN_TRA": "Transport", "REN_ELC": "Electricitat", "REN_HEAT_CL": "Calefacció i refrigeració"}

     # Crea una columna que indica el sector en el qual es consumeix l'energia renovable: total, transport, electricitat i calefacció i refrigeració
     energy["SECTOR"] = energy["PAÍS"].apply(lambda x: e[x.split(",")[1]])

     # https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes

     p = {"AT": "Àustria", "BE": "Bèlgica", "BG": "Bulgària", "CY": "Xipre", "CZ": "Txèquia", "DE": "Alemanya", "DK": "Dinamarca", "EE": "Estònia", "EL": "Grècia", "ES": "Espanya",
          "EU27_2020": "EU-27 (2020)", "FI": "Finlàndia", "FR": "França", "HR": "Croàcia", "HU": "Hongria", "IE": "Irlanda", "IS": "Islàndia", "IT": "Itàlia", "LT": "Lituània", "LU": "Luxemburg",
          "LV": "Letònia", "MT": "Malta", "NL": "Països Baixos", "NO": "Noruega", "PL": "Polònia", "PT": "Portugal", "RO": "Romania", "SE": "Suècia", "SI": "Eslovènia", "SK": "Eslovàquia",
          "AL": "Albània", "ME": "Montenegro", "MK": "Macedònia del Nord", "RS": "Sèrbia", "XK": "Kosovo"}

     energy["PAÍS"] = energy["PAÍS"].apply(lambda x: p[x[x.rfind(",") + 1:]]) # Canvia el valor de les files de la primera columna: A,REN,PC,AL -> AL -> Albània

     if verbose:
          print(energy)

     return energy


if __name__ == "__main__":
     energy = p2(True)
     energy.to_csv("pregunta_2.csv", encoding = "UTF-8", index = False) # Desa el conjunt de dades modificades en un nou fitxer CSV