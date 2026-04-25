from flask import Flask, request
import requests

app = Flask(__name__)

# --- SETTINGS ---
PAYSTACK_TEST_KEY = "sk_test_YOUR_KEY_HERE" # Put your key from Paystack dashboard

def get_next_voucher():
    try:
        with open("vouchers.txt", "r") as f:
            lines = f.readlines()
        if not lines: return None
        voucher = lines[0].strip()
        with open("vouchers.txt", "w") as f:
            f.writelines(lines[1:])
        return voucher
    except: return None

@app.route('/ussd', methods=['POST'])
def ussd_logic():
    text = request.values.get("text", "")
    phone = request.values.get("phoneNumber")

    # LEVEL 0: Main Menu
    if text == "":
        res = "CON Welcome to Zone Data\n1. Buy 1GB (GHS 5)\n2. Buy 2GB (GHS 10)"
    
    # LEVEL 1: User chose 1GB
    elif text == "1":
        res = "CON Confirm 1GB for GHS 5?\n1. Yes, Pay Now\n2. Cancel"
    
    # LEVEL 2: User confirmed "Yes"
    elif text == "1*1":
        # This is where we simulate a successful transaction
        voucher = get_next_voucher()
        if voucher:
            res = f"END Payment Success!\nYour Code: {voucher}\nThank you for using Zone Data!"
        else:
            res = "END Sorry, we are out of stock. Please try later."
            
    else:
        res = "END Invalid choice. Please start again."
        
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

