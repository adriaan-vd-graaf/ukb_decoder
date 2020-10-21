import numpy as np
import copy
from . data_codings import *
from . data_fields import *

class decoder:

    def __init__(self):
        self.data_coding = data_codings.AllUKBDataCoding()
        self.data_fields = data_fields.AllDataFields()


        """
        Below are converting datapoints for categorical single datatypes
        """

        #these values will always be converted into nans.
        self.single_category_ordinal_nans = {
            -121: np.nan,    # Do not know
            -818: np.nan,    # prefer not to say
            -313: np.nan     # not applicable
        }

        self.codes_usable_as_ordinal_values = {
            96,       # liking of food in a scale from 1 to 8
            339,      # codes indicating being bothered by something, -600  to -602. -600 means not bothered
            408,      # Pain scale 0 - 10, 0 is No pain
            502,      # Yes 0, No  1
            503,      # Yes: 0, No 1,
            548,      # 0 - 10 agreement scale, 0 No agreement
            616,      # 0 - 10 happiness scale, 0 means very happy
            620,      # 0 - 10 distension scale, 0 means no distension
            871,      # 0 - 6, frequency scale, 0 means never, 6 means every day.
            913,      # 0 - 10, number of days with pain. 10 is 10 days of pain
            950,      # -500 to -504, Never to always scale. -504 is always
            1018,     # -600 to -602, Not bothered to bothered scale, -600 is bothered.
            1021,     # No 0, yes   1, scale
            1022,     # No 0, yes   1, scale
            100010,  # No 0, yes 1
            100013,  # No 0, yes 1
            100014,   # 5, 10, 15 size of portions, 5 is smaller than average
        }

        self.truly_categorical_single_categorical_values = {
            1862,  # ced diagnosis types.
            2730,  # speed of IBS symptoms
            7310,  # infection diagnosed along with IBS symptoms.
            100015, #type of milk consumed

        }

        self.decoder_to_ordinal = {
            100001:  {1: 1, 200: 2, 555: 0.5}, # recoding 2+ as 2
            100002:  {1: 1, 111: np.nan, 2: 2, 300: 3, 555: 0.5}, #recoding 3+ as 3
            100003: {1: 1, 111: np.nan, 2: 2, 300: 3, 555: 0.5}, # recoding 3+ as 3
            100004: {1: 1, 2: 2, 3: 3, 555: 0.5, 400: 4},
            100005: {1: 1, 2: 2, 3: 3, 4: 4, 500: 5, 555: 0.5, 444: 0.25},
            100006: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 600: 6, 555: 0.5},
            100007: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 600: 6},
            100008: {0: 0, 1: 1, 111:np.nan, 222:np.nan, 313:np.nan },
            100011: {0: 0, #this is time spent vigurous activity, taking the mean of a range, if it is given
                     10: 5, #taking mean of minutes
                     1030: 20,
                     12: 90,
                     24: 180,
                     3060: 45,
                     46: 300,
                     600: 360},
            100012: { #time, taking hours.
                0:0, 1:0.5, 1200:12, 13:2, 35:4, 57:6, 79:8, 912:10.5
            },
            100016: { # sausage intake, 0 is not encoded. So may have to revisit.
                np.nan: 0, 1:1, 2:2, 3:3, 4:4, 500: 5, 555:0.5
            },
            100017: {  # intake, 0 is not encoded. So may have to revisit how to perform that.
                np.nan: 0, 1: 1, 2: 2, 300: 3, 555: 0.5, 444: 0
            }
        }


        #these codes should not overlap.
        assert(len(self.codes_usable_as_ordinal_values & self.decoder_to_ordinal.keys()) == 0)
        assert(len(self.codes_usable_as_ordinal_values & self.truly_categorical_single_categorical_values) == 0)
        assert(len(self.decoder_to_ordinal.keys() & self.truly_categorical_single_categorical_values) == 0)

    def decode_field(self, field_id, data_vector = None, converter = None):

        if converter is not None:
            raise NotImplementedError

        field_of_interest = self.data_fields.data_field_by_id[field_id]
        value_type = field_of_interest.value_type

        if value_type == "Date":
            raise NotImplementedError
        elif value_type == 'Compound':
            raise NotImplementedError
        elif value_type == 'Time':
            raise NotImplementedError
        elif value_type == 'Categorical multiple':
            raise NotImplementedError
        elif value_type == 'Text':
            raise NotImplementedError
        elif value_type == 'Integer':
            converted_data = self._decode_integer(field_of_interest, data_vector, )
        elif value_type == 'Categorical single':
            converted_data = self._decode_categorical_single(field_of_interest, data_vector)
        elif value_type == 'Continuous':
            converted_data = self._decode_continuous(field_of_interest, data_vector)
        else:
            raise ValueError("Programming Error, Categories were not correcly encoded.")

        return converted_data


    def _decode_integer(self, field_of_interest, data_vector):
        '''
        All integer decoders were
        '''

        if field_of_interest.coding == '':
            return data_vector
        else:
            return self._decode_all_listed_codings_as_nan(field_of_interest, data_vector)


    def _decode_categorical_single(self, field_of_interest, data_vector):
        """
        Difficult to implement, a lot of data necessary.

        1. remove common na values using
        2. Determine if the data is categorical, or nominal#needs to be hard-coded.
            2.1 if categorical: return a matrix of dummy variables
            2.2 if nominal, convert if applicable and return a integer vector.

        return


        :param field_of_interest:
        :param data_vector:
        :return:
        """

        field_coding = int(field_of_interest.coding)

        tmp_data_vec = copy.copy(data_vector)
        #remove nans.
        tmp_data_vec = [x if x not in self.single_category_ordinal_nans else self.single_category_ordinal_nans[x] for x in tmp_data_vec]
        if field_of_interest.coding in self.truly_categorical_single_categorical_values:
            raise NotImplementedError("Have not implemented categorical values yet")

        elif field_coding in self.codes_usable_as_ordinal_values.union(set(self.decoder_to_ordinal.keys())):

            if field_coding in self.codes_usable_as_ordinal_values:
                return tmp_data_vec
            elif field_coding in self.decoder_to_ordinal.keys():
                for i, value in enumerate(tmp_data_vec):
                    if np.isnan(value):
                        continue #leave it as is.
                    elif value not in self.decoder_to_ordinal.keys():
                        print(f"Errors {field_of_interest.field_id} did not contain the value {value} in the "
                                         f"set: {self.decoder_to_ordinal[field_coding].keys()}")
                        raise ValueError("Incorrect value found, see above")

                    else:
                        tmp_data_vec[i] = self.decoder_to_ordinal[field_coding][value]

                return tmp_data_vec
            else:
                raise NotImplementedError("Programmer error, not implemented correctly")
        else:
            raise NotImplementedError(f"Field with coding {field_of_interest.coding} not found in translation dictionary. "
                                      f"Don't know what to do now")

    def _decode_continuous(self, field_of_interest, data_vector):
        """
        Will return a non-converted data vector.
        as of 15th of october 2020, there are a few codes with special values
        For now it will set them as na.

        :param field_of_interest: field number
        :param data_vector: data vector
        :return: data_ce
        """
        if field_of_interest.coding == '':
            return data_vector
        else:
            return self._decode_all_listed_codings_as_nan(field_of_interest, data_vector)

    def _decode_all_listed_codings_as_nan(self, field_of_interest, data_vector):
        """
        This will decode all listed codings as nan.

        :param field_of_interes:
        :param data_vector:
        :return:
        """
        listed_keys = self.data_coding[int(field_of_interest.coding)].code_values.keys()

        #setting all special values to nan.
        nan_values = set([float(x) for x in listed_keys])
        new_data = [x if x not in nan_values else np.nan for x in copy.copy(data_vector)]

        return new_data