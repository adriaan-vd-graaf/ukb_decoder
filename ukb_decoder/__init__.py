import numpy as np
import copy
from . data_codings import *
from . data_fields import *

class decoder:
    def __init__(self):
        self.data_coding = data_codings.AllUKBDataCoding()
        self.data_fields = data_fields.AllDataFields()

    def decode_field(self, field_id, data_vector = None):

        field_of_interest = self.data_fields.data_fields[field_id]
        category = field_of_interest.category

        if category == "Date":
            raise NotImplementedError
        elif category == 'Compound':
            raise NotImplementedError
        elif category == 'Time':
            raise NotImplementedError
        elif category == 'Categorical multiple':
            raise NotImplementedError
        elif category == 'Text':
            raise NotImplementedError
        elif category == 'Integer':
            raise NotImplementedError
        elif category == 'Categorical single':
            converted_data = self._decode_categorical_single(field_of_interest, data_vector)
        elif category == 'Continuous':
            converted_data = self._decode_continuous(field_of_interest, data_vector)
        else:
            raise ValueError("Programming Error, Categories were not correcly encoded.")

        return converted_data


    def _decode_integer(self, field_of_interest, data_vector):
        '''
        Listed below are the codepoints that are relevant in the encoding.

        6361 - 0, meaning: b'Did not make any correct matches'
        100373 - -1, meaning: b'Do not know'
        100373 - -10, meaning: b'Less than one'
        100373 - -3, meaning: b'Prefer not to answer'
        100306 - -1, meaning: b'Do not know'
        100306 - -2, meaning: b'Never went to school'
        100306 - -3, meaning: b'Prefer not to answer'
        100300 - -1, meaning: b'Do not know'
        100300 - -10, meaning: b'Less than one mile'
        100300 - -3, meaning: b'Prefer not to answer'
        946 - -1001, meaning: b'Less than one cigarette per day'
        946 - -818, meaning: b'Prefer not to answer'
        946 - 0, meaning: b'No cigarettes, only smoke cigars or pipes'
        957 - -313, meaning: b'Do not work'
        957 - -777, meaning: b'Given up work because of IBS'
        957 - -818, meaning: b'Prefer not to answer'
        100291 - -1, meaning: b'Do not know'
        100291 - -3, meaning: b'Prefer not to answer'
        513 - -121, meaning: b'Do not know'
        513 - -818, meaning: b'Prefer not to answer'
        100298 - -1, meaning: b'Do not know'
        100298 - -10, meaning: b'Less than once a week'
        100298 - -3, meaning: b'Prefer not to answer'
        100569 - -1, meaning: b'Do not know'
        100569 - -10, meaning: b'Less than a year ago'
        100569 - -3, meaning: b'Prefer not to answer'
        17 - -1, meaning: b'Next button not pressed'
        517 - -999, meaning: b'All my life / as long as I can remember'
        42 - -313, meaning: b'Not applicable'
        42 - -818, meaning: b'Prefer not to answer'
        100355 - -1, meaning: b'Do not know'
        100355 - -10, meaning: b'Less than one a day'
        100355 - -3, meaning: b'Prefer not to answer'
        37 - -1, meaning: b'Time uncertain/unknown'
        37 - -3, meaning: b'Preferred not to answer'
        100585 - -1, meaning: b'Do not know'
        100585 - -2, meaning: b'Only had twins'
        100585 - -3, meaning: b'Prefer not to answer'
        511 - -818, meaning: b'Prefer not to answer'
        511 - -999, meaning: b'Too many to count / One episode ran into the next'
        218 - 99, meaning: b'Not known'
        402 - 0, meaning: b'Test not completed'
        100504 - -1, meaning: b'Do not know'
        100504 - -2, meaning: b'Never had sex'
        100504 - -3, meaning: b'Prefer not to answer'
        100698 - -313, meaning: b'Ongoing when data entered'
        485 - -1, meaning: b'Invalid timing recorded'
        100567 - -1, meaning: b'Do not know'
        100567 - -10, meaning: b'Less than 1 year ago'
        100567 - -3, meaning: b'Prefer not to answer'
        528 - -121, meaning: b'Do not know'
        528 - -818, meaning: b'Prefer not to answer'
        528 - -999, meaning: b'Too many to count'
        584 - -818, meaning: b'Prefer not to answer'
        100595 - -1, meaning: b'Do not know'
        100595 - -11, meaning: b'Still taking the pill'
        100595 - -3, meaning: b'Prefer not to answer'
        170 - -1, meaning: b'Location could not be mapped'
        100290 - -1, meaning: b'Do not know'
        100290 - -10, meaning: b'Less than a year'
        100290 - -3, meaning: b'Prefer not to answer'
        100537 - -1, meaning: b'Do not know'
        100537 - -10, meaning: b'Less than once a year'
        100537 - -3, meaning: b'Prefer not to answer'
        100582 - -1, meaning: b'Do not know'
        100582 - -3, meaning: b'Prefer not to answer'
        100582 - -6, meaning: b'Irregular cycle'
        100598 - -1, meaning: b'Do not know'
        100598 - -11, meaning: b'Still taking HRT'
        100598 - -3, meaning: b'Prefer not to answer'
        487 - -1, meaning: b'More than a month'
        100586 - -3, meaning: b'Prefer not to answer'
        100586 - -4, meaning: b'Do not remember'
        100353 - -1, meaning: b'Do not know'
        100353 - -10, meaning: b'Less than one a day'
        525 - -121, meaning: b'Do not know'
        525 - -818, meaning: b'Prefer not to answer'
        530 - -121, meaning: b'Do not know'
        530 - -818, meaning: b'Prefer not to answer'
        530 - -999, meaning: b'As long as I can remember'
        100329 - -1, meaning: b'Do not know'
        100329 - -10, meaning: b'Less than an hour a day'
        100329 - -3, meaning: b'Prefer not to answer'
        100584 - -3, meaning: b'Prefer not to answer'
        1990 - 0, meaning: b'Trail not completed'
        100696 - -1, meaning: b'Abandoned'
        100307 - -1, meaning: b'Do not know'
        100307 - -2, meaning: b'Unable to walk'
        100307 - -3, meaning: b'Prefer not to answer

        '''

        return self._decode_all_listed_codings_as_nan(field_of_interest, data_vector)

    def _decode_categorical_single(self, field_of_interest, data_vector):
        raise NotImplementedError


    def _decode_continuous(self, field_of_interest, data_vector):
        """
        Will return a non-converted data vector.
        as of 15th of october 2020, there are a few codes with special values
        For now it will set them as na.

        :param field_of_interest: field number
        :param data_vector: data vector
        :return: data_ce
        """
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