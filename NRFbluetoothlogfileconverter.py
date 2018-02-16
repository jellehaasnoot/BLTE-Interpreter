# Used to convert NRF bluetooth hexadecimal numbers to binary numbers and use those to find the meaning of the
# used bluetooth code
import texttable
import matplotlib.pyplot as plt
from ValueConverter import ValueConverter
from LogReader import LogReader
from PopUp import PopUp

# Variables
functions_values = [False, False, False, False, False, False, False, False, False, False, False, False, False, False,
                    False, False]
functions_names = ['pedal_power_balance_present', 'pedal_power_balance_reference', 'accumulated_torque_present',
                   'accumulated_torque_source', 'wheel_revolution_data', 'crank_revolution_data',
                   'extreme_force_magnitudes_present', 'extreme_torque_magnitudes_present', 'extreme_angles_present',
                   'top_dead_spot_angle_present', 'bottom_dead_spot_angle_present', 'accumulated_energy_present',
                   'offset_compensation_indicator', 'reserved_1', 'reserved_2', 'reserved_3']


class Main:
    """
    his class will convert the data send by a cycling power management based sensor. (Assigned Number 0x2A63
    """
    def __init__(self, logfile):
        log_reader = LogReader(logfile)
        log_reader.extract_string('"(0x)')
        log_reader.extract_value('"(0x)')

        self.value_list = log_reader.value_list
        self.lines = log_reader.lines

        self.functions_present = []
        self.wheel_revolution_list = []
        self.wheel_event_time_list = []
        self.crank_revolution_list = []
        self.crank_event_time_list = []
        self.crank_rpm = []
        self.power_list = []
        self.speed = []
        self.rpm = []
        self.wheel_circumference = 2.132
        self.value_converter = ValueConverter()

    def identification(self):
        """
        This function will identify which sensors are present. So, it basically reads how many functions it needs
        to call to read the whole code
        """
        self.value_converter.hex_to_bin(self.input[:2])
        bin_code_first_octet = self.value_converter.binary

        self.value_converter.hex_to_bin(self.input[2:4])
        bin_code_second_octet = self.value_converter.binary

        # Bluetooth is hard to encrypt. The code below will make a readable binairy code for both the system and
        # operator.
        self.bin_code = list(reversed(bin_code_first_octet)) + list(reversed(bin_code_second_octet))

        for i in range(len(self.bin_code)):
            if self.bin_code[i] == 1:
                functions_values[i] = True     # The function is present
                self.functions_present.append(functions_names[i])
            else:
                functions_values[i] = False    # The function is not present

    def print_identification(self):
        """
        This is used to print the present functions, this is no necessary feature and therefore not part of the main
        identification function.
        """
        print('Functions present:')
        for i in range(len(self.functions_present)):
            print('* ' + self.functions_present[i])

    def data_processing(self):
        """
        This is used to process the data.
        """
        for i in range(len(self.value_list)):
            self.input = self.value_list[i]
            self.identification()
            self.value_reader()
        self.speed_calculation()
        self.rpm_calculation()
        # self.counter()        # TODO: Turn on when necessary


    def counter(self):
        """
        This function will count the presence of different functions. This will also give a table with the important
        values.
        """
        counter = []
        percentage = []
        for i in range(len(functions_names)):
            counter.append(self.functions_present.count(functions_names[i]))
            percentage.append(self.functions_present.count(functions_names[i])/len(self.value_list) * 100)

        table = texttable.Texttable()
        headings = ['Function', 'Counts', 'Percentage of total']
        table.header(headings)

        for row in zip(functions_names, counter, percentage):
            table.add_row(row)

        table_graphic = table.draw()
        pop_up = PopUp()
        pop_up.pop_up_normal("Table counter", table_graphic)

    def value_reader(self):
        """
        It will be clear after the identification which functions are present. The length of the output of the
        bluetooth sensor will be variable and adjust itself to the present functions.
        Each function will have there own number of hexadecimal characters. It is easy to decrypt the bluetooth signal
        with this in mind. The documentation can be found at: https://www.bluetooth.com/specifications/gatt/viewer?attri
        buteXmlFile=org.bluetooth.characteristic.cycling_power_measurement.xml
        """
        index = 4  # This is the index where the identification code stops

        # The power is given by the first 4 numbers after identification. This is mandatory and will therefore be
        # Always present in the bluetooth signal
        power_hexadecimal = self.input[index: index + 4]
        first_octet = self.value_converter.hex_to_bin(power_hexadecimal[:2])
        second_octet = self.value_converter.hex_to_bin(power_hexadecimal[2:4])

        power_binary = second_octet + first_octet
        power_decimal = self.value_converter.bin_to_dec(power_binary)
        self.power_list.append(power_decimal)
        index += 4

        # The remaining code is not mandatory and will therefore only be used if the function is present in the
        # identification. The calculations are based on the documentation on https://www.bluetooth.com/specifications/
        # gatt/viewer?attributeXmlFile=org.bluetooth.characteristic.cycling_power_measurement.xml. It is only
        # understandable if you know the bluetooth protocol
        if self.bin_code[0] == 1 or self.bin_code[1] == 1:
            index += 2
        if self.bin_code[2] == 1 or self.bin_code[3] == 1:
            index += 4
        if self.bin_code[4] == 1:
            wheel_revolutions_hexadecimal = self.input[index: index+8]
            first_octet = self.value_converter.hex_to_bin(wheel_revolutions_hexadecimal[:2])
            second_octet = self.value_converter.hex_to_bin(wheel_revolutions_hexadecimal[2:4])
            third_octet = self.value_converter.hex_to_bin(wheel_revolutions_hexadecimal[4:6])
            fourth_octet = self.value_converter.hex_to_bin(wheel_revolutions_hexadecimal[6:8])

            wheel_revolutions_binary = fourth_octet + third_octet + second_octet + first_octet
            wheel_revolutions_decimal = self.value_converter.bin_to_dec(wheel_revolutions_binary)
            self.wheel_revolution_list.append(wheel_revolutions_decimal)
            index += 8

            wheel_event_time = self.input[index: index+4]
            first_octet = self.value_converter.hex_to_bin(wheel_event_time[:2])
            second_octet = self.value_converter.hex_to_bin(wheel_event_time[2:4])
            wheel_event_time_binary = second_octet + first_octet
            wheel_event_time_decimal = self.value_converter.bin_to_dec(wheel_event_time_binary)/2048
            self.wheel_event_time_list.append(wheel_event_time_decimal)
            index += 4

        if self.bin_code[5] == 1:
            crank_revolutions_hexadecimal = self.input[index: index+4]
            first_octet = self.value_converter.hex_to_bin(crank_revolutions_hexadecimal[:2])
            second_octet = self.value_converter.hex_to_bin(crank_revolutions_hexadecimal[2:4])

            crank_revolutions_binary = second_octet + first_octet
            crank_revolutions_decimal = self.value_converter.bin_to_dec(crank_revolutions_binary)
            self.crank_revolution_list.append(crank_revolutions_decimal)
            index += 4

            crank_event_time = self.input[index: index+4]
            first_octet = self.value_converter.hex_to_bin(crank_event_time[:2])
            second_octet = self.value_converter.hex_to_bin(crank_event_time[2:4])

            crank_event_time_binary = second_octet + first_octet
            crank_event_time_decimal = self.value_converter.bin_to_dec(crank_event_time_binary)/1024
            self.crank_event_time_list.append(crank_event_time_decimal)
            index += 4

        if self.bin_code[6] == 1:
            index += 4
            index += 4
        if self.bin_code[7] == 1:
            index += 4
            index += 4
        if self.bin_code[8] == 1:
            index += 6
        if self.bin_code[9] == 1:
            index += 4
        if self.bin_code[10] == 1:
            index += 4
        if self.bin_code[11] == 1:
            index += 4

    def speed_calculation(self):
        """
        This function will calculate the rpm speed of the back wheel with the given information. It will also give the
        speed in m/s of the bicycle.
        """
        dt = []
        dr = []
        for m in range(len(self.wheel_event_time_list)-1):
            if self.wheel_event_time_list[m+1] < self.wheel_event_time_list[m]:
                dt.append(dt[m-1])
                dr.append(dr[m-1])
            else:
                dt.append(self.wheel_event_time_list[m+1] - self.wheel_event_time_list[m])
                dr.append(self.wheel_revolution_list[m+1] - self.wheel_revolution_list[m])

            if dt[m] == 0 or dr[m] == 0:
                pass
            else:
                self.rpm.append(dr[m]/dt[m]*60)

        for i in range(len(self.rpm)):
            self.speed.append(self.rpm[i]/60*self.wheel_circumference)

    def rpm_calculation(self):
        """
        This function will calculate the rpm speed of the cranks (the Cadance) with the given information.
        """
        dt = []
        dr = []
        for m in range(len(self.crank_event_time_list)-1):
            if self.crank_event_time_list[m+1] < self.crank_event_time_list[m]:
                dt.append(dt[m-1])
                dr.append(dr[m-1])
            else:
                dt.append(self.crank_event_time_list[m+1] - self.crank_event_time_list[m])
                dr.append(self.crank_revolution_list[m+1] - self.crank_revolution_list[m])

            if dt[m] == 0 or dr[m] == 0:
                pass
            else:
                self.crank_rpm.append(dr[m]/dt[m]*60)


