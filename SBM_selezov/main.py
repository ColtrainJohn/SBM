## standart
import sys


## special


## This !
from . import funKit as fun
from . import prepare as prep


class Manager:

    def __init__(self, dataset, dataset_id, patients, load_to_pg_table, save_to):
        """
        dataset          : pd.DataFrame of laboratory parameter datapoints
        dataset_id       : int value of dataset from yuh_general_dataset
        patients         : default=False or pd.DataFrame of patients data in case of Invitro
        load_to_pg_table : True/False, define if should be loaded to Postgre yuh_general_datapoint
        save_to          : default=False or path + filename to save .csv result dataframe to
        """
        funDict = {
            1: prep.prepare_cmd,
            2: prep.prepare_litech,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: prep.prepare_invitro,
        }

        # This is for invitro if there is a patients file
        self.loading_table = funDict[dataset_id](dataset) if patients is False else funDict[dataset_id](dataset, patients)

        if load_to_pg_table:
            self.load_to_pg(load_to_pg_table)

        if save_to:
            self.loading_table.to_csv(save_to, sep=',')


    def load_to_pg(self, database):
        fun.put_to_pg(self.loading_table, database, index_label='id')


# Core function to import 
def main(dataset, dataset_id, patients=False, load_to_pg_table=False, save_to=False):
    Manager(dataset, dataset_id, patients, load_to_pg_table, save_to)


# To run from CLI pass filename and dataset id
if __name__ == "__main__":
    main(sys.argv[1:])
