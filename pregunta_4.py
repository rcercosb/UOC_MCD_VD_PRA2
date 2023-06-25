import pandas as pd
import numpy as np

from pregunta_3 import p3

def p4(input, range_diff, verbose = False):
    sectors = np.unique(input["SECTOR"]) # Obté el nom dels sectors

    outputs = []

    for sector in sectors:
        # El fitxer pregunta_2.csv té el mateix format que el pregunta_1.csv excepte la columna SECTOR
        # Per tant, es duu a terme el processament de pregunta_3.py per cada un dels sectors (eliminant la columna)
        df = p3(input.loc[input["SECTOR"] == sector, input.columns != "SECTOR"], range_diff, verbose)
        # Com que en el pas anterior s'elimina la columna SECTOR, ara es torna a crear i a omplir amb el nom del sector corresponent
        df["SECTOR"] = np.repeat(sector, df.shape[0]).tolist()

        outputs.append(df)

    # Es mouen els dataframes per tal que estiguin ordenats per sector de la manera següent: Electricitat, Calefacció i refrigeració, Transport i Total
    outputs.insert(0, outputs.pop(1))
    outputs.insert(3, outputs.pop(2))


    output = pd.concat(outputs) # Concatena la llista de dataframes

    if verbose:
        print(output)

    return output


if __name__ == "__main__":
    # Font: pregunta_2.csv
    input = pd.read_csv("pregunta_2.csv", encoding = "UTF-8") # Llegeix el fitxer CSV

    input = input[input["PAÍS"] != "EU-27 (2020)"] # Elimina EU-27 (2020)

    output = p4(input, 7, True)

    output.to_csv("pregunta_4.csv", encoding = "UTF-8", index = False) # Desa el conjunt de dades modificades en un nou fitxer CSV