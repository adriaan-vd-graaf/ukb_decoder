from collections import defaultdict

class AllDataFields:
    def __init__(self):
        self.data_fields = []
        self.data_field_by_id = {}

        with open('/'.join(__file__.split('/')[:-1]) + "/resources/2020_10_15_data_dictionary_showcase.tsv", 'r') as f:
            f.readline() #header
            for line in f:
                tmp_data_field = DataField(*line.split("\t"))
                self.data_fields.append(tmp_data_field)
                self.data_field_by_id[tmp_data_field.field_id] = tmp_data_field

        self.all_paths = {x.path for x in self.data_fields}
        self.all_categories = {x.category for x in self.data_fields}
        self.all_field_ids = {x.field_id for x in self.data_fields}
        self.all_fields = {x.field for x in self.data_fields}
        self.all_units = {x.units for x in self.data_fields}
        self.all_item_types = {x.item_type for x in self.data_fields}
        self.all_item_types = {x.value_type for x in self.data_fields}
        self.all_strata = {x.strata for x in self.data_fields}
        self.all_instances = {x.instances for x in self.data_fields}
        self.all_codings = {x.coding for x in self.data_fields}


    def __str__(self):
        return f'all datafields object, containing {len(self.data_fields)} fields'


    def __getitem__(self, item):
        return self.data_field_by_id[item]


    def __iter__(self):
        self._iteration_indice = 0
        return self


    def __next__(self):
        if self._iteration_indice >= len(self.data_fields):
            raise StopIteration
        else:
            self._iteration_indice += 1
            return self.data_fields[self._iteration_indice -1]


class DataField:
    def __init__(self, path, category, field_id, field, participants, items,
                 stability, value_type, units, item_type, strata, sexed, instances,
                 array, coding, notes, link):
        self.path = path
        self.category = category
        self.field_id = field_id
        self.field = field
        self.participants = participants
        self.items = items
        self.stability = stability
        self.value_type = value_type
        self.units = units
        self.item_type = item_type
        self.strata = strata
        self.sexed = sexed
        self.instances = instances
        self.array = array
        self.coding = coding
        self.notes = notes
        self.link = link

    def __str__(self):
        return f'{self.field_id}: {self.field}'

    def __repr__(self):
        return f'{self.__class__.__name__} class representing: {self.field_id}: {self.field}'


