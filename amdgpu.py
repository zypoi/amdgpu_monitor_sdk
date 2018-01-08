import sys
import os
import re


class PermissionError(Exception):
    pass


class GPUError(Exception):
    pass


class amdgpu:

    _Temperature = 0
    _CoreClock = 0
    _MemoryClock = 0
    _CoreWatt = 0.0
    _MemoryWatt = 0.0
    _maxWatt = 0.0
    _averageWatt = 0.0
    _load = 0
    path = ''

    _dict_regexp = {
        'gputemp': r'(?<=GPU Temperature: ).*(?= C)',
        'gpuload': r'(?<=GPU Load: ).*(?= %)',
        'coreclock':  r'\d*(?= MHz \(SCLK\))',
        'memclock':  r'\d*(?= MHz \(MCLK\))',
        'vddc': r'[0-9.]*(?= W \(VDDC\))',
        'vddci': r'[0-9.]*(?= W \(VDDCI\))',
        'maxwatt': r'[0-9.]*(?= W \(max GPU\))',
        'avgwatt': r'[0-9.]*(?= W \(average GPU\))'
    }

    def __init__(self, num):
        self.path = '/sys/kernel/debug/dri/{}/amdgpu_pm_info'.format(num)
        if os.path.exists(self.path):
            try:
                self.update_info()
            except:
                raise PermissionError
        else:
            raise GPUError

    def get_temperature(self):
        self.update_info()
        return self._Temperature

    def get_core_clock(self):
        self.update_info()
        return self._CoreClock

    def get_mem_clock(self):
        self.update_info()
        return self._MemoryClock

    def get_core_watt(self):
        self.update_info()
        return self._CoreWatt

    def get_mem_watt(self):
        self.update_info()
        return self._MemoryWatt

    def get_max_watt(self):
        self.update_info()
        return self._maxWatt

    def get_avg_watt(self):
        self.update_info()
        return self._averageWatt

    def _reg_search_pattern(self,reg_pattern, str_match):
        searchobj = re.search(pattern=reg_pattern, string=str_match, flags=re.M | re.I)
        if searchobj:
            return searchobj.group()
        else:
            return None

    def update_info(self):
        f = open(self.path)
        lines = f.readlines()
        for line in lines:
            for reg in self._dict_regexp:
                value = self._reg_search_pattern(self._dict_regexp[reg], line)
                if not value is None:
                    if reg == 'gputemp':
                        self._Temperature = int(value)
                    elif reg == 'gpuload':
                        self._load = int(value)
                    elif reg == 'coreclock':
                        self._CoreClock = int(value)
                    elif reg == 'memclock':
                        self._MemoryClock = int(value)
                    elif reg == 'vddc':
                        self._CoreWatt = float(value)
                    elif reg == 'vddci':
                        self._MemoryWatt = float(value)
                    elif reg == 'maxwatt':
                        self._maxWatt = float(value)
                    elif reg == 'avgwatt':
                        self._averageWatt = float(value)
