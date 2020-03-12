import time,smbus2

i2c_ch = 1
i2c_address = 0x76

temp_msb = 0xFA
temp_lsb = 0xFB
temp_xlsb = 0xFC
temp_calibration_address = 0x88

press_msb = 0xF7
press_calibration_address = 0x8E

ctrl_meas = 0xF4



def set_mode_to_normal():
    bus.write_byte_data(i2c_address,ctrl_meas,0b00100111)
    time.sleep(1)

def get_celsius():
    return calculate_tmp()/100

def get_fahrenheit():
    return get_celsius() * 9/5 + 32

def calculate_tmp():
    return ((get_t_fine() * 5 + 128) >> 8 )

def get_t_fine():
    adc = read_tmp()
    var1 = ((((adc >> 3)-(t1 << 1)) * t2) >> 11)
    var2 = ((((adc >> 4) - t1) * ((adc >> 4) - t1)) >> 12) * (t3 >> 14)
    return var1 + var2 

def get_tmp_calibration():
    return read_calibration(temp_calibration_address,6)

def get_press_calibration():
    return read_calibration(press_calibration_address,18)

def read_calibration(start_address,amount):
    raw_vals = read_registers(start_address,amount)
    calc_vals = []
    for i in range(0,amount,2):
        cal = 0
        cal |= (raw_vals[i+1] << 8)
        cal |= raw_vals[i]
        if i == 0:
            cal %= 0xFFFF
        calc_vals.append(cal)
    return calc_vals


def read_tmp():
    return read_measurement(temp_msb)

def read_press():
    return read_measurement(press_msb)

def read_measurement(start_address):
    msb,lsb,xlsb = read_registers(start_address,3)
    meas = 0
    meas |= (msb << 12)
    meas |= (lsb << 4)
    meas |= (xlsb >> 4)
    return meas

def read_registers(start_address,amount):
    return bus.read_i2c_block_data(i2c_address, start_address, amount)

bus = smbus2.SMBus(i2c_ch)
time.sleep(1)
t1,t2,t3 = get_tmp_calibration()
press_calibs = get_press_calibration()
set_mode_to_normal()
