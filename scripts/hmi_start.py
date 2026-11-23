import time
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1", port=502)
client.connect()

client.write_coil(2, True, device_id=1)          # FC5: RemoteStart = TRUE
print("Sent start command (RemoteStart=TRUE)\n")

for _ in range(8):
    regs  = client.read_holding_registers(0, count=2, device_id=1)
    coils = client.read_coils(0, count=3, device_id=1)
    level, setpoint = regs.registers
    pump, alarm = coils.bits[0], coils.bits[1]
    print(f"Level={level:3}  Setpoint={setpoint}  Pump={pump}  HighAlarm={alarm}")
    time.sleep(1)

client.close()
