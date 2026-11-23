# OT Modbus Lab: Attack, Detection & IEC 62443 Gap Assessment

A self-contained lab that builds a soft PLC, attacks it over Modbus TCP, captures and detects the attack, and assesses the result against IEC 62443-3-3 and MITRE ATT&CK for ICS. A hands-on OT/ICS security portfolio project.

> **Isolated lab only.** Everything runs inside a single Kali VM on a private Docker network. Nothing here touches a real device, a production network, or the internet.

## The arc

A soft PLC runs a simulated tank-fill process and exposes its I/O over Modbus TCP. Acting first as a legitimate HMI and then as an attacker, the lab issues unauthenticated Modbus writes that force a pump and overwrite a safety setpoint, defeating the high-level alarm with no authentication required. The traffic is captured in Wireshark, detected with a Suricata rule, and the weaknesses are mapped to specific 62443 system requirements and ATT&CK for ICS techniques.

## Architecture


All components run in one Kali VM on a flat Docker network (`otlab`):

| Host | Role | Address |
| --- | --- | --- |
| OpenPLC (soft PLC) | tank-fill process, Modbus server | 172.30.0.10:502 |
| HMI (pymodbus) | legitimate reads (FC1/FC3) | 172.30.0.50 |
| Rogue (pymodbus) | unauthorized writes (FC5/FC6) | 172.30.0.66 |
| Wireshark + Suricata | capture and detect on the bridge | n/a |

## Repository layout

| Path | Contents |
| --- | --- |
| `plc/tank_fill.st` | OpenPLC Structured Text program |
| `scripts/hmi_read.py` | read holding registers and coils (FC1/FC3) |
| `scripts/hmi_start.py` | start the pump via a coil write (FC5) |
| `scripts/attack_setpoint.py` | overwrite the setpoint via a register write (FC6) |
| `detection/ot.rules` | Suricata rule: Modbus write from a non-HMI source |
| `detection/fast.log` | the alert the rule produced |
| `captures/` | Wireshark captures of the attack |
| `screenshots/` | Wireshark evidence frames |
| [docs/defence-writeup.pdf](docs/defence-writeup.pdf) | full attack, detection and 62443 gap assessment |

## Quick start

Prerequisites: Docker, Python 3 with `pymodbus`, Wireshark, Suricata.

1. Build and run the PLC:

   ```bash
   git clone https://github.com/thiagoralves/OpenPLC_v3.git
   cd OpenPLC_v3 && docker build -t openplc:v3 .
   docker run -d --name openplc-v3 --privileged -p 8080:8080 -p 502:502 openplc:v3
   ```

   Open `http://localhost:8080` (login `openplc`/`openplc`, then change it), upload `plc/tank_fill.st`, launch it, and click **Start PLC**.

2. Run the HMI and attack scripts from the host (they target `127.0.0.1:502`, the PLC's published port):

   ```bash
   python scripts/hmi_read.py        # read status
   python scripts/hmi_start.py       # force the pump on (FC5)
   python scripts/attack_setpoint.py # overwrite the setpoint to 9999 (FC6)
   ```

3. Detection. Put a separate "rogue" host on an isolated network so the rule can tell sources apart, capture the bridge while the write runs, then:

   ```bash
   suricata -r captures/modbus_detect.pcap -S detection/ot.rules -l . -k none
   cat fast.log
   ```

See [docs/defence-writeup.pdf](docs/defence-writeup.pdf) for the full method.

## Findings (IEC 62443-3-3)

One zone, target SL 2, achieved approximately SL 1. The gap:

| SR | Requirement | Status |
| --- | --- | --- |
| SR 1.2 | Software process and device identification and authentication | Unmet |
| SR 2.1 | Authorization enforcement | Unmet |
| SR 5.1 | Network segmentation | Unmet |
| SR 5.2 | Zone boundary protection | Unmet |
| SR 6.2 | Continuous monitoring | Implemented |

**ATT&CK for ICS:** Command Message (T1692.001) and Modify Parameter (T0836), both under Impair Process Control (TA0106).

## Key takeaway

On Modbus, network reachability is authority. The protocol provides no identity, authorization, or integrity, and the device cannot fix that. Security comes from the network layer: segmentation to control who can reach the controller, and monitoring to catch what gets through.
