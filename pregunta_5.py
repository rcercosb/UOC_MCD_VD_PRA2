import pandas as pd
import numpy as np

def p5_1(input, range_diff, verbose = False):
    country = []
    range_name = []
    diff = []

    ranges = []

    for i in range(1, len(input.columns), range_diff): # Obté els rangs d'anys
        if (i + range_diff) >= len(input.columns):
            ranges.append((input.columns[i], input.columns[-1]))
        else:
            ranges.append((input.columns[i], input.columns[i + range_diff]))

    if verbose:
        print(ranges)

    for range_start, range_end in ranges:
        country += input.loc[:, "PAÍS"].tolist() # El nom dels països

        range_name += np.tile("{}-{}".format(range_start, range_end), input.shape[0]).tolist() # Desa tants "noms" de rang com països

        start = input.loc[:, range_start].tolist() # Obté els valors del primer any del rang
        end = input.loc[:, range_end].tolist() # Obté els valors de l'últim any del rang

        diff += np.subtract(np.array(end), np.array(start)).tolist() # Les diferències entre els valors de l'últim i el primer any del rang

    output = pd.DataFrame(data = {"PAÍS": country, "RANG": range_name, "DIFERÈNCIA": diff})

    if verbose:
        print(output)

    return output

def p5_2(input,  range_diff, verbose = False):
    sectors = np.unique(input["SECTOR"]) # Obté el nom dels sectors

    outputs = []

    for sector in sectors:
        # El fitxer pregunta_2.csv té el mateix format que el pregunta_1.csv excepte la columna SECTOR
        # Per tant, es duu a terme el processament de pregunta_3.py per cada un dels sectors (eliminant la columna)
        df = p5_1(input.loc[input["SECTOR"] == sector, input.columns != "SECTOR"], range_diff, verbose)
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
    # Font: pregunta_1.csv i pregunta_2.csv
    pregunta_1 = pd.read_csv("pregunta_1.csv", encoding = "UTF-8") # 1990-2021 i 31 països (+ Suïssa)
    pregunta_2 = pd.read_csv("pregunta_2.csv", encoding = "UTF-8") # 2004-2021 i 35 països (- Suïssa)

    # 1990-2021 i 31 països -> 2004-2021 i 29 països
    pregunta_1 = pregunta_1[pregunta_2.columns[:-1]]
    pregunta_1 = pregunta_1[pregunta_1["PAÍS"] != "Suïssa"] # Elimina Suïssa
    pregunta_1 = pregunta_1[pregunta_1["PAÍS"] != "EU-27 (2020)"] # Elimina EU-27 (2020)
    
    pregunta_2 = pregunta_2[pregunta_2["PAÍS"].isin(pregunta_1["PAÍS"])] # 2004-2021 i 35 països -> 2004-2021 i 29 països

    emissions = p5_1(pregunta_1, 7)
    energy = p5_2(pregunta_2, 7)

    print(emissions)
    print(energy)

    output = energy

    output.rename(columns = {"DIFERÈNCIA": "MD_ENERGIA"}, inplace = True) # Canvia el nom de la segona columna: DIFERÈNCIA -> MD_ENERGIA
    output["MD_EMISSIONS"] = np.tile(emissions["DIFERÈNCIA"], len(np.unique(energy["SECTOR"]))) # Repeteix nº de sectors vegades les diferències d'emissions

    # Arrodoneix a dos decimals
    output["MD_ENERGIA"] = output["MD_ENERGIA"].round(2)
    output["MD_EMISSIONS"] = output["MD_EMISSIONS"].round(2)

    print(output)

    output.to_csv("pregunta_5.csv", encoding = "UTF-8", index = False) # Desa el conjunt de dades modificades en un nou fitxer CSV