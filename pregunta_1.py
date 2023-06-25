import pandas as pd

def p1(verbose = False):
     # Font: https://ec.europa.eu/eurostat/databrowser/bookmark/1f9e4da2-3d49-4726-8fdc-74988ab529aa?lang=en > Download > Data on this page only > TSV

     emissions = pd.read_csv("sdg_13_10_page_tabular.tsv", sep = "\t") # Llegeix el fitxer TSV (Valors Separats per Tabulacions)

     emissions.rename(columns = {"freq,airpol,src_crf,unit,geo\TIME_PERIOD": "PAÍS"}, inplace = True) # Canvia el nom de la primera columna: freq,airpol,src_crf,unit,geo\TIME_PERIOD -> PAÍS
     emissions.columns = emissions.columns.str.replace(' ', '') # Elimina els espais en blanc en el nom de les columnes: "1990 " -> "1990"

     # https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Country_codes

     p = {"AT": "Àustria", "BE": "Bèlgica", "BG": "Bulgària", "CH": "Suïssa", "CY": "Xipre", "CZ": "Txèquia", "DE": "Alemanya", "DK": "Dinamarca", "EE": "Estònia", "EL": "Grècia", "ES": "Espanya",
          "EU27_2020": "EU-27 (2020)", "FI": "Finlàndia", "FR": "França", "HR": "Croàcia", "HU": "Hongria", "IE": "Irlanda", "IS": "Islàndia", "IT": "Itàlia", "LT": "Lituània", "LU": "Luxemburg",
          "LV": "Letònia", "MT": "Malta", "NL": "Països Baixos", "NO": "Noruega", "PL": "Polònia", "PT": "Portugal", "RO": "Romania", "SE": "Suècia", "SI": "Eslovènia", "SK": "Eslovàquia"}

     emissions["PAÍS"] = emissions["PAÍS"].apply(lambda x: p[x[24:]]) # Canvia el valor de les files de la primera columna: A,GHG,TOTXMEMONIA,I90,AT -> AT -> Àustria

     if verbose:
          print(emissions)

     return emissions


if __name__ == "__main__":
     emissions = p1(True)
     emissions.to_csv("pregunta_1.csv", encoding = "UTF-8", index = False) # Desa el conjunt de dades modificades en un nou fitxer CSV