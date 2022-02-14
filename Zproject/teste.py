import certifi
from pymongo import MongoClient

#connect to MongoDatabase
ca = certifi.where()
client = MongoClient("mongodb+srv://fverruck:ik2-y47-dia-76Z@cluster0.g9gze.mongodb.net/result?retryWrites=true&w=majority", tlsCAFile=ca)
senhas = client.result.senhas
user = 'fabio'
#create variable to check if user already exists
check = senhas.find_one({"login" : user})

teste = user == check['login']
contrateste = user != check['login']

print(user)
print(check)
print(teste)
print(contrateste)

if teste:
	print("Deu certo")