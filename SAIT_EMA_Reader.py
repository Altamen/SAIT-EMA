import random
import os

import numpy as np


class RawEMA_Reader():
    """
    Used to read raw EMA of a speaker from a certain dataset.
    It works at the directory containing raw EMA files.
    """
    def __init__(
            self,
            raw_EMA_dir,
            speaker_name
        ):
        self.raw_EMA_dir = raw_EMA_dir
        self.speaker_name = speaker_name

        self.raw_EMA_type = None  # raw EMA file extension name
        self.EMA_index_list = None  # all indices of raw EMA
        self.EMA_NUM = None  # total num of raw EMA
        self._setup_raw_EMA_list()  # set the values for the preceding 3 attributes

        self.raw_EMA_channels = None # dictionary containing info about: sensor_name - index
        self.raw_EMA_values = None  # list specifying orders of values of an EMA channel like: x, y, z, theta...
        self._setup_raw_EMA_channels_and_values()  # set the values for the preceding 3 attributes
    

    """
    Switching between paths and indices.
    """
    def _get_raw_EMA_index_from_path(self, raw_EMA_path):
        """
        Extracting index from raw EMA path.
        """
        file_name = os.path.basename(raw_EMA_path)
        index, _ = os.path.splitext(file_name)
        return index
    
    def _get_raw_EMA_path_from_index(self, index):
        """
        Building raw EMA path from its index.
        """
        raw_EMA_path = os.path.join(
            self.raw_EMA_dir,
            index + self.raw_EMA_type
        )
        return raw_EMA_path
    

    """
    Read a random EMA.
    """
    def _randn_index_generator(self):
        index = random.sample(self.EMA_index_list, 1)
        index = index[0]
        return index

    def _randn_raw_EMA_path_generator(self):
        index = self._randn_index_generator()
        raw_EMA_path = self._get_raw_EMA_path_from_index(index)
        return raw_EMA_path
    
    def get_randn_std_EMA(self):
        raw_EMA_path = self._randn_raw_EMA_path_generator()
        std_EMA = self.get_std_EMA(raw_EMA_path)
        return std_EMA
    

    """
    General Operations
    """
    def get_std_EMA_by_index(self, index):
        """
        通过 index 获取对应的 standard EMA
        """
        EMA_path = self._get_raw_EMA_path_from_index(index)
        std_EMA = self.get_std_EMA(EMA_path)
        return std_EMA
    
    def get_std_EMA_list_by_index_list(
            self, index_list=None
        ):
        """
        Returns the list containing all std_EMA accessible by "index_list".
        If "index_list" is None, return all std EMA accessible by self.EMA_index_list.

        Parameters
        ----------
        index_list : list
            List containing indices to be loaded.

        Returns
        -------
        std_EMA_list : list
            The elements of this list are all tuples: (index, std_EMA).
        """
        if index_list is None:
            index_list = self.EMA_index_list
        std_EMA_list = []
        for index in index_list:
            std_EMA = self.get_std_EMA_by_index(index)
            print(f"std_EMA {index} loaded")
            std_EMA_list.append((index, std_EMA))
        return std_EMA_list
    

    """
    Special Operations that should be implemented in subclasses.
    """
    def _setup_raw_EMA_list(self):
        """
        Used to set the values of:
            - self.raw_EMA_type  (file extension of raw EMA)
            - self.EMA_index_list  (list containing all indices of EMA)
            - self.EMA_NUM  (total num of raw EMA)
        """
        raise NotImplementedError

    def _setup_raw_EMA_channels_and_values(self):
        """
        Used to set the values of:
            - self.raw_EMA_channels
            - self.raw_EMA_values
        """
        raise NotImplementedError

    def _read_raw_EMA(self, raw_EMA_path):
        """
        Extracting basic EMA data from raw EMA file.
        """
        raise NotImplementedError

    def get_std_EMA(self, raw_EMA_path):
        """
        Returns std EMA (num_frames, 12) as numpy.ndarray.
        12 represents x, y channel of 6 sensors, they are:
            - tt, tb, td, li, ul, ll
        """
        raise NotImplementedError


