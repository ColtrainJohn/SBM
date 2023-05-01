## standart
import uuid


## special
import pandas as pd


## This !
from . import funKit
from . import psq




def translate_parameter_names(dataset, dataset_id):

    # Read paramter mapping table
    tab = funKit.base_get(psq.paramMapper.format(dataset_id=dataset_id))

    # Для инвитро (датасет 8) параметры мапятся через айдишники
    row =  "id_in_lab" if dataset_id == 8 else "name_in_lab"

    # Map parameter ID codes
    dataset['parameter_id'] = dataset['parameter_id'].map(
        dict((name, code) for name, code in zip(tab[row], tab['parameter_id']))
        )

    # Add dataset ID code
    dataset['dataset_id'] = dataset_id

    return dataset


def common_fix(dataset):

    # Fix value symbols
    dataset['value'] = dataset['value'].astype('str')\
        .str.replace(' ', '')\
            .replace('>', '')\
            .replace('<', '')
    
    # Value type
    dataset['value'] = pd.to_numeric(dataset['value'], errors='coerce')

    # Encode gender
    dataset['sex'] = dataset['sex'].map(lambda x: -1 if isinstance(x, float) else 0 if x.lower().startswith('м') else 1 if x.lower().startswith('ж') else -1)

    # Process dates
    dataset['date'] = pd.to_datetime(dataset['date'], errors='coerce')
    dataset['birthdate'] = pd.to_datetime(dataset['birthdate'], errors='coerce')

    # Calculate age
    dataset['age'] = (dataset['date'] - dataset['birthdate']) / pd.Timedelta('365 days')

    # Filter NAs
    # TODO expand for all approrpriate columns
    dataset.dropna(subset=['birthdate', 'value', 'date'], inplace=True)

    return dataset


def add_ids(tab):

    # TODO rewrite it more compact

    # Patients UUIDs
    pat_unique_cols = ['original_id', 'sex', 'birthdate']
    patients = tab[pat_unique_cols].drop_duplicates(keep='first').copy()
    patients['patient_uuid'] = [uuid.uuid4() for _ in range(len(patients.index))]

    # Create datapoints
    tab = patients.merge(tab, left_on=pat_unique_cols, right_on=pat_unique_cols)

    # Observations UUIDs
    obs_unique_cols = ['patient_uuid', 'date']
    observations = tab[obs_unique_cols].drop_duplicates(keep='first').copy()
    observations['observation_uuid'] = [uuid.uuid4() for _ in range(len(observations.index))]

    # Add new uuids
    tab = observations.merge(tab, left_on=obs_unique_cols, right_on=obs_unique_cols)
    tab['datapoint_uuid'] = [uuid.uuid4() for _ in range(len(tab.index))]

    return tab


def main(dataset, dataset_id):
    
    dataset = translate_parameter_names(dataset, dataset_id)
    dataset = common_fix(dataset)
    dataset = add_ids(dataset)

    return dataset[psq.datapointColumns]
