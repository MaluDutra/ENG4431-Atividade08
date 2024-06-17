import os, json
import discord
import requests as req
from webscrapping import extrair_informacao, extrair_horario
from gemini import gemini_generate
from login_function import login_user,login_clear,logout_user

TOKEN = os.getenv("DISCORD_KEY")
API_URL = "https://91678cc7-e244-4eb0-ade2-957e2c5bd10f-00-hkbvpotnx773.kirk.replit.dev:3000/logs"

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print(f"{client.user} está funcionandooo! =D")
  login_clear()


comandos = ["/help", "/ghibli", "/hora_jp","/ai","/logout"]

@client.event
async def on_message(msg):
  tem_comando = False
  logado = False
  if msg.author == client.user:
    return

  user_msg = msg.content.lower()

  for el in comandos:
    if el in msg.content:
      tem_comando = True
  
  if "/login" in user_msg:
    enviar = user_msg.split(" ")
    if login_user(enviar[1],enviar[2]):
      logado = True
      await msg.channel.send("Login realizado com sucesso! =)\ncaso deseje sair de sua conta, é só usar o comando /logout")
    else:
      await msg.channel.send("Login não realizado! =(")
      
  if tem_comando:
    with open("users.json") as arq:
      lista = json.loads(arq.read())
      for el in lista:
        if el["username"] == msg.author.name:
          logado = el["login"]

    if "/help" in user_msg:
      await msg.channel.send("oie! sou um bot e estes são os comandos que vc pode utilizar:\n/help - mostro esta mensagem\n/ghibli - mostro os filmes do Studio Ghibli em ordem de lançamento\n/ai - faço uma pergunta para a Gemini AI do Google\n/hora_jp - mostro o horário atual no japão")
    
    if logado:      
      if "/ghibli" in user_msg:
        scrape_info = extrair_informacao()
        if scrape_info:
          await msg.channel.send(scrape_info) 
        else:
          await msg.channel.send("Não consegui pegar a informação desejada :(")
      
      if "/hora_jp" in user_msg:
        scrape_info = extrair_horario()
        if scrape_info:
          await msg.channel.send(scrape_info) 
        else:
          await msg.channel.send("Não consegui pegar a informação desejada :(")
      
      if "/ai" in user_msg:
        response = gemini_generate(user_msg[4:])
        if response:
          await msg.channel.send(response)
        else:
          await msg.channel.send("Não consegui me comunicar com a AI :(")
      
      if "/logout" in user_msg:
        logout_user(msg.author.name)
        await msg.channel.send("logout realizado com sucesso! =)")
          
    else:
      await msg.channel.send("por favor, realize seu login com o comando '/login (username) (senha)' antes!")
  if tem_comando:
    req_body = {
      "authorName": msg.author.name,
      "msgContent": msg.content,
      "createdAt": str(msg.created_at)
    }
    response = req.post(API_URL, json=req_body)
    
    if response.status_code == 201:
      print("Log registrado com sucesso!")
    else:
      print("Deu ruim no log! =c")

client.run(TOKEN)