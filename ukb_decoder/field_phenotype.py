from . data_fields import DataField, AllDataFields
import numpy as np
import pandas as pd
from . decoder import *
import icd10
import datetime
from collections import defaultdict

all_fields = AllDataFields()

# path, category, field_id, field, participants, items,
# stability, value_type, units, item_type, strata, sexed, instances,
# array, coding, notes, link

class PhenotypesPerField(DataField):
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

        self.last_joined_phenotype = None

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
        return (instance * (self.array)) + array


    def apply_func_to_pheno_mat(self, func1d, rm_nas=True, *args, **kwargs):
        """

        only works with scalar function output.
        will output a na value if there is no phenotype present.

        if rm_nas = False, the function needs to accept a full vector of na values.

        :param func:
        :param rm_nas:
        :param args:
        :param kwargs:
        :return:
        """

        array = np.zeros(self.n_participants, dtype=float)
        for i in range(self.n_participants):

            if rm_nas:
                nas = np.isnan(self.phenotype_matrix[i,:])

                if nas.shape[0] == 0:
                    array[i] = np.nan
                else:
                    array[i] = func1d(self.phenotype_matrix[i, ~nas], *args, **kwargs)
            else:
                array[i] = func1d(self.phenotype_matrix[i, :], *args, **kwargs)

        self.last_joined_phenotype=array

        return array


    def load_from_pd_df(self, pandas_df: pd.DataFrame):
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



    def summary_stats_of_array(self, instance: int, array: int):

        index = self._index(instance, array)
        if not self.phenotypes_added[index]:
            raise ValueError("Did not add the phenotypes for this phenotype")

        na_indices = np.isnan(self.phenotype_matrix[:, index])

        mean = np.mean(self.phenotype_matrix[~na_indices, index])
        std = np.std(self.phenotype_matrix[~na_indices, index])
        min = np.min(self.phenotype_matrix[~na_indices, index])
        max = np.max(self.phenotype_matrix[~na_indices, index])

        deciles = np.quantile(self.phenotype_matrix[~na_indices, index], [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        decile_str = ', '.join([f'{x:.2e}' for x in deciles])
        combined_string = ""
        combined_string += f'{super.__str__(self)}, instance: {instance}, array: {array}\n'
        combined_string += f'   containing {self.n_participants} individuals, of which {np.sum(na_indices)} ({100 * np.sum(na_indices) / self.n_participants:.1f}%) are nan valued\n'
        combined_string += f'   mean: {mean:.3e}, sd: {std:.3e}, range: [{min:.3e} - {max:.3e}]\n'
        combined_string += f'   deciles: [{decile_str}]'

        return combined_string


    def full_summary(self):
        full_string = ''
        i = 0
        for instance in range(self.instances):
            for array in range(self.array):
                if self.phenotypes_added[i]:
                    full_string += self.summary_stats_of_array(instance, array)
                i += 1

        return full_string

    @property
    def joined_phenotypes(self):
        if self.last_joined_phenotype is not None:
            return self.last_joined_phenotype
        else:
            raise ValueError("Please set the joined phenotype by applying")



class UKBICD10Pheno(PhenotypesPerField):
    def __init__(self, n_participants: int):

        this_field = all_fields['41270'] #all ICD10 diagnoses
        DataField.__init__(self, this_field.path, this_field.category, this_field.field_id, this_field.field,
                           this_field.participants, this_field.items, this_field.stability, this_field.value_type,
                           this_field.units, this_field.item_type, this_field.strata, this_field.sexed,
                           this_field.instances, this_field.array, this_field.coding, this_field.notes, this_field.link)

        self.dates_of_diagnosis_field = all_fields['41280']


        self.instances = int(self.instances)
        self.array = int(self.array)

        self.n_participants = n_participants

        self.phenotypes_added = np.zeros(self.instances * self.array, dtype=bool)

        self.last_joined_phenotype = None

        """
        Each individual is provided a dictionary that contains the ICD10 code as keys, and the months since birth date for the diagnosis as the value.
        """
        self.indice_and_diagnoses = {i : {} for i in range(self.n_participants)}

        self.indice_and_birthdates = {}

        self.diagnoses_count = defaultdict(int)


    def _identify_month_year_of_birth(self, pandas_df: pd.DataFrame):
        month_col = '52-0.0'
        year_col = '34-0.0'

        months_dat = pandas_df[month_col].astype(str).tolist()
        year_dat = pandas_df[year_col].astype(str).tolist()

        # Unknown what the day of birth is, so hard-coded to 1.

        birthdates = {i: datetime.date(year=int(float(year_dat[i])), month=int(float(months_dat[i])), day=1) for i in
                      range(self.n_participants) if year_dat[i] != 'nan' and months_dat[i] != 'nan'}

        return birthdates


    def _add_instance_to_diagnoses(self, instance: int, array: int,
                                   diagnosis_series: pd.DataFrame,
                                   date_of_diagnosis_series: pd.DataFrame, month_year_of_birth: dict):

        diagnosis_list = diagnosis_series.astype(str).tolist() #this makes the nan values a string of 'nan'
        date_list = [str(x).split('-') for x in date_of_diagnosis_series.astype(str).tolist()]
        date_list = [datetime.date(year=int(x[0]), month=int(x[1]), day=int(x[2])) if x[0] != 'nan' else 'nan' for x in date_list]
        days_since_diagnosis = [(x - month_year_of_birth[i]).days
                                if (x != 'nan' and month_year_of_birth[i] != 'nan') else 'nan'
                                for i, x in enumerate(date_list)]
        
        for i in range(self.n_participants):
            if diagnosis_list[i] == 'nan':
                if days_since_diagnosis[i] != 'nan':
                    raise ValueError(f"Programmer or data error, encountered a diagnosis nan, with a non nan date, on line {i}")
                continue

            else:
                if days_since_diagnosis[i] == 'nan':
                    raise ValueError(f"Programmer or data error, encountered a date nan with a diagnosis on line {i}")

                self.indice_and_diagnoses[i][diagnosis_list[i]] = days_since_diagnosis[i]
                self.diagnoses_count[diagnosis_list[i]] += 1

        self.phenotypes_added[self._index(instance, array)] = True


    def load_from_pandas_array(self, pandas_df):

        if pandas_df.shape[0] != self.n_participants:
            raise ValueError(f"pandas df shape ({pandas_df.shape}) dif not match the number of participants: {self.n_participants}")

        month_year_of_birth = self._identify_month_year_of_birth(pandas_df)

        colnames = [str(x) for x in pandas_df.columns]

        fields_instance_array = [
            (x.split("-")[0], x.split("-")[1].split('.')[0], x.split("-")[1].split('.')[1])
            for x in colnames if x != "eid"
        ]

        for field, instance, array in fields_instance_array:
            if field == self.field_id:
                self._add_instance_to_diagnoses(int(instance), int(array),
                                         pandas_df[f'{field}-{instance}.{array}'],
                                         pandas_df[f'{self.dates_of_diagnosis_field.field_id}-{instance}.{array}'],
                                         month_year_of_birth
                                         )



    def add_phenotype_array(self, instance: int, array: int, phenotype_vector: list):
        raise NotImplementedError()

    def load_from_pd_df(self, pandas_df: pd.DataFrame):
        raise NotImplementedError()

    def apply_func_to_pheno_mat(self, func1d, rm_nas=True, *args, **kwargs):
        raise NotImplementedError()

    def summary_stats_of_array(self, indice, array):
        raise NotImplementedError()

    @property
    def joined_phenotypes(self):
        raise NotImplementedError()
