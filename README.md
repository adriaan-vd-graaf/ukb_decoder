# `ukb_decoder`

**Currently untested, only use if you're confident in debugging python code**

This is a package that is designed for personal use to decode ukb phenotypes as they come from the ukb resources.

Right now it can be difficult to know what all the values are from a UKB phenotype file, therefore you can decode your 
phenotype field using this package. 

```
import numpy as np
import ukb_decoder

data_field_id = 2897 #Age Stopped Smoking
# This data field has 2 special values:
# -1, meaning: b'Do not know'
# -3, meaning: b'Prefer not to answer'

data_vector = [28, np.nan, -1, np.nan, -3, 58]
decoder = ukb_decoder()
decoded_vector = ukb_decoder.decode(data_field_id, data_vector)

decoded_vector
# [28, np.nan, np.nan, np.nan, np.nan, 58]
```

The package  is mainly written so that a vector from the UKB phenotype files (not included in this package) can be 
converted into a vector that can be used for association analysis.
This package only contains publicly available data that was retrieved from the UKB data resource.
The package does not contain any data that is subject to a data access agreement.

 
