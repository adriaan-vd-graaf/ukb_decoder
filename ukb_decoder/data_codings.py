
class AllUKBDataCoding:
    def __init__(self):
        self.data_codings = {}
        with open('/'.join(__file__.split('/')[:-1]) + '/resources/2020_10_15_ukb_codings.tsv', 'rb') as f:
            f.readline() #header
            for line in f:
                code, value, meaning = line[:-1].split(b'\t')
                value = value.decode('utf8')
                code = int(float(code))

                #initialize if it hadden't happened already
                if code not in self.data_codings.keys():
                    self.data_codings[code] = UKBDataCoding(code)

                self.data_codings[code].add_code_point(value, meaning)

    def code_value_meaning(self, code, value):
        return self.data_codings[code].meaning_of_value(value)

    def __getitem__(self, item):
        return self.data_codings[int(item)]

class UKBDataCoding:
    def __init__(self, coding):
        self.coding = coding
        self.code_values = {}

    def add_code_point(self, value, meaning):
        if value in self.code_values.keys():
            self.code_values[value].meaning += b"\nOr: " + meaning #sometimes, this occurs multiple times.

        else:
            self.code_values[value] = UKBDataCodingValue(self.coding, value, meaning)

    def __str__(self):
        return f'UKBDataCoding containing {len(self.code_values)} code values'

    def meaning_of_value(self, value):
        return self.code_values[value].meaning

    def __iter__(self):
        self._values_to_iterate_over = list(self.code_values.keys())
        self._iter_indice = 0
        return self

    def __next__(self):
        if self._iter_indice < len(self._values_to_iterate_over):
            self._iter_indice += 1
            return self.code_values[self._values_to_iterate_over[self._iter_indice - 1]]
        else:
            raise StopIteration

class UKBDataCodingValue:
    def __init__(self, parent, value, meaning):
        self.parent = parent
        self.value = value
        self.meaning = meaning.replace(b'\r', b'')

    def __str__(self):
        return f'UKBDataCodingPoint, CODE {self.parent} - {self.value}, meaning: {self.meaning}'

    def __repr__(self):
        return self.__str__()