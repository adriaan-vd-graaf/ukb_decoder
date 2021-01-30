from . data_fields import DataField, AllDataFields
import numpy as np
import pandas as pd
from . decoder import *

all_fields = AllDataFields()

# path, category, field_id, field, participants, items,
# stability, value_type, units, item_type, strata, sexed, instances,
# array, coding, notes, link

class AllPhenotypesPerField(DataField):
    def __init__(self, field_id: str, n_participants: int):
        this_field = all_fields[field_id]
        super().__init__(this_field.path, this_field.category, this_field.field_id, this_field.field,
                         this_field.participants, this_field.items, this_field.stability, this_field.value_type,
                         this_field.units, this_field.item_type, this_field.strata, this_field.sexed, this_field.instances,
                         this_field.array, this_field.coding, this_field.notes, this_field.link)

        self.instances = int(self.instances)
        self.array = int(self.array)

        if not self.value_type in {"Continuous", "Integer"}:
            raise ValueError(f'{self.item_type} is not implemented')

        self.n_participants = n_participants

        if self.value_type == "Continuous":
            self.dtype = float
        elif self.value_type == "Integer":
            self.dtype = int

        self.phenotype_matrix = np.zeros((self.n_participants, self.instances*self.array), dtype=self.dtype)
        self.phenotype_matrix[:, :] = np.nan

        self.phenotypes_added = np.zeros(self.instances*self.array, dtype=bool)

        self.decoder = Decoder()

    def add_phenotype_array(self, instance: int, array: int, phenotype_vector: list):
        if instance > self.instances:
            raise ValueError("Instance does not match the number of instances known to ukb_decoder")

        if array > self.array:
            raise ValueError("Array is larger than what is known to ukb_decoder")

        if len(phenotype_vector) != self.n_participants:
            raise ValueError(f"The phenotype vector does not have the same length ({len(phenotype_vector)}) as the number of participants provided ({self.n_participants})")

        #instance starts at 1 and array start at 0
        index = self._index(instance, array)
        self.phenotype_matrix[:, index] = self.decoder.decode_field(field_id=self.field_id, data_vector=phenotype_vector)

        self.phenotypes_added[index] =True


    def all_phenotypes_present(self):
        return np.all(self.phenotypes_added)


    def _index(self, instance, array):
        return (instance * array) + array


    def summary_stats_of_array(self, instance: int, array: int):
        
        index = self._index(instance, array)
        if not self.phenotypes_added[index]:
            raise ValueError("Did not add the phenotypes for this phenotype")         
            
        na_indices = np.isnan(self.phenotype_matrix[:,index])
        
        mean = np.mean(self.phenotype_matrix[~na_indices, index])
        std = np.std(self.phenotype_matrix[~na_indices, index])
        min = np.min(self.phenotype_matrix[~na_indices, index])
        max = np.max(self.phenotype_matrix[~na_indices, index])
        
        deciles = np.quantile(self.phenotype_matrix[~na_indices, index], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        decile_str = ', '.join([f'{x:.2e}' for x in deciles])
        combined_string = ""
        combined_string += f'{super.__str__(self)}, instance: {instance}, array: {array}\n'
        combined_string += f'   containing {self.n_participants} individuals, of which {np.sum(na_indices)} ({100*np.sum(na_indices)/self.n_participants:.1f}%) are nan valued\n'
        combined_string += f'   mean: {mean:.3e}, sd: {std:.3e}, range: [{min:.3e} - {max:.3e}]\n'
        combined_string += f'   deciles: [{decile_str}]'

        return combined_string


    def full_summary(self):
        full_string = ''
        i = 0
        for instance in  range(self.instances):
            for array in range(self.array):
                if self.phenotypes_added[i]:
                    full_string += self.summary_stats_of_array(instance, array)
            i += 1


    def apply_to_available_phenotypes(self, func1d, *args, **kwargs):
        """

        only works with scalar function output.

        :param func:
        :param args:
        :param kwargs:
        :return:
        """
        
        array = np.zeros(self.n_participants, dtype=float)
        for i in range(self.n_participants):
            array[i] = func1d(self.phenotype_matrix[i,~np.isnan(self.phenotype_matrix[i,:])], *args, **kwargs)

        return array


    def load_field_from_pandas(self, pandas_df: pd.DataFrame):
        if pandas_df.shape[0] != self.n_participants:
            raise ValueError(f"pandas df shape ({pandas_df.shape}) dif not match the number of participants: {self.n_participants}")

        colnames = [str(x) for x in pandas_df.columns]
        fields_instance_array = [
            (x.split("-")[0], x.split("-")[1].split('.')[0], x.split("-")[1].split('.')[1])
            for x in colnames if x != "eid"
        ]

        for field, instance, array in fields_instance_array:
            if field == self.field_id:
                self.add_phenotype_array(int(instance), int(array), pandas_df[f'{field}-{instance}.{array}'])


