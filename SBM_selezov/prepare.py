## standart


## special
import pandas as pd


# This !
from . import psq
from . import funKit
from . import common_steps


def test_file(lab_id=1):

    if lab_id == 1:
        return pd.read_csv(psq.test_cmd_datapoints, sep=';'), lab_id

    elif lab_id == 8:
        patients = pd.read_excel(psq.test_patients_invitro)
        datapoints = pd.read_excel(psq.test_datapoints_invitro)
        return datapoints, lab_id, patients

    elif lab_id == 2:
        return pd.read_excel(psq.test_datapoints_litech), lab_id
        


def prepare_cmd(dataset: pd.DataFrame):

    # Select necessary columns
    dataset = dataset[['Идентификатор пациента', 'Пол', 'Дата рождения', 'Дата исследования', 'Тест', 'Результат', 'Округ',	'Город']]

    # Unify column names
    dataset = dataset.rename(
        columns = {
            'Идентификатор пациента': 'original_id',
            'Дата рождения': 'birthdate',
            'Дата исследования': 'date',
            'Тест': 'parameter_id',
            'Результат': 'value',
            'Пол': 'sex',
        })
    
    ## Можно это не через эксель как то?
    birth_day_correction = pd.read_excel(psq.birthDayCorrectionFile)
    non_valid_patients = pd.read_excel(psq.nonValidPatientsFile)

    # Filter known patients
    dataset = dataset.loc[~dataset['original_id'].isin(list(non_valid_patients['Идентификатор пациента']))]

    # Correct known errors 
    for c in birth_day_correction.to_dict(orient='records'):
        dataset.loc[dataset['original_id'] == c['Идентификатор пациента'], 'birthdate'] = c['Корректировка']

    # Merge regions
    regions = funKit.base_get(psq.getGeography)
    dataset = dataset.merge(regions, left_on=['Округ', 'Город'], right_on=['district', 'city'])

    dataset = common_steps.main(dataset, 1)

    return dataset


def prepare_invitro(patients : pd.DataFrame, datapoints : pd.DataFrame):

    dataset = patients.merge(datapoints, left_on='Id', right_on='Идентификатор пациента')

    # Select necessary columns
    dataset = dataset[['Идентификатор пациента', 'sex', 'bday', 'Дата исследования', 'Идентификатор теста', 'Результат', 'Идентификатор города']]

    # Unify column names
    dataset.rename(
        columns={
            'Идентификатор пациента': 'original_id',
            'Идентификатор теста': 'parameter_id',
            'Дата исследования': 'date',
            'Результат': 'value',
            'bday': 'birthdate',
        }, inplace=True)

    # Merge regions
    regions = funKit.base_get('SELECT * FROM region_name_mapping;')
    dataset = dataset.merge(regions, left_on="Идентификатор города", right_on="city_id")
     
    dataset = common_steps.main(dataset, 8)

    return dataset


def prepare_litech(dataset: pd.DataFrame):

    # Unpivot to long format
    dataset = dataset.melt(id_vars=['ИДЕНТИФИКАТОР', 'ДАТА', 'Пол', 'Возраст'], value_vars=psq.litechFeatures, var_name='parameter_id').dropna(subset=['value'])
    dataset['value'] = dataset['value'].map(lambda x: str(x).replace(',', '.')).astype('float', errors='ignore')

    # Unify column names
    dataset.rename(
        columns={
            'ИДЕНТИФИКАТОР': 'original_id',
            'Возраст': 'birthdate',
            'Результат': 'value',
            'ДАТА': 'date',
            'Пол': 'sex'
        }, inplace=True)

    # Litech center = Litech moscow
    dataset['city_id'] = 122
    dataset['district_id'] = 7
    dataset['region_id'] = 41

    dataset = common_steps.main(dataset, 2)

    return dataset

