import cv2
import os
import csv
from flask import Flask, request, render_template
from datetime import date, datetime, timedelta
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib

app = Flask(__name__)

nimgs = 10
selected_camera_id = 0  # Akan dipilih lewat dropdown

# Tanggal minggu ini
current_date = date.today()
start_of_week = current_date - timedelta(days=current_date.weekday())
end_of_week = start_of_week + timedelta(days=6)
datetoday_week = start_of_week.strftime("%Y-W%U")
datetoday2 = start_of_week.strftime("%d-%B-%Y")
date_range_week = f"{start_of_week.strftime('%d %B')} - {end_of_week.strftime('%d %B %Y')}"
tanggal_hari_ini = current_date.strftime("%A, %d %B %Y")
attendance_filename = f'Attendance/Attendance-{datetoday_week}.csv'

# Inisialisasi folder & face detector
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
os.makedirs('Attendance', exist_ok=True)
os.makedirs('static/faces', exist_ok=True)

# Buat file absensi jika belum ada
if not os.path.exists(attendance_filename):
    with open(attendance_filename, 'w') as f:
        f.write('Name,Bagian,Tanggal,Jam Berangkat,Jam Pulang,Total Jam Kerja\n')

def totalreg():
    return len(os.listdir('static/faces'))

def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        return face_points
    except:
        return []

def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)

def train_model():
    faces, labels = [], []
    userlist = os.listdir('static/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/faces/{user}'):
            img = cv2.imread(f'static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    if faces:
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(np.array(faces), labels)
        joblib.dump(knn, 'static/face_recognition_model.pkl')

def extract_attendance():
    df = pd.read_csv(attendance_filename)
    names = df['Name'].tolist()
    bagian = df['Bagian'].tolist()
    tanggal = df['Tanggal'].tolist()
    times = list(zip(df['Jam Berangkat'], df['Jam Pulang'], df['Total Jam Kerja']))
    return names, bagian, tanggal, times, len(df)

@app.route('/')
def home():
    names, bagian, tanggal, times, l = extract_attendance()
    return render_template('home.html',
        names=names, rolls=bagian, tanggal=tanggal, times=times, l=l,
        totalreg=totalreg(), datetoday2=datetoday2,
        date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
        selected_camera=selected_camera_id, mess=None)

@app.route('/set_camera', methods=['POST'])
def set_camera():
    global selected_camera_id
    selected_camera_id = int(request.form['camera'])
    print(f"[DEBUG] Kamera dipilih: {selected_camera_id}")
    return home()

@app.route('/test_camera')
def test_camera():
    print(f"[DEBUG] Menguji kamera ID: {selected_camera_id}")
    cap = cv2.VideoCapture(selected_camera_id)
    if not cap.isOpened():
        return render_template('home.html', mess="Kamera tidak bisa dibuka.",
            names=[], rolls=[], tanggal=[], times=[], l=0,
            totalreg=totalreg(), datetoday2=datetoday2,
            date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
            selected_camera=selected_camera_id)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Uji Kamera', frame)
        if cv2.waitKey(1) == 27:  # ESC
            break
    cap.release()
    cv2.destroyAllWindows()
    return home()

@app.route('/absen_masuk')
def absen_masuk():
    return run_attendance('masuk')

@app.route('/absen_pulang')
def absen_pulang():
    return run_attendance('pulang')

def run_attendance(mode='masuk'):
    print(f"[DEBUG] Mulai absensi ({mode}) dengan kamera ID: {selected_camera_id}")
    cap = cv2.VideoCapture(selected_camera_id)
    if not cap.isOpened():
        return render_template('home.html', mess="Kamera tidak tersedia.",
            names=[], rolls=[], tanggal=[], times=[], l=0,
            totalreg=totalreg(), datetoday2=datetoday2,
            date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
            selected_camera=selected_camera_id)

    if 'face_recognition_model.pkl' not in os.listdir('static'):
        return render_template('home.html', mess="Model belum dilatih. Tambahkan wajah dulu.",
            names=[], rolls=[], tanggal=[], times=[], l=0,
            totalreg=totalreg(), datetoday2=datetoday2,
            date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini,
            selected_camera=selected_camera_id)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        faces = extract_faces(frame)
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
            user = identify_face(face.reshape(1, -1))[0]
            update_attendance(user, mode)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, user, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.imshow("Absensi", frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    return home()

def update_attendance(name, mode='masuk'):
    username = name.split('_')[0]
    userbagian = name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")
    today_str = date.today().strftime("%d-%m-%Y")
    df = pd.read_csv(attendance_filename)

    existing = df[(df['Name'] == username) & (df['Tanggal'] == today_str)]

    if existing.empty:
        jam_masuk = current_time if mode == 'masuk' else '-'
        jam_pulang = current_time if mode == 'pulang' else '-'
        with open(attendance_filename, 'a') as f:
            f.write(f'\n{username},{userbagian},{today_str},{jam_masuk},{jam_pulang},-')
    else:
        idx = existing.index[0]
        if mode == 'masuk' and df.at[idx, 'Jam Berangkat'] == '-':
            df.at[idx, 'Jam Berangkat'] = current_time
        elif mode == 'pulang' and df.at[idx, 'Jam Pulang'] == '-':
            df.at[idx, 'Jam Pulang'] = current_time

        if df.at[idx, 'Jam Berangkat'] != '-' and df.at[idx, 'Jam Pulang'] != '-':
            fmt = "%H:%M:%S"
            try:
                jam_masuk = datetime.strptime(df.at[idx, 'Jam Berangkat'], fmt)
                jam_pulang = datetime.strptime(df.at[idx, 'Jam Pulang'], fmt)
                durasi = jam_pulang - jam_masuk
                df.at[idx, 'Total Jam Kerja'] = str(durasi)
            except:
                df.at[idx, 'Total Jam Kerja'] = '-'
        df.to_csv(attendance_filename, index=False)

@app.route('/add', methods=['POST'])
def add():
    newusername = request.form['newusername']
    newbagian = request.form['newuserid']

    if not newusername or not newbagian:
        return render_template('home.html', mess="Nama dan Bagian harus diisi.",
                               names=[], rolls=[], tanggal=[], times=[], l=0,
                               totalreg=totalreg(), datetoday2=datetoday2,
                               date_range_week=date_range_week, tanggal_hari_ini=tanggal_hari_ini)

    userimagefolder = f'static/faces/{newusername}_{newbagian}'
    os.makedirs(userimagefolder, exist_ok=True)

    i, j = 0, 0
    cap = cv2.VideoCapture(selected_camera_id)
    if not cap.isOpened():
        return render_template('home.html', mess="Kamera tidak tersedia.")

    while True:
        _, frame = cap.read()
        faces = extract_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/{nimgs}', (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2)
            if j % 5 == 0:
                name = f"{newusername}_{newbagian}_{i}.jpg"
                cv2.imwrite(os.path.join(userimagefolder, name), frame[y:y+h, x:x+w])
                i += 1
            j += 1
        if j == nimgs * 5:
            break
        cv2.imshow('Adding new User', frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    train_model()
    return home()

if __name__ == '__main__':
    app.run(debug=True)
