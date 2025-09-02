import cv2
import socket
import numpy as np
from flask import Flask, render_template
import threading

app = Flask(__name__)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12345))

cap = cv2.VideoCapture(0)

temperature_data = {"value": 0.0, "message": "", "penjelasan": "",  "health_info": ""}

def update_temperature():
    global temperature_data
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        temperature = float(data.decode())

        temperature_data["value"] = temperature

        if temperature < 28.0:
            temperature_data["message"] = "Suhu tubuh RENDAH. Terdeteksi : Hipotermia (Berat)!"
            temperature_data["penjelasan"] = "Hipotermia sudah bisa dikatakan parah bila suhu tubuh kurang dari 28 derajat Celsius. Kondisi ini sangat berbahaya, sehingga perlu mendapatkan pertolongan medis secepatnya. Gejala hipotermia fase parah, antara lain sulit bernapas, pupil tidak reaktif, gagal jantung, edema paru dan henti jantung. Ketika seseorang sudah mengalami hipotermia parah, ia sudah tidak sadar dengan apa yang ia lakukan atau lingkungan di sekitarnya."
            temperature_data["health_info"] = "Suhu tubuh RENDAH. Terdeteksi : Hipotermia (Berat)!"
        elif temperature < 32.0:
            temperature_data["message"] = "Suhu tubuh RENDAH. Terdeteksi : Hipotermia (Sedang)!"
            temperature_data["penjelasan"] = "Hipotermia memasuki fase sedang bila suhu tubuh menurun sampai di kisaran 28–32 derajat Celsius. Gejala hipotermia fase sedang, antara lain detak jantung tidak teratur, detak jantung dan pernapasan melambat, tingkat kesadaran menurun, pupil melebar, tekanan darah menurun, dan refleks menurun."
            temperature_data["health_info"] = "Suhu tubuh RENDAH. Terdeteksi : Hipotermia (Sedang)!"
        elif temperature < 35.5:
            temperature_data["message"] = "Suhu tubuh RENDAH. Terdeteksi : Hipotermia (Ringan)!"
            temperature_data["penjelasan"] = "Hipotermia masih termasuk fase ringan bila suhu tubuh berada di kisaran 32–35 derajat Celsius. Gejala hipotermia fase ringan, antara lain tekanan darah tinggi, menggigil, detak jantung meningkat dan napas menjadi cepat, pembuluh darah menyempit, kelelahan, serta kurang koordinasi. (Gejala menggigil sebenarnya adalah pertanda baik bahwa sistem regulasi panas tubuh seseorang masih aktif.) "
            temperature_data["health_info"] = "Suhu tubuh RENDAH. Terdeteksi : Hipotermia (Ringan)!"
        elif temperature > 41.0:
            temperature_data["message"] = "Suhu tubuh TINGGI. Terdeteksi Hiperpireksia!"
            temperature_data["penjelasan"] = "Hiperpireksia adalah suatu kondisi di mana suhu tubuh seseorang meningkat secara signifikan melebihi batas normal (biasanya di atas 41 derajat Celsius atau 105,8 derajat Fahrenheit). Hiperpireksia sering kali terkait dengan penyakit atau kondisi medis tertentu, dan dapat menjadi gejala dari berbagai gangguan. Penyebab hiperpireksia dapat bervariasi, termasuk infeksi bakteri atau virus, kondisi inflamasi, penyakit autoimun, efek samping obat, dan gangguan termoregulasi."
            temperature_data["health_info"] = "Suhu tubuh TINGGI. Terdeteksi Hiperpireksia!"
        elif temperature > 40.0:
            temperature_data["message"] = "Suhu tubuh TINGGI. Terdeteksi Malaria!"
            temperature_data["penjelasan"] = "Malaria adalah penyakit menular yang disebabkan oleh parasit dari genus Plasmodium. Penyakit ini umumnya ditularkan melalui gigitan nyamuk Anopheles yang terinfeksi oleh parasit tersebut. Ada beberapa spesies Plasmodium yang dapat menyebabkan malaria pada manusia, tetapi Plasmodium falciparum dan Plasmodium vivax adalah dua spesies yang paling umum. Gejala malaria melibatkan demam, menggigil, sakit kepala, dan mual, yang dapat muncul beberapa minggu setelah terpapar parasit. Malaria dapat menjadi penyakit yang serius dan bahkan fatal jika tidak diobati dengan cepat. Faktor risiko utama termasuk perjalanan ke daerah-daerah endemis malaria dan paparan gigitan nyamuk yang terinfeksi."
            temperature_data["health_info"] = "Suhu tubuh TINGGI. Terdeteksi Malaria!"
        elif temperature > 38.0:
            temperature_data["message"] = "Suhu tubuh TINGGI. Terdeteksi Tipes!"
            temperature_data["penjelasan"] = "Tipes, atau disebut juga dengan tifoid, adalah penyakit infeksi bakteri yang disebabkan oleh bakteri bernama Salmonella typhi. Penyakit ini dapat menyebar melalui air atau makanan yang terkontaminasi oleh kotoran manusia yang mengandung bakteri tersebut. Tifoid umumnya menyebabkan gejala seperti demam tinggi, sakit kepala, nyeri perut, dan seringkali disertai dengan konstipasi atau diare."
            temperature_data["health_info"] = "Suhu tubuh TINGGI. Terdeteksi Tipes!"
        elif temperature > 35.5:
            temperature_data["message"] = "Suhu tubuh NORMAL"
            temperature_data["penjelasan"] = "Suhu tubuh normal manusia dapat bervariasi sedikit tergantung pada berbagai faktor, termasuk waktu pengukuran dan metode pengukuran. Namun, suhu tubuh normal rata-rata adalah sekitar 98.6 derajat Fahrenheit atau sekitar 37 derajat Celsius."
            temperature_data["health_info"] = "Suhu tubuh NORMAL"

temperature_thread = threading.Thread(target=update_temperature)
temperature_thread.start()

@app.route('/')
def index():
    return render_template('index.html', temperature=temperature_data["value"], 
    message=temperature_data["message"], penjelasan=temperature_data["penjelasan"])

if __name__ == '__main__':
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000, 'debug': False}).start()

    while True:
        ret, frame = cap.read()

        client_socket.sendall(frame.tobytes())

        temperature_message = f"Temperature: {temperature_data['value']:.2f} C"
        cv2.putText(frame, temperature_message, (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        health_info_message = temperature_data["health_info"]
        cv2.putText(frame, health_info_message, (15, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("Deteksi Suhu Tubuh", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    client_socket.close()
