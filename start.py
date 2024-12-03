import requests
import random
import string
import time
import subprocess

# Konfigurasi
ROUTER_IP = "192.168.0.1"
PASSWORD_CHANGE_URL = f"http://{ROUTER_IP}/boafrm/formWlEncrypt"
REBOOT_URL = f"http://{ROUTER_IP}/countDownPage.htm"  # Sesuaikan jika endpoint reboot berbeda
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "id,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": ROUTER_IP,
    "Origin": f"http://{ROUTER_IP}",
    "Referer": f"http://{ROUTER_IP}/wlbasic.htm",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

# Fungsi untuk membuat password acak
def generate_random_password(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Fungsi untuk mengganti password Wi-Fi
def change_wifi_password(new_password):
    payload = {
        "submit-url": "/wlbasic.htm",
        "SSID_Setting2": "1",
        "has_vwlan2": "",
        "wpaAuth2": "psk",
        "wpa11w2": "none",
        "wpa2EnableSHA2562": "disable",
        "ciphersuite2": "tkip",
        "wpa2ciphersuite2": "aes",
        "wps_clear_configure_by_reg2": "0",
        "wlan_disabled2": "0",
        "wlan_ssid2": "clone",  # Ganti dengan SSID Wi-Fi Anda
        "method2": "4",
        "stanums2": "32",
        "authType2": "open",
        "wepKeyLen2": "wep64",
        "wepEnabled2": "ON",
        "length2": "1",
        "format2": "1",
        "key2": "",
        "pskFormat2": "0",
        "pskValue2": new_password,
        "preAuth2": "",
        "radiusIP2": "",
        "radiusPort2": "1812",
        "radiusPass2": "",
        "use1x2": "OFF",
        "eapType2": "0",
        "eapInsideType2": "0",
        "eapUserId2": "",
        "radiusUserName2": "",
        "radiusUserPass2": "",
        "radiusUserCertPass2": "",
        "wl_access2": "0",
        "tx_restrict2": "0",
        "rx_restrict2": "0",
        "hiddenSSID2": "0",
        "sync_password2": "",
        "save_apply": "1",
    }

    response = requests.post(PASSWORD_CHANGE_URL, headers=HEADERS, data=payload, allow_redirects=False)
    if response.status_code == 302 and "countDownPage.htm" in response.headers.get("Location", ""):
        print(f"Password berhasil diubah menjadi: {new_password}")
        return True
    else:
        print(f"Gagal mengubah password. Status kode: {response.status_code}")
        return False

# Fungsi untuk merestart router
def reboot_router():
    response = requests.get(REBOOT_URL, headers=HEADERS)
    if response.status_code == 200:
        print("Router sedang direboot...")
        time.sleep(60)  # Tunggu 60 detik agar reboot selesai
    else:
        print(f"Gagal merestart router. Status kode: {response.status_code}")

def update_wifi_connection(new_password):
    try:
        # Panggil skrip bash untuk memperbarui koneksi Wi-Fi
        subprocess.run(["./update_wifi.sh", new_password], check=True)
        print("Berhasil memperbarui koneksi Wi-Fi di sistem.")
    except subprocess.CalledProcessError as e:
        print(f"Gagal memperbarui koneksi Wi-Fi: {e}")

# Main program
if __name__ == "__main__":
    while True:
        new_password = generate_random_password()
        if change_wifi_password(new_password):
            reboot_router()  # Restart router setelah password diubah
            update_wifi_connection(new_password)  # Hubungkan ke Wi-Fi baru
        
        # Tunggu 24 jam sebelum mengganti password lagi
        print("Menunggu 24 jam...")
        time.sleep(86400)  # 24 jam dalam detik
