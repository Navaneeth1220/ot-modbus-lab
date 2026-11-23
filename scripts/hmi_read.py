from pymodbus.client import ModbusTcpClient

PLC = "127.0.0.1"          # OpenPLC container, port 502 published to host
client = ModbusTcpClient(PLC, port=502)
client.connect()

coils = client.read_coils(0, count=10, device_id=1)          # FC1
regs  = client.read_holding_registers(0, count=10, device_id=1)  # FC3

if coils.isError() or regs.isError():
    print("Read error — try device_id=0:", coils, regs)
else:
    print("Coils 0-9   :", coils.bits[:10])
    print("Holding 0-9 :", regs.registers)

client.close()
