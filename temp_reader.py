import time,smbus2

i2c_ch = 1
i2c_address = 0x76

temp_msb = 0xFA
temp_lsb = 0xFB
temp_xlsb = 0xFC
temp_calibration_address = 0x88

press_msb = 0xF7

ctrl_meas = 0xF4



def set_mode_to_normal():
    bus.write_byte_data(i2c_address,ctrl_meas,0b00100011)
    time.sleep(1)

def get_celsius():
    return calculate_tmp()/100

def get_fahrenheit():
    return get_celsius() * 9/5 + 32

def calculate_tmp():
    adc = read_tmp()
    var1 = ((((adc >> 3)-(t1 << 1)) * t2) >> 11)
    var2 = ((((adc >> 4) - t1) * ((adc >> 4) - t1)) >> 12) * (t3 >> 14)
    t_fine = var1 + var2
    return ((t_fine * 5 + 128) >> 8 )

def read_calibration():
    calibration_vals = bus.read_i2c_block_data(i2c_address,temp_calibration_address,6)
    t1 = 0
    t1 |= (calibration_vals[1] << 8)
    t1 |= calibration_vals[0]
    t1 &= 0xFFFF
    t2 = 0
    t2 |= (calibration_vals[3] << 8)
    t2 |= calibration_vals[2]
    t3 = 0
    t3 |= (calibration_vals[5] << 8)
    t3 |= calibration_vals[4]
    return t1,t2,t3

def read_tmp():
    return read_measurement(temp_msb)

def read_measurement(start_address):
    msb,lsb,xlsb = read_registers(start_address)
    meas = 0
    meas |= (msb << 12)
    meas |= (lsb << 4)
    meas |= (xlsb >> 4)
    return meas

def read_registers(start_address):
    return bus.read_i2c_block_data(i2c_address, start_address, 3)

bus = smbus2.SMBus(i2c_ch)
time.sleep(1)
t1,t2,t3 = read_calibration()
set_mode_to_normal()
