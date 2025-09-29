# SAIT-EMA
codes for retrieving data in the corpus SAIT-EMA

## How to initialise

```Python
from SAIT_EMA_Reader import SAIT_RawEMA_Reader

EMA_Reader = SAIT_RawEMA_Reader(raw_EMA_dir, speaker_name)
```

`raw_EMA_dir` is the absolute path of `pos` diretory (caution, not the `rawpos` directory) of the current speaker `speaker_name`.

All possible speaker names: `F001, F002, F003, F004, F005, M001, M002, M003, M004, M005, A_M001, A_F001, L_F001, L_F002, L_F003, L_M001, L_M002, L_M003`.


## Glossary

The term `std_EMA` refers to a `numpy.ndarray` with the shape of `(num_frames, 12)`. 12 stands for the `x, y` coordinates of the six sensors: `tt, tb, td, lj, ul, ll`.
Each speaker has exactly 962 `std_EMA`s.

The term `nose_EMA` refers to a `numpy.ndarray` with the shape of `(num_frames, 2)`. It is the `x, y` coordinates of the `NOSE` sensor.

The term "index" refers to the filename without extension. For example, for the file `0001.pos`, its index is `0001`. An "index list" is a Python list whose elements are all indices. For example, `["0001", "0002", "0900"]` is an index list.


## How to use

### For extracting `std_EMA`:

Extracting `std_EMA` by providing the absolute path of the `.pos` file.
```Python
std_EMA = EMA_Reader.get_std_EMA(path)
```

Extracting `std_EMA` by providing its index.
```Python
std_EMA = EMA_Reader.get_std_EMA_by_index(index)
```

Get a list of `std_EMA` by providing the corresponding index list.
If index list is `None`, return a list containing all `std_EMA` of the current speaker.
```Python
std_EMA_list = EMA_Reader.get_std_EMA_list_by_index_list(index_list)
```

Get a random `std_EMA`.
```Python
std_EMA = EMA_Reader.get_randn_std_EMA()
```


### For extracting `nose_EMA`

Extracting `nose_EMA` by providing the absolute path of the `.pos` file.
```Python
nose_EMA = EMA_Reader.get_nose_EMA_by_path(path)
```

Extracting `nose_EMA` by providing its index.
```Python
nose_EMA = EMA_Reader.get_nose_EMA_by_index(index)
```

Get a list of `nose_EMA` by providing the corresponding index list.
If index list is `None`, return a list containing all `nose_EMA` of the current speaker.
```Python
nose_EMA_list = EMA_Reader.get_nose_EMA_list_by_index_list(index_list)
```