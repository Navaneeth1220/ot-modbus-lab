PROGRAM prog0
  VAR
    Level       AT %QW0   : INT;   (* tank level 0-100, read via FC3 *)
    Setpoint    AT %QW1   : INT;   (* high-level stop point (parameter) *)
    Pump        AT %QX0.0 : BOOL;  (* pump output, read via FC1 *)
    HighAlarm   AT %QX0.1 : BOOL;  (* high-level alarm output *)
    RemoteStart AT %QX0.2 : BOOL;  (* run command - operator writable *)
  END_VAR
  VAR
    Init : BOOL := TRUE;
  END_VAR

  IF Init THEN
    Setpoint := 80;
    Init := FALSE;
  END_IF;

  Pump := RemoteStart AND (Level < Setpoint);

  IF Pump THEN
    Level := Level + 2;
  ELSIF Level > 0 THEN
    Level := Level - 1;
  END_IF;

  IF Level > 100 THEN Level := 100; END_IF;

  HighAlarm := Level >= Setpoint;
END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#100ms, PRIORITY := 0);
    PROGRAM instance0 WITH task0 : prog0;
  END_RESOURCE
END_CONFIGURATION
