import serial
import time

def setup_serial(port='/dev/ttyACM0', baudrate=9600):
    """ Setup a connection to the specified serial port with given baud rate. """
    try:
        ser = serial.Serial(port, baudrate)
        print(f"Successfully connected to {port}.")
        return ser
    except serial.serialutil.SerialException as e:
        print(f"Failed to connect to {port}: {e}")
        return None

def read_from_serial(ser):
    """ Read one line from the serial port. """
    if not ser or not ser.is_open:
        print("Serial connection is not open.")
        return None

    try:
        # Wait for data to be available in the buffer
        while ser.in_waiting == 0:
            time.sleep(0.1)

        line = ser.readline().decode('utf-8').rstrip()
        return line
    except serial.serialutil.SerialException as e:
        print(f"Error reading from serial port: {e}")
        return None

def  write_to_serial(ser,char):
    if not set or not ser.is_open:
        print("error serial not present")
        return None

    ser.write(char.encode('utf-8'))
    ser.write(b'\r\n')

def check_for_data(ser):
    """ Check if there is data available to read on the serial port. """
    if not ser or not ser.is_open:
        print("Serial connection is not open.")
        return False

    return ser.in_waiting > 0

def setup_simon():
    ser = setup_serial()
    return ser

