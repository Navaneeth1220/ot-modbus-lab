# OT Modbus Lab - progress
Done: steps 1-6 (PLC + process, HMI reads, FC5/FC6 attack, Wireshark capture, Suricata detection working)
Artifacts: modbus_attack.pcap, modbus_detect.pcap, ot.rules, logs/fast.log, hmi_read.py, hmi_start.py, attack_setpoint.py
PLC: openplc-v3 @172.30.0.10 (web 8080) | HMI: attacker @172.30.0.50 | Rogue: rogue @172.30.0.66 | net: otlab
TODO: step 7 defence write-up (IEC 62443 + MITRE ATT&CK ICS), GitHub repo, LinkedIn post
Note: containers stop on reboot -> `docker start openplc-v3 attacker rogue` then Start PLC in web UI
