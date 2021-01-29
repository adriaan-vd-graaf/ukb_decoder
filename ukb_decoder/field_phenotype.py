from . data_fields import DataField, AllDataFields
from . import decoder
import numpy as np


all_fields = AllDataFields()

class AllPhenotypesPerField(DataField):
    def __init__(self, field_id: str, n_participants: int):
        this_field = all_fields[field_id]
        super().__init__(self, this_field.path, this_field.category, this_field.field_id, this_field.field,
                         this_field.participants, this_field.items, this_field.stability, this_field.value_type,
                         this_field.units, this_field.item_type, this_field.strata, this_field.instances,
                         this_field.array, this_field.coding, this_field.notes, this_field.link)

        if not self.item_type in {"Continuous", "Integer"}:
            raise ValueError(f'{self.item_type} is not implemented')

        self.n_participants = n_participants

        if self.item_type == "Continuous":
            self.dtype = float
        elif self.item_type == "Integer":
            self.dtype = int

        self.phenotype_matrix = np.zeros((self.n_participants, self.instances*self.array), dtype=self.dtype)
        self.phenotype_matrix[:, :] = np.nan

        self.phenotypes_added = np.zeros(self.instances*self.array, dtype=bool)


    def add_phenotype_array(self, instance: int, array: int, phenotype_vector: list):
        if instance > self.instances:
            raise ValueError("Instance does not match the number of instances known to ukb_decoder")

        if array > self.array:
            raise ValueError("Array is larger than what is known to ukb_decoder")

        if len(phenotype_vector) != self.n_participants:
            raise ValueError(f"The phenotype vector does not have the same length ({len(phenotype_vector)}) as the number of participants provided ({self.n_participants})")

        #instance starts at 1 and array start at 0
        index = self._index(instance, array)
        self.phenotype_matrix[:, index] = decoder.decode_field(self.field_id, data_vector=phenotype_vector)

        self.phenotypes_added[index] =True


    def all_phenotypes_present(self):
        return np.all(self.phenotypes_added)


    def _index(self, instance, array):
        return (instance * array) + array


    def provide_vector_summary_statistics(self, instance: int, array: int):
        
        index = self._index(instance, array)
        if not self.phenotypes_added[index]:
            raise ValueError("Did not add the phenotypes for this phenotype")         
            
        na_indices = np.isnan(self.phenotype_matrix[:,index])
        
        mean = np.mean(self.phenotype_matrix[~na_indices, index])
        std = np.std(self.phenotype_matrix[~na_indices, index])
        min = np.min(self.phenotype_matrix[~na_indices, index])
        max = np.max(self.phenotype_matrix[~na_indices, index])
        
        deciles = np.quantile(self.phenotype_matrix[~na_indices, index], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        
        print(f'{super.__str__(self)}, instance: {instance}, array: {array}, containing {self.n_participants} individuals')
        print(f'mean: {mean:.3e}, sd: {std:.3e}, range: [{min:.3e} - {max:.3e}]')
        print(f'deciles: {deciles}')
