import bcrypt

password = "admin1234".encode("utf-8")
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode("utf-8"))