data = Main('log.txt')
data.data_processing()
data2 = Main('log1.txt')
data2.data_processing()


fig = plt.figure(1, figsize=(20, 13))
plot1 = fig.add_subplot(1, 1, 1)
data.speed = [i * 3.6 for i in data.speed]
plot1.plot(data.speed)
plt.title("Speed (m/s)  [Power meter vs. Satori]")
if not data2.speed:
    factor = 1
else:
    factor = len(data.speed)/len(data2.speed)
x_coordinates_raw = range(0, len(data2.speed))
x_coordinates = [i * factor for i in x_coordinates_raw]
plot1.plot(x_coordinates, data2.speed)
plt.grid(b=True, which='major', color='b', linestyle='-')
plt.grid(b=True, which='minor', color='g', linestyle='--')
plt.minorticks_on()
plt.xticks([])

fig2 = plt.figure(2, figsize=(20, 13))
plot3 = fig2.add_subplot(1, 1, 1)
plot3.plot(data.crank_rpm)
plt.title("Crank speed (rpm)    [Power meter vs. Satori]")
if not data2.crank_rpm:
    factor = 1
else:
    factor = len(data.crank_rpm)/len(data2.crank_rpm)
x_coordinates_raw = range(0, len(data2.crank_rpm))
x_coordinates = [i * factor for i in x_coordinates_raw]
plot3.plot(x_coordinates, data2.crank_rpm)
plt.grid(b=True, which='major', color='b', linestyle='-')
plt.grid(b=True, which='minor', color='g', linestyle='--')
plt.minorticks_on()
plt.xticks([])

fig3 = plt.figure(3, figsize=(20, 13))
plot5 = fig3.add_subplot(1, 1, 1)
plot5.plot(data.power_list)
plt.title("Power (W)    [Power meter vs. Satori]")
if not data2.power_list:
    factor = 1
else:
    factor = len(data.power_list)/len(data2.power_list)
x_coordinates_raw = range(0, len(data2.power_list))
x_coordinates = [i * factor for i in x_coordinates_raw]
plot5.plot(x_coordinates, data2.power_list)
plt.grid(b=True, which='major', color='b', linestyle='-')
plt.grid(b=True, which='minor', color='g', linestyle='--')
plt.minorticks_on()
plt.xticks([])

print(data2.power_list)

plt.tight_layout()
plt.show()


