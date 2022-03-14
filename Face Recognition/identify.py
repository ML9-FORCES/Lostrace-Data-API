import face_recognition
from PIL import Image, ImageDraw

image_bill = face_recognition.load_image_file('./img/bill.jpg')
img_bill_enc = face_recognition.face_encodings(image_bill)[0]

image_elon = face_recognition.load_image_file('./img/elon.jpg')
img_elon_enc = face_recognition.face_encodings(image_elon)[0]

#array of encodings and names
known_face_encodings = [
    img_bill_enc,
    img_elon_enc
]

known_face_names = [
    "Bill Gates",
    "Elon Musk"
]

#test image
test_img = face_recognition.load_image_file('./img/bill_elon.jpg')

face_locations = face_recognition.face_locations(test_img)
face_encodings = face_recognition.face_encodings(test_img, face_locations)

pil_image = Image.fromarray(test_img)

draw = ImageDraw.Draw(pil_image)

for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    name = "Unknown Person"
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    draw.rectangle(((left, top), (right, bottom)), outline=(0,0,0))

    text_width, text_height = draw.textsize(name)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill = (0,0,0), outline=(0,0,0))
    draw.text((left+6, bottom-text_height-5), name, fill=(255, 255, 255, 255))

del draw
pil_image.show()