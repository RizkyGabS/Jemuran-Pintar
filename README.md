# Jemuran-Pintar
Jemuran ini dapat bergerak menggunakan servo. Indikator yang menggerakkan servo diambil dari sensor dht dan photoresistor. Sensor tersebut akan mengirim data ke esp-32,  servo akan bergerak sesuai kondisi yang terpenuhi.


# Menjalankan Program
1. Buka NGROK dan masukkan perintah "ngrok tcp 1883".
2. Buka CMD lalu buka path mqtt dan jalankan perintah "mosquitto_sub -t Jemuran".
3. Di rangkaian wokwi dan juga kode python, ubah port sesuai dengan NGROK.
4. Jalankan file python.
5. Jalankan wokwi.

# Stress Test
1. Download/duplicate project "https://github.com/inovex/mqtt-stresser".
2. Install Golang "https://go.dev/dl/".
3. pada path nomor (1) jalankan perintah pada terminal "go install" kemudian "go build".
4. eksekusi test (windows) "mqtt-stresser.exe -broker tcp://127.0.0.1:1883 -num-clients 10 -num-messages 150 -rampup-delay 1s -rampup-size 10 -global-timeout 180s -timeout 20s".

Note: Program ini dijalankan dengan pyhton versi 3.1.1.
