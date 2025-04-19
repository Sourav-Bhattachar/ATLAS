from RUN.FEATURES.remove_words import remove_words
import pubchempy

def element_details(query):
    words_to_remove = ['atlas','please','what','is','the','iupac','details','molecular','weight','formula','give','me','name','of','element']
    query = remove_words(query, words_to_remove)
    query = query.replace(' ','')
    query = str(query)

    try:
        compound = pubchempy.get_compounds(query,'name')[0]
        response_text = (
            f'IUPAC Name: {compound.iupac_name}.\n'
            f'Common Name: {compound.synonyms[0]}.\n'
            f'Moleculer Weight : {compound.molecular_weight} amu.\n'
            f'Formula: {compound.molecular_formula}.\n'
        )
        return response_text
        
    except Exception as e:
        return f"{query} is not valid"