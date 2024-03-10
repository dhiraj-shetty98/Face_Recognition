from imgbeddings import imgbeddings
import PIL.Image
import psycopg2

mydb = psycopg2.connect(
    host="localhost",
    database="dhirajshetty",
    user="dhirajshetty",
    password="Dhiraj@123"
)

file_name = "Virat2.jpg"
img = PIL.Image.open(file_name)
ibed = imgbeddings()
embedding = ibed.to_embeddings(img)

cur = mydb.cursor()
string_representation = "[" + ",".join(str(x) for x in embedding[0].tolist()) + "]"
print(string_representation)
cur.execute("SELECT * FROM pictures ORDER BY embedding <-> %s LIMIT 1;", (string_representation,))
rows = cur.fetchall()
for row in rows:
    print(row[0])
    img = PIL.Image.open("stored-faces/" + row[0])
    img.show()
cur.close()
