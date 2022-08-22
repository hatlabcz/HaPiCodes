import yaml
import numpy as np
import matplotlib.pyplot as plt
import h5py
from HaPiCodes.test_examples import basicMsmtPulses as bmp
from HaPiCodes.data_process import fittingAndDataProcess as f
from HaPiCodes.pathwave.pxi_instruments import PXI_Instruments
from HaPiCodes.test_examples import msmtInfoSel
from HaPiCodes.data_process import postSelectionProcess as psdp

def piPulseTuneUp(yamlFile=msmtInfoSel.cwYaml, ampArray=np.linspace(-0.9, 0.9, 100), plot=1, update=0,sel=False):
    msmtInfoDict = yaml.safe_load(open(yamlFile, 'r'))
    f.yamlFile = yamlFile
    pxi = PXI_Instruments(msmtInfoDict, reloadFPGA=True)
    WQ = bmp.BasicExperiments(pxi.module_dict, msmtInfoDict, subbuffer_used=pxi.subbuffer_used)
    W, Q = WQ.piPulseTuneUp(ampArray)
    pxi.autoConfigAllDAQ(W, Q)
    pxi.uploadPulseAndQueue()
    dataReceive = pxi.runExperiment(timeout=20000)
    pxi.releaseHviAndCloseModule()
    IQdata = f.processDataReceiveWithRef(pxi.subbuffer_used, dataReceive, plot=1)
    Id, Qd = f.average_data(IQdata.I_rot, IQdata.Q_rot)
    piPulseAmp = f.pi_pulse_tune_up(Id, Qd, updatePiPusle_amp=update, plot=plot)

    if
    selData = psdp.PostSelectionData(Id, Qd, msmtInfoDict, [1, 0, 0], plotGauFitting=0)
    selMask = selData.mask_g_by_circle(sel_idx=0, plot=0)
    I_vld, Q_vld = selData.sel_data(selMask, plot=0)

    return (W, Q, dataReceive, Id, Qd, piPulseAmp)

if __name__ == '__main__':
    msmt = piPulseTuneUp()