class SAIT_RawEMA_Reader(RawEMA_Reader):
    def __init__(
            self,
            raw_EMA_dir,
            speaker_name
        ):

        # standard EMA channel index
        self.std_raw_EMA_channels = {
            'NOSE' : 1, 'LE' : 2, 'RE' : 3,
            'TD' : 4, 'TB' : 5, 'TT' : 6,
            'LJ' : 7, 'LL' : 8, 'UL' : 9
        }

        # which speakers have irregular channels
        self.speakers_with_normal_channels = [
            'F001', 'F002', 'F003', 'F004', 'F005',
            'M001', 'M002', 'M003', 'M004', 'M005',
            'L_M001', 'L_F001', 'L_F002', 'A_M001'
        ]
        self.speakers_with_irregular_channels = [
            'L_M002', 'L_M003', 'A_F001', 'L_F003'
        ]

        # irregular channels information
        self.L_M002_raw_EMA_channels = {
            'NOSE' : 11, 'LE' : 12, 'RE' : 13,
            'TD' : 14, 'TB' : 5, 'TT' : 6,
            'LJ' : 7, 'LL' : 8, 'UL' : 9
        }
        self.L_M003_raw_EMA_channels = self.L_M002_raw_EMA_channels
        self.A_F001_raw_EMA_channels = {
            'NOSE' : 11, 'LE' : 12, 'RE' : 13,
            'TD' : 14, 'TB' : 10, 'TT' : 16,
            "LJ" : 7, "LL" : 8, "UL" : 9
        }
        self.L_F003_raw_EMA_channels = {
            'NOSE' : 1, 'LE' : 5, 'RE' : 3,
            'TD' : 11, 'TB' : 10, 'TT' : 12,
            'LJ' : 7, 'LL' : 8, 'UL' : 9
        }

        super().__init__(
            raw_EMA_dir,
            speaker_name
        )


    """
    functions in parent class
    """
    def _setup_raw_EMA_list(self):
        self.raw_EMA_type = ".pos"
        self.EMA_NUM = 962

        dir_filelist = os.listdir(self.raw_EMA_dir)
        self.EMA_index_list = [os.path.splitext(x)[0] for x in dir_filelist \
                               if os.path.splitext(x)[-1] == self.raw_EMA_type]
        self.EMA_index_list = sorted(self.EMA_index_list)
        # only the first 962 data were chosen because the rest data were for palate
        self.EMA_index_list = self.EMA_index_list[: self.EMA_NUM]
    
    def _setup_raw_EMA_channels_and_values(self):
        self.raw_EMA_values = [
            'x', 'y', 'z',
            'phi', 'theta', 'rms', 'extra'
        ]

        # choose the mapping between channels and indices according to speaker_name
        if self.speaker_name not in self.speakers_with_normal_channels and \
                self.speaker_name not in self.speakers_with_irregular_channels:
            raise ValueError("speaker {} does not exit".format(self.speaker_name))
        
        if self.speaker_name in self.speakers_with_normal_channels:
            self.raw_EMA_channels = self.std_raw_EMA_channels
        elif self.speaker_name == 'L_M002':
            self.raw_EMA_channels = self.L_M002_raw_EMA_channels
        elif self.speaker_name == 'L_M003':
            self.raw_EMA_channels = self.L_M003_raw_EMA_channels
        elif self.speaker_name == 'A_F001':
            self.raw_EMA_channels = self.A_F001_raw_EMA_channels
        elif self.speaker_name == 'L_F003':
            self.raw_EMA_channels = self.L_F003_raw_EMA_channels
    
    def _read_raw_EMA(self, raw_EMA_path):
        """
        the file contains a header

        the EMA data part, is a 1d numpy array
            - 16 channels
            - 7 values for each channel: x, y, z, phi, theta, rms, extra
        """
        header_size = self._get_header_size(raw_EMA_path)

        EMA_data = np.fromfile(
            raw_EMA_path,
            np.float32,
            offset=header_size
        ) # EMA_data 此时为一维 numpy 数组

        EMA_data = EMA_data.reshape((-1, 112))
        """
        the shape of the ultimate EMA_data is (num_frams, 112)

        the meaning of 112:
            - 16 * 7 = 112
                - 16 stands for 16 channels
                - 7 stands for the 7 values of each channel: x, y, z, phi, theta, rms, extra
        """
        return EMA_data
    
    def get_std_EMA(self, raw_EMA_path):
        """
        get standard EMA (numpy ndarray) from the absolute path of .pos file

        standard EMA (num_frames, 12), 12 stands for the x, y coordinates of the six sensors:
            - tt, tb, td, lj, ul, ll
        """

        EMA_data = self._read_raw_EMA(raw_EMA_path)

        tt_x = EMA_data[:, self._get_channel_value_index('TT', 'x')]
        tt_z = EMA_data[:, self._get_channel_value_index('TT', 'z')]
        tb_x = EMA_data[:, self._get_channel_value_index('TB', 'x')]
        tb_z = EMA_data[:, self._get_channel_value_index('TB', 'z')]
        td_x = EMA_data[:, self._get_channel_value_index('TD', 'x')]
        td_z = EMA_data[:, self._get_channel_value_index('TD', 'z')]

        lj_x = EMA_data[:, self._get_channel_value_index('LJ', 'x')]
        lj_z = EMA_data[:, self._get_channel_value_index('LJ', 'z')]
        ul_x = EMA_data[:, self._get_channel_value_index('UL', 'x')]
        ul_z = EMA_data[:, self._get_channel_value_index('UL', 'z')]
        ll_x = EMA_data[:, self._get_channel_value_index('LL', 'x')]
        ll_z = EMA_data[:, self._get_channel_value_index('LL', 'z')]

        stacked_channels = np.vstack((
            tt_x, tt_z, tb_x, tb_z, td_x, td_z,
            lj_x, lj_z, ul_x, ul_z, ll_x, ll_z
        ))
        stacked_channels = stacked_channels.T

        return stacked_channels
    

    """
    Tools
    """
    def _get_header_size(self, raw_EMA_path):
        """
        get the size of header of the .pos file
        """
        with open(raw_EMA_path, 'rb') as EMA_file:
            # counting the bytes of header
            counter = 0
            for line in EMA_file:
                counter += 1
                if counter == 2: # the second line of the header indicates how many bytes the header has
                    header_size = line.decode('latin-1').strip("\n")
                    header_size = int(header_size)
                    break
        return header_size
    
    def _get_channel_value_index(self, sensor, value):
        sensor_index = self.raw_EMA_channels[sensor] - 1
        value_index = self.raw_EMA_values.index(value)

        channel_index = sensor_index * 7 + value_index
        return channel_index
    
    # handling header files
    def print_header(self, raw_EMA_path):
        with open(raw_EMA_path, 'rb') as EMA_file:
            # counting the bytes of header
            counter = 0
            for line in EMA_file:
                line = line.decode('latin-1').strip("\n")
                print(line)
                counter += 1
                if counter == 14:
                    break
    
    # getting nose EMA
    def get_nose_EMA_by_path(self, raw_EMA_path):
        EMA_data = self._read_raw_EMA(raw_EMA_path)

        nose_x = EMA_data[:, self._get_channel_value_index('NOSE', 'x')]
        nose_z = EMA_data[:, self._get_channel_value_index('NOSE', 'z')]

        stacked_channels = np.vstack((
            nose_x, nose_z
        ))
        stacked_channels = stacked_channels.T

        return stacked_channels
    
    def get_nose_EMA_by_index(self, index):
        raw_EMA_path = self._get_raw_EMA_path_from_index(index)
        nose_EMA = self.get_nose_EMA_by_path(raw_EMA_path)
        return nose_EMA
    
    def get_nose_EMA_list_by_index_list(self, index_list=None):
        """
        Returns a list containing (index, nose_EMA) accessible by index_list.
        If index_list is None, change it to self.EMA_index_list.

        Returns
        -------
        nose_EMA_list : list
            The elements of this list are all tuples: (index, nose_EMA).
            Shape of "nose_EMA": (num_frames, 2).
        """
        if not index_list:
            index_list = self.EMA_index_list
        nose_EMA_list = []
        for index in index_list:
            nose_EMA = self.get_nose_EMA_by_index(index)
            nose_EMA_list.append((index, nose_EMA))
        return nose_EMA_list