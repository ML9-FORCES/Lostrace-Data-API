from email.mime import image
import face_recognition

image = face_recognition.load_image_file('./img/img1.jpg')
face_locations = face_recognition.face_locations(image)

print(face_locations)
print(f'There are {len(face_locations)} people in this image')
