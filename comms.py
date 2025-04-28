import pyvisa
import numpy as np

rm = pyvisa.ResourceManager()

def getInstruments():
    devices = {}
    
    for resource in rm.list_resources():
        try:
            with rm.open_resource(resource) as inst:
                idn = inst.query('*IDN?').strip()
                devices[resource] = idn
                inst.close()
        except Exception:
            devices[resource] = "VISA Device (No IDN)"

    return devices

def printDevice(selectBox, index):
    device = selectBox.itemData(index)
    name = selectBox.currentText()
    box = selectBox.objectName()
    print(f'Box: {box}, Name: {name}, Device: {device}')

def setWaveform(inst, func):
    try:
        inst.write(f'FUNC {func}')
        print(f"Current function: {inst.query('FUNC?').strip()}")
    except Exception as e:
        print(f'Error setting waveform: {e}')

def setFrequency(inst, freq):
    try:
        inst.write(f'FREQ {freq}')
        print(f"Current frequency: {np.float64(inst.query('FREQ?')):.4f} Hz")
    except Exception as e:
        print(f'Error setting frequency: {e}')

def setPeriod(inst, per):
    try:
        inst.write(f'FREQ {1/per}')
        print(f"Current period: {1/np.float64(inst.query('FREQ?')):.4f} s")
    except Exception as e:
        print(f'Error setting period: {e}')
    
def setVoltage(inst, fgen_name, volt):
    try:
        inst.write('VOLT:UNIT VPP')
        inst.write('VOLT:OFFS 0V')
        inst.write('OUTP:LOAD INF')
        inst.write(f'VOLT {volt}')
        volt_read = np.float64(inst.query('VOLT?').strip())
        volt_unit = inst.query('VOLT:UNIT?').strip()
        offset = np.float64(inst.query('VOLT:OFFS?'))
        load = inst.query('OUTP:LOAD?').strip()
        if volt_read == volt:
            print(f"Current voltage: {volt_read:.4f} {volt_unit}")
        else:
            print(f"Error setting voltage for {fgen_name} to {volt}: {volt_read}")
        if offset == 0.0:
            print(f"Current DC offset: {offset:.4f} V")
        else:
            print(f"Error resetting offset for {fgen_name}")
        print(f"Current load: {load} Ohm")
    except Exception as e:
        print(f'Error setting voltage parameters: {e}')

def getVoltageFuncGen(inst):
    try:
        if inst is None:
            print("Error getting voltage: No instrument defined!")
            return None
        volt_read = np.float64(inst.query('VOLT?'))
        return volt_read
    except Exception as e:
        print(f'Error getting voltage from {inst}: {e}')
        return None

def getVoltage(inst):
    try:
        if inst is None:
            print("Error getting voltage: No instrument defined!")
            return None
        volt_read = np.float64(inst.query('READ?'))
        return volt_read
    except Exception as e:
        print(f'Error getting voltage from {inst}: {e}')
        return None

def resetWaveform(inst, phase=0):
    inst.write("BURS:STAT ON")   # Enable burst mode
    inst.write("BURS:NCYC 1")    # One cycle per trigger
    inst.write("BURS:MODE TRIG") # Set burst mode to triggered
    inst.write(f"BURS:PHAS {phase}")    # Set phase to 0 degrees (reset wave start point)
    inst.write("TRIG:SOUR IMM")  # Set trigger source to immediate

def outputSignal(inst, fgen_name, outp=True):
    if outp:
        if np.int32(inst.query('*OPC?')) == 1:
            print(f"Instrument {fgen_name} ready.")
    
        inst.write('OUTP ON') # Enable output
        inst.write("TRIG")
        inst.write("BURS:STAT OFF")
        print(f"Output on for {fgen_name}")
    else:
        inst.write('OUTP OFF') # Disable output
        print(f"Output off for {fgen_name}")

