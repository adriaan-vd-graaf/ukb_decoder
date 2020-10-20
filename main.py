import ukb_decoder as ukb_decoder
import itertools

fields = ukb_decoder.AllDataFields()
encodings = ukb_decoder.AllUKBDataCoding()

data_codings = set([x.coding for x in fields if x.value_type == "Integer"])
[[print(encoding) for encoding in encodings[x]] for x in data_codings if x != ""]

# all_meanings = set(itertools.chain(*[[x.meaning for x in y.code_values.values() if len(y.code_values) < 10] for y in encodings.data_codings.values()]))
# for meaning in all_meanings:
#     print(meaning)
# print(len(all_meanings))
#
#
# field_of_interest = fields.data_field_by_id['1289']
#
#
# converter = ukb_decoder.quantitative_converter(field_of_interest,
#                                                encodings,
#                                                [-10, -10, -3, -3, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8])