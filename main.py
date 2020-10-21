"""
This script is used to debug the files.

"""

import ukb_decoder as ukb_decoder
import itertools

fields = ukb_decoder.AllDataFields()
encodings = ukb_decoder.AllUKBDataCoding()

data_codings = set([x.coding for x in fields if x.value_type == "Categorical single"])
truly_categorical_single = ['7',
                             '339',
                             '620',
                             '7310',
                             '100015',
                             '502',
                             '100002',
                             '408',
                             '100014',
                             '1021',
                             '100012',
                             '616',
                             '871',
                             '100010',
                             '1022',
                             '503',
                             '100013',
                             '2730',
                             '548',
                             '950',
                             '913',
                             '1862',
                             '100003',
                             '100009',
                             '73',
                             '100016',
                             '100693',
                             '96',
                             '100007',
                             '100005',
                             '100017',
                             '100011',
                             '100006',
                             '1018',
                             '100008',
                             '100004',
                             '100001']

[[print(encoding) for encoding in encodings[x]] for x in data_codings if x in truly_categorical_single]

