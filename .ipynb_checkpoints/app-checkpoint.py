from flask import Flask, render_template, request, jsonify
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
import json

app = Flask(__name__)

# Global Modbus client
modbus_client = None

# Store device information
devices = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save-config', methods=['POST'])
def save_config():
    global modbus_client
    try:
        data = request.get_json()
        port = data['port']
        baudrate = int(data['baudrate'])
        parity = data['parity']
        stop_bits = int(data['stopBits'])
        byte_size = int(data['byteSize'])
        modbus_client = ModbusClient(method='rtu', port=port, baudrate=baudrate, parity=parity, stopbits=stop_bits, bytesize=byte_size)
        return jsonify({'success': True, 'message': 'Configuration Saved'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error saving configuration: {e}'})

@app.route('/connect-modbus', methods=['POST'])
def connect_modbus():
    global modbus_client
    if modbus_client:
        try:
            if modbus_client.connect():
                return jsonify({'success': True, 'message': 'Successfully connected to Modbus'})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to Modbus'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Connection Error: {e}'})
    else:
        return jsonify({'success': False, 'message': 'Configuration not set'})

# Other routes and functionalities remain the same

if __name__ == '__main__':
    app.run(debug=True)