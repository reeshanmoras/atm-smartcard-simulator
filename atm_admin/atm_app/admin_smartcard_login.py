# atm_app/admin_smartcard_login.py

from smartcard.System import readers
from atm_app.utils import pause
from atm_app.admin import admin_menu

# Admin Card ATR
ADMIN_SMARTCARD_ID = "3BFF1300FF10000031C173C8211064414D3137079000"


# READ ADMIN CARD ATR

def read_admin_card():
    r = readers()

    if len(r) == 0:
        return None

    reader = None
    for dev in r:
        if "Contacted" in str(dev):
            reader = dev
            break

    if reader is None:
        reader = r[0]

    try:
        conn = reader.createConnection()
        conn.connect()
    except:
        return None

    atr_hex = "".join(format(x, "02X") for x in conn.getATR())
    print("Admin Card ATR:", atr_hex)
    return atr_hex


# AUTO ADMIN CARD DETECTION
def auto_admin_card_check():
    atr = read_admin_card()

    if atr == ADMIN_SMARTCARD_ID:
        print("\n Admin Smart Card Detected — Auto Login Enabled!")
        pause()
        admin_menu()
        return True

    return False
