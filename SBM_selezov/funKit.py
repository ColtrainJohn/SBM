## standart


## special
import numpy as np
import pandas as pd
import psycopg2 as pg
from sqlalchemy import create_engine


## This !
from . import psq



def base_get(SQL, **kwargs):
    
    with pg.connect(psq.authentication) as conn:
        return pd.io.sql.read_sql(SQL, conn, **kwargs)


def put_to_pg(dataframe, framename, index_label=None):
    engine = create_engine(psq.sql_alchemy_auth)
    dataframe.to_sql(framename, engine, if_exists='append', index=True, index_label=index_label)
    return True


# def get_google_doc(doc_name, sheet_name):

#     gs = gspread.service_account('googleKey.json')
#     sheet = gs.open(doc_name).worksheet(sheet_name)
#     tab = pd.DataFrame(sheet.get_all_records(numericise_ignore=['all']))

#     return tab



# def reload_std_names():
#     doc = get_google_doc('Slovnik2', 'standart_names')
#     doc.columns = [col.lower() for col in doc]
#     put_to_pg(doc, 'parameter_name_mapping', index_label='id')
#     return True


# def get_lab_parameter_names(lab):
#     query = f'SELECT russian_name, engl, {lab} FROM parameter_name_mapping;'
#     lab_tab = base_get(query)
#     lab_tab = lab_tab.loc[~lab_tab[lab].isna()]
#     lab_tab_dict = dict(zip(lab_tab[lab], lab_tab['engl']))

#     return lab_tab_dict
