import numpy as np
import matplotlib.pyplot as plt
import package_pulse as pp
import time
import package_pathWaveAndHvi as pwh
import package_allMsmtPulses as amp
import package_dataProcess as dp
from collections import OrderedDict
import json
import keysightSD1
import warnings
import keysight_hvi as kthvi
from AddOns.DigFPGAConfig_Demodulate import config_demodulator, config_weight_func, get_recommended_truncation
# with open(r"sysInfo.json") as file_:
#     info = json.load(file_)
triggerAwgDigDelay = 330 #info['sysConstants']['triggerAwgDigDelay']
pulse_general_dict = {'relaxingTime': 50, # float; precision: 0.01us; relax after the start of the firt pulse
                      'avgNum': 10000}

if __name__ == '__main__':

    pointPerCycle = 3000
    cycles = 10000
    start = time.time()
    FPGA_file = r'C:\PXI_FPGA\Projects\Demodulate_showWeight\Demodulate_showWeight.data\bin\Demodulate_showWeight_2020-12-24T21_59_37\Demodulate_showWeight.k7z'
    module_dict = pwh.openAndConfigAllModules(FPGA_file)

    WEIGHT_data = np.zeros(100 // 5, dtype=int) + 2 ** 13 - 1
    for i in range(1, 5):
        module_dict["D1"].instrument.DAQconfig(i, pointPerCycle, cycles, 0, 1)
        config_weight_func(module_dict["D1"].instrument, i, WEIGHT_data, 1, 100 // 5)
    config_demodulator(module_dict["D1"].instrument, [18, 18, 18, 18])

    W, Q, hvi = pwh.definePulseAndUpload(amp.driveAndMsmt, module_dict, pulse_general_dict)

    dataReceive = pwh.digReceiveData(module_dict['D1'], hvi, pointPerCycle, cycles, chan='0011', timeout=2000)
    pwh.releaseHviAndCloseModule(hvi, module_dict)

    # (demod_I, demod_Q, mag2) = dp.plotSingleCycle(dataReceive, 1, 180, weightAndTrig=1)

    sumRange_ = [1000, 4000]
    (demod_I, demod_Q, mag2) = dp.plotPreRrun(dataReceive, [1, 2], sumRange=sumRange_)
    print(get_recommended_truncation(dataReceive['1'][:, 0::5], dataReceive['1'][:, 1::5], sumRange_[0], sumRange_[1], 18))
    print(get_recommended_truncation(dataReceive['2'][:, 0::5], dataReceive['2'][:, 1::5], sumRange_[0], sumRange_[1], 18))

    plt.show()