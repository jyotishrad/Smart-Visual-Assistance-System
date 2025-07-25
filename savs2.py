import cv2
import face_recognition
import pyttsx3
import numpy as np

# Initialize Text-to-Speech
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

# Load object detection model
net = cv2.dnn.readNetFromCaffe(
    'MobileNetSSD_deploy.prototxt',
    'MobileNetSSD_deploy.caffemodel'
)

# Class labels MobileNet SSD can detect
class_names = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant",
    "sheep", "sofa", "train", "tvmonitor"
]

# Known face images
known_faces = []
known_names = []
speech_count = {}

known_images = {
    "MS Dhoni": r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\dhoni.jpg",
    "Virat Kohli": r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\kohli (2).jpg",
    "Narendra Modi": r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\modi (2).jpg",
    "Jyoti": r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\WhatsApp Image 2024-02-24 at 17.31.07_2b4a8ec2.jpg",
    "Kareena Kapoor Khan" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\images (3).jpg",
    "Vaidehi Ma'am" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\Screenshot 2025-03-30 125955.png",
    "Vicky Kaushal" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\Vicky_Kaushal_snapped_promoting_Zara_Hatke_Zara_Bach_Ke_on_the_sets_of_The_Kapil_Sharma_Show_(cropped).jpg",
    "Saif Ali Khan" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\download (1).webp",
    "Shah Rukh Khan" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\download.webp",
    "Deepika Padukone" :r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\images (1).jpg",
    "Sanskruti" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\WhatsApp Image 2025-03-30 at 13.54.28_7a5f8266.jpg",
    "Katrina Kaif" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\images (2).jpg",
    "Anushka Sharma": r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\images.jpg",
    "chalk" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\360_F_202576910_WWCzOvshgGuZjahD9z4kxTVT3moFXXPt.jpg",
    "duster" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\duster.jpg",
    "duster" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\omega-black-board-duster.png",
    "pen" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\4-Copy-jpg.webp",
    "pen" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\cello-alpha-gel-pen-253.jpg",
    "Water Bottle" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\borosilgripnsip.webp",
    "very common Water Bottle" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\1000-bpa-free-drinking-water-bottle-with-time-marker-straw-for-original-imagf8npfztmb3qg.webp",
    "Spects" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\images (6).jpg",
    "Glasses" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\Small-Round-Progressive-Reading-Glasses-for-Computers-3.webp",
    "piece of chalk" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\white-broken-chalk-on-chalkboard-260nw-312595022.webp",
    "Duster" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\images (4).jpg",
    "Blue color" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\images.png",
    "Red color" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\red-00.webp",
    "Black color" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\ps-1440-z-pro-sq-arcit18.jpg",
    "Green board" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\1.jpg",
    "White board" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\istockphoto-1306350466-612x612.jpg",
    "Car" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\Hyundai-Creta-180120241405.jpg",
    "Lamborghini" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\_New Sedans  Sports Cars Web Resized  Watermarked._002.jpeg",
    "watch" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\Apple_Watch_Series_8_LTE_41mm_Midnight_Aluminum_Midnight_Sport_Band_PDP_Image_Position-1__en-US_4b6ccd1d-dbfc-4589-a43b-3efcbe392819.webp",
    "Bottle" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\my-borosil-stainless-steel-bottles-trek-black-personalise-32329717710986.webp",
    "No entry sign ahead" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\No_Entry_Sign_(IRC-67_2022).svg.png",
    "No standing sign ahead" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\No_standing.svg.png",
    "Pedestrian Crossing ahead" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\Pedestrian_only_India.svg.png",
    "Give way sign ahead" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\Indian_Road_Sign_I-I-2.svg.png",
    "Stop ahead" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\istockphoto-486744506-612x612.jpg",
    "Bench" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\SchoolDesk-Bench_2.webp",
    "No U turn sign ahead"  : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\U-turn_prohibited.svg.png",
    "hand" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\istockphoto-149402372-612x612.jpg",
    "rubber band" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\images (8).jpg",
    "Noel sir" : r"C:\Users\Jyoti2005\Desktop\Projects\Assisstance for Visually Impaired\imgs\Screenshot 2025-04-03 145334.png"
}

for name, img_path in known_images.items():
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: Cannot read image {img_path}")
        continue

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_img)

    if encodings:
        known_faces.append(encodings[0])
        known_names.append(name)
        speech_count[name] = 0
    else:
        print(f"Warning: No face found in {name}'s image.")

video_capture = cv2.VideoCapture(0)
last_recognized_name = None

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # ---- FACE DETECTION ----
    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.5)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_faces, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index] and face_distances[best_match_index] < 0.5:
            name = known_names[best_match_index]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        if name != "Unknown" and speech_count[name] < 2:
            text_to_speech(f"This is {name}.")
            speech_count[name] += 1
            last_recognized_name = name

    # ---- OBJECT DETECTION ----
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            object_label = class_names[idx]

            box = detections[0, 0, i, 3:7] * np.array([
                frame.shape[1], frame.shape[0],
                frame.shape[1], frame.shape[0]
            ])
            (startX, startY, endX, endY) = box.astype("int")

            cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
            cv2.putText(frame, object_label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            if object_label not in speech_count:
                speech_count[object_label] = 0

            if speech_count[object_label] < 2:
                text_to_speech(f"I see a {object_label}.")
                speech_count[object_label] += 1

    # Display the frame
    cv2.imshow("Face & Object Recognition", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r') and last_recognized_name:
        text_to_speech(f"This is {last_recognized_name}.")

video_capture.release()
cv2.destroyAllWindows()
