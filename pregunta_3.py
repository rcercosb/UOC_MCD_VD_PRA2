import pandas as pd
import numpy as np

def p3(input, range_diff, verbose = False):
    country = []
    range_name = []
    diff = []
    category = []

    ranges = []

    for i in range(1, len(input.columns), range_diff): # Obté els rangs d'anys
        if (i + range_diff) >= len(input.columns):
            ranges.append((input.columns[i], input.columns[-1]))
        else:
            ranges.append((input.columns[i], input.columns[i + range_diff]))

    if verbose:
        print(ranges)

    categories = ["Baix", "Mitjà", "Alt", "Molt alt"]

    for range_start, range_end in ranges:
        country += input.loc[:, "PAÍS"].tolist() # Els noms dels països

        range_name += np.tile("{}-{}".format(range_start, range_end), input.shape[0]).tolist() # Desa tants "noms" de rangs com països

        start = input.loc[:, range_start].tolist() # Obté els valors del primer any del rang
        end = input.loc[:, range_end].tolist() # Obté els valors de l'últim any del rang

        diff += np.subtract(np.array(end), np.array(start)).tolist() # Les diferències entre els valors de l'últim i el primer any del rang
        
        means = np.mean(input.loc[:, range_start:range_end], axis = 1) # Les mitjanes de les emissions emeses / percentatge d'energia renovable consumida durant el rang d'anys

        q1 = np.quantile(means, 0.25) # El primer quartil
        q2 = np.quantile(means, 0.5) # El segon quartil
        q3 = np.quantile(means, 0.75) # El tercer quartil

        for mean in means: # Indica la categoria d'emissions emeses / d'energia renovable consumida a la qual pertany cada país
            if mean < q1:
                category.append(categories[0])
            elif mean >= q1 and mean < q2:
                category.append(categories[1])
            elif mean >= q2 and mean < q3:
                category.append(categories[2])
            elif mean >= q3:
                category.append(categories[3])


    tmp = pd.DataFrame(data = {"PAÍS": country, "RANG": range_name, "DIFERÈNCIA": diff, "CATEGORIA": category})

    if verbose:
        print(tmp)

    # Per cada combinació de rang i categoria obté la mitjana de les diferències de tots els països que hi pertanyen
    mean_diff = tmp.groupby(["RANG", "CATEGORIA"])["DIFERÈNCIA"].mean().round(2)

    if verbose:
        print(mean_diff)

    mean_diff = mean_diff.tolist()

    for i in range(0, len(mean_diff), len(categories)): # Es mouen les mitjanes d'Alt de la primera a la tercera posició (seguint el mateix ordre de categories)
        mean_diff.insert(i + 2, mean_diff.pop(i))

    range_name = np.repeat(np.unique(range_name), len(categories)).tolist() # Repeteix nº de categories vegades cada un dels "noms" de rangs
    category = np.tile(categories, len(ranges)).tolist() # Repeteix nº de rangs vegades la llista categories

    new_emissions = pd.DataFrame(data = {"RANG": range_name, "CATEGORIA": category, "MITJANA_DIFERÈNCIA": mean_diff})

    if verbose:
        print(new_emissions)

    return new_emissions

if __name__ == "__main__":
    # Font: pregunta_1.csv

    input = pd.read_csv("pregunta_1.csv", encoding = "UTF-8") # Llegeix el fitxer CSV

    input = input[input["PAÍS"] != "EU-27 (2020)"] # Elimina EU-27 (2020)

    output = p3(input, 7, True)

    output.to_csv("pregunta_3.csv", encoding = "UTF-8", index = False) # Desa el conjunt de dades modificades en un nou fitxer CSV