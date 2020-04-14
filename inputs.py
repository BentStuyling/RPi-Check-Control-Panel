import Adafruit_ADS1x15


 # Create an ADS1015 ADC (12-bit) instance.
adc_1 = Adafruit_ADS1x15.ADS1115(address=0x48)
adc_2 = Adafruit_ADS1x15.ADS1115(address=0x49)
adc_3 = Adafruit_ADS1x15.ADS1115(address=0x4a)
# Create instances of sensors:
Vin = 5.25

class analog:
    """
    class with analog sensors
    """

    def __init__(self):
        self.value = None
        self.U = None
        self.R = None


    def OilTemp(self):
        """
        aa
        """
        # self.U = random.uniform(3,5)
        self.U = (4.096/32768)*adc_1.read_adc(1, gain=1)
        self.R = 330*((Vin/self.U)-1)
        if 1 < self.R < 24000:
            self.temp = (480608.65298) / \
                (1 + (self.R/(2.876073*10**-17))**0.1812132) - 96.85298
            self.value = round(self.temp, 2)
            if self.value > 80:
                global Warning
                Warning = 'High Oiltemp'
                print(Warning)
            return self.value
        else:
            self.value = "--"
            return self.value

    def OilPress(self):
        self.value = (((4.096/32768)*adc_1.read_adc(0, gain=1)-0.475)/4)*9
        if self.value <= 0.1:
            self.value = 0
        return self.value

    def FuelPress(self):
        # self.value = round(random.uniform(0,80)/10,1)
        self.value = abs(
            round((((4.096/32768)*adc_2.read_adc(3, gain=1)-0.475)/4)*9, 1))
        return self.value

    def ClntTemp(self):
        # self.U = random.uniform(3,4)
        self.U = (4.096/32768)*adc_1.read_adc(2, gain=1)
        self.R = 330*((Vin/self.U)-1)
        if 1 < self.R < 24000:
            self.temp = (211749.2077) / \
                (1 + (self.R/(1.274787*10**-14))**0.185661) - 113.7
            self.value = round(self.temp, 2)
            return self.value
        else:
            self.value = "--"
            return self.value

    def BatVolt(self):
        self.value = '{:.1f}'.format(round(adc_1.read_adc(
            3, gain=1)*(4.069/32768)*((3.3+1)/1)*1.022, 1))
        return self.value

    def DiffTemp(self):
        # self.U = random.uniform(0,4)
        self.U = (4.096/32768)*adc_2.read_adc(1, gain=1)
        self.R = 330*((Vin/self.U)-1)
        if 1 < self.R < 24000:
            self.temp = (480608.65298) / \
                (1 + (self.R/(2.876073*10**-17))**0.1812132) - 96.85298
            self.value = round(self.temp, 2)
            return self.value
        else:
            self.value = "--"
            return self.value

    def GetriebeTemp(self):
        # self.U = random.uniform(0,4)
        self.U = (4.096/32768)*adc_2.read_adc(2, gain=1)
        self.R = 330*((Vin/self.U)-1)
        if 1 < self.R < 24000:
            self.temp = (480608.65298) / \
                (1 + (self.R/(2.876073*10**-17))**0.1812132) - 96.85298
            self.value = round(self.temp, 2)
            return self.value
        else:
            self.value = "--"
            return self.value

    def AirPressure(self):
        self.data = bme280.sample(smbus2.SMBus(1), 0x76, calibration_params)
        # Pressure:
        self.value = round(self.data.pressure, 1)
        return self.value

    def ModuleTemp(self):
        self.data = bme280.sample(smbus2.SMBus(1), 0x76, calibration_params)
        # Temperature
        self.value = round(self.data.temperature, 1)
        return self.value

    def CPUTemp(self):
        self.process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
        self.output, self._error = self.process.communicate()
        self.outputstr = str(self.output)
        self.out = int(self.outputstr[self.outputstr.index(
            "=") + 1:self.outputstr.index(".")])
        return self.out

    def CPULoad(self):
        self.process = Popen('w', stdout=PIPE)
        self.output = self.process.communicate()
        self.outputstr = str(self.output)
        self.out = int((float(self.outputstr[self.outputstr.index(
            "average:") + 9:self.outputstr.index(",", self.outputstr.index("average:"))]))/(4.5/100))
        return self.out

    def OutsiteTemp(self):
        try:
            self.device_file = '/sys/bus/w1/devices/28-0114382f22aa/w1_slave'
            self.f = open(self.device_file, 'r')
            self.lines = self.f.readlines()
            self.f.close()

            while self.lines[0].strip()[-3:] != 'YES':
                # time.sleep(0.2)
                self.lines = read_temp_raw()
            self.equals_pos = self.lines[1].find('t=')
            if self.equals_pos != -1:
                self.temp_string = self.lines[1][self.equals_pos+2:]
                self.value = round(float(self.temp_string) / 1000.0, 1)
        except:
            self.value = 20
        return self.value



class ECU:
    """
    class with data from the ECU
    """

    def __init__(self):
        self.value = None
    
        def RPM(self):
            self.value = RPM_signl.frequency()*20
        if self.value <= 150:
            self.value = 0
        return self.value

    def Speed(self):
        Wheelcircumf = 1.930  # 195/60R15
        Correction = 0.98
        self.value = (SPD_signl.frequency()/9) * \
            Wheelcircumf*3.6*Correction  # km/h
        return self.value

    def FuelRate(self):
        self.f = FuelRate_signl.frequency()  # in Hz
        if self.f >= 1:
            self.pw = (1/self.f)*1000 - \
                (FuelRate_signl.pulse_width()-0.08)  # in ms
            self.value = (self.pw/1000)*self.f*0.1918*60*6  # L/hr
        else:
            self.value = 0.0

        # e34: 0 280 150 714 for Bosch injector in 535i 1989 to 1993
        # http://users.erols.com/srweiss/tableifc.htm#BOSCH
        # 191.8 cc/min at 3.0bar
        return self.value