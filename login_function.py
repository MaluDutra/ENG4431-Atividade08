import json

def login_user(username, password):
  try:
    with open("users.json", "r+") as arq:
        lista = json.loads(arq.read())
        for (pos, el) in enumerate(lista):
          if username == el["username"] and password == el["password"]:
            lista[pos]["login"] = True
            arq.seek(0)
            arq.truncate()
            arq.write(json.dumps(lista))
            return True
        return False
  except Exception as e:
    return {"message": str(e)}, 400

def login_clear():
  try:
    with open("users.json", "r+") as arq:
      lista = json.loads(arq.read())
      for (pos, el) in enumerate(lista):
        lista[pos]["login"] = False
        arq.seek(0)
        arq.truncate()
        arq.write(json.dumps(lista))
  except Exception as e:
    return {"message": str(e)}, 400

def logout_user(username):
  try:
    with open("users.json", "r+") as arq:
      lista = json.loads(arq.read())
      for (pos, el) in enumerate(lista):
        if username == el["username"]:
          lista[pos]["login"] = False
          arq.seek(0)
          arq.truncate()
          arq.write(json.dumps(lista))
  except Exception as e:
    return {"message": str(e)}, 400