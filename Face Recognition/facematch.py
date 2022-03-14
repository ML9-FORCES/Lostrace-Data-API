import face_recognition
image = face_recognition.load_image_file('./img/img2.jpg')
image_enc = face_recognition.face_encodings(image)[0]

unknown_img = face_recognition.load_image_file('./img/img2.jpg')
unknown_face_encoding = face_recognition.face_encodings(unknown_img)[0]

# Compare faces
results = face_recognition.compare_faces(
    [image_enc], unknown_face_encoding)

if results[0]:
    print("Same image")
else:
    print("Not the same image")