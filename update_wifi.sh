#!/bin/bash

SSID="clone"  # Ganti dengan nama SSID Anda
PASSWORD="$1"  # Password baru sebagai argumen

# Perbarui koneksi Wi-Fi menggunakan nmcli
nmcli dev wifi connect "$SSID" password "$PASSWORD" || {
    echo "Gagal menghubungkan ke Wi-Fi dengan SSID $SSID"
    exit 1
}

echo "Berhasil terhubung ke Wi-Fi $SSID dengan password baru."
