# Jemuran-Pintar
Jemuran ini dapat bergerak menggunakan servo. Indikator yang menggerakkan servo diambil dari sensor dht dan photoresistor. Sensor tersebut akan mengirim data ke esp-32,  servo akan bergerak sesuai kondisi yang terpenuhi.


# Menjalankan Program
1. Buka NGROK dan masukkan perintah "ngrok tcp 1883".
2. Buka CMD lalu buka path mqtt dan jalankan perintah "mosquitto_sub -t Jemuran".
3. Di rangkaian wokwi dan juga kode python, ubah port sesuai dengan NGROK.
4. Jalankan file python.
5. Jalankan wokwi.

# Stress Test
