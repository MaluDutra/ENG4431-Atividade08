from flask import Flask, request, render_template, redirect
import json
from uuid import uuid4

app = Flask(__name__)

#parte do login
@app.route('/form', methods=["GET", "POST"])
def login_form():
  if request.method == "POST":
    new_log = {}
    try:
      with open("users.json", "r+") as arq:
        lista = json.loads(arq.read())
        formulario = dict(request.form)
        for usuario in lista:
          if usuario["username"] == formulario["username"]:
            return render_template("form.html", error_msg = "Nome de usuário já usado =c")
        new_log["username"] = formulario["username"]
        new_log["password"] = formulario["password"]
        new_log["login"] = False
        lista.append(new_log)

        arq.seek(0)
        arq.truncate()
        arq.write(json.dumps(lista))

      return redirect("/form")
    except Exception as e:
      return {"message": str(e)}, 400
  return render_template("form.html")

#parte dos logs dos comandos
@app.route('/logs')
def list():
  lista = []
  try:
    with open("db.json") as arq:
      lista = json.loads(arq.read())
    return lista, 200  
  except Exception as e:
    return {"message": str(e)}, 500

@app.route('/logs', methods=["POST"])
def create():
  lista = []
  try:
    body = request.json
    body["_id"] = str(uuid4())
    with open("db.json", "r+") as arq:
      lines = arq.read()
      lista = json.loads(lines)
      lista.append(body)
  
      arq.seek(0)
      arq.write(json.dumps(lista))
  
      arq.truncate()

    return body, 201
  except Exception as e:
    return {"message": str(e)}, 500

#parte do CRUD dos logs
def find_by_id(id, lista):
  for i in range(len(lista)):
    if lista[i]["_id"] == id:
      return i
  return -1

@app.route('/')  
def read_all():
  logs = []
  try:
    with open("db.json") as arq:
      logs = json.loads(arq.read())
    return logs, 200
  except:
    return "Erro interno do servidor", 500

@app.route('/logs/<string:id>') 
def read_one(id):
  logs = []
  try:
    with open("db.json") as arq:
      logs = json.loads(arq.read())
      logId = find_by_id(id, logs)
      if logId != -1:
        return logs[logId], 200
  except:
    return "Erro interno do servidor", 500

@app.route('/logs/criar', methods=['POST'])
def create_one():
  logs = []
  try:
    with open("db.json", "r+") as arq:
      logs = json.loads(arq.read())
      novo_log = request.json
      novo_log["_id"] = str(uuid4())
      logs.append(novo_log)

      arq.seek(0)
      arq.write(json.dumps(logs))
    return logs, 201
  except:
    return "Erro interno do servidor", 500


@app.route('/logs/update/<string:id>', methods=['PUT'])
def update_one(id):
  logs = []
  try:
    with open("db.json", "r+") as arq:
      logs = json.loads(arq.read())
      log_update = request.json
      log_updateId = find_by_id(id, logs)
      if log_updateId != -1:
        log_update["_id"] = id
        logs[log_updateId] = log_update

      else:
        return "Log não encontrado", 404

      arq.seek(0)
      arq.write(json.dumps(logs))
    return log_update, 201
  except:
    return "Erro interno do servidor", 500

@app.route('/logs/deletar/<string:id>', methods=['DELETE'])
def delete_one(id):
  logs = []
  try:
    with open("db.json", "r+") as arq:
      logs = json.loads(arq.read())
      log_deletaId = find_by_id(id, logs)
      if log_deletaId != -1:
        logs.pop(log_deletaId)

      else:
        return "Log não encontrado", 404

      arq.seek(0)
      arq.truncate()
      arq.write(json.dumps(logs))

    return logs, 200
  except:
    return "Erro interno do servidor", 500



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)  