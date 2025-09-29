# SAIT-EMA
codes for retrieving data in the corpus SAIT-EMA

## How to use it

```Python
from SAIT_EMA_Reader import SAIT_RawEMA_Reader

EMA_Reader = SAIT_RawEMA_Reader(raw_EMA_dir, speaker_name)
```

`raw_EMA_dir` is the absolute path of `pos` diretory of the current speaker `speaker_name`.