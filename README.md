# SAIT-EMA
codes for retrieving data in the corpus SAIT-EMA

## How to initialise

```Python
from SAIT_EMA_Reader import SAIT_RawEMA_Reader

EMA_Reader = SAIT_RawEMA_Reader(raw_EMA_dir, speaker_name)
```

`raw_EMA_dir` is the absolute path of `pos` diretory of the current speaker `speaker_name`.

All possible speaker names: `F001`, `F002`, `F003`, `F004`, `F005`, `M001`, `M002`, `M003`, `M004`, `M005`, `A_M001`, `A_F001`, `L_F001`, `L_F002`, `L_F003`, `L_M001`, `L_M002`, `L_M003`.


## Glossary

The term `std_EMA` refers to a `numpy.ndarray` with the shape of `(num_frames, 12)`. 12 stands for the `x, y` coordinates of the six sensors: `tt, tb, td, lj, ul, ll`.

The term `nose_EMA` refers to a `numpy.ndarray` with the shape of `(num_frames, 2)`. It is the `x, y` coordinates of the `NOSE` sensor.