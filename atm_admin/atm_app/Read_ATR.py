from smartcard.System import readers

r = readers()
connection = r[0].createConnection()
connection.connect()
atr = connection.getATR()

atr_hex="".join(f"{b:02X}" for b in atr)
print("Admin Card ATR:", atr_hex)
