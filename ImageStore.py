import cv2
from imgbeddings import imgbeddings
import PIL.Image
import os
import psycopg2

mydb = psycopg2.connect(
    host="localhost",
    database="dhirajshetty",
    user="dhirajshetty",
    password="Dhiraj@123"
)

alg = "haarcascade_frontalface_default.xml"
haar_cascade = cv2.CascadeClassifier(alg)
i = 0
cur = mydb.cursor()
cur.execute("TRUNCATE pictures;")
for images in os.listdir("read-faces"):
    print(images)
    if images == ".DS_Store":
        continue
    img = cv2.imread("read-faces/" + images, 0)
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    target_file_name = 'stored-faces/' + str(i) + '.jpg'
    cv2.imwrite(
        target_file_name,
        gray_img,
    )
    i = i + 1


for filename in os.listdir("stored-faces"):
    img = PIL.Image.open("stored-faces/" + filename)
    ibed = imgbeddings()
    embedding = ibed.to_embeddings(img)
    cur.execute("INSERT INTO pictures (picture, embedding) values (%s,%s);", (filename, embedding[0].tolist()))
    print(filename)
mydb.commit()
