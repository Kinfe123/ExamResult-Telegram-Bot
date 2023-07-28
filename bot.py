import os
import telebot
import json
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(API_TOKEN)

with open('data.json') as f:
    data = json.load(f)

@bot.message_handler(commands=["start"])
def send_message(message):
    user = message.from_user
    bot.send_message(chat_id=user.id , text= f"👋 Hello 👤 {user.first_name}(@{user.username}) Welcome To Yaberus Result Bot 🚀 , where you can explore your result and acadamic status 📊 , Just send us your ID over here  ")




@bot.message_handler(func=lambda message: True)
def message_handler(message):
    # Get the user's name from the message text
    name = message.text
    user = message.from_user
    if(name ==  ""):
       bot.send_message(chat_id=message.chat.id , text=f'❗ Please , {user.first_name} Provide a valid ID  ')
    else:
       isFound = False
       result = {}
       id_from_user = message.text
       for each_student in data:
          if id_from_user == each_student['id']:
             isFound = True
             result = each_student

       print(isFound , result)

       if isFound:
          to_be_send = f"""

             

              PERSONAL DETAILS 🧑
        ----------------------------------------
          👤 NAME ➖   {result['name']}

          🆔 ID ➖  {result['id']}


              RESULT DETAILS 📊
        ----------------------------------------

          MATHS    ➖   {result['math']}

          CHEMISTRY   ➖    {result['chem']}

          BIOLOGY    ➖    {result['bio']}

          CIVICS    ➖   {result['civic']}

          ENGLISH    ➖   {result['eng']}


          
        


"""
       
    
    # Send a message to the user with their name
          bot.send_message(chat_id=message.chat.id, text=to_be_send)
          bot.send_message(chat_id=message.chat.id , text='Please provide your ID to view results  ') 
       else:
          bot.send_message(chat_id=message.chat.id , text=f"No such student 👤 with ID - {id_from_user}")

@bot.message_handler(commands=['hello'])
def send_welcome(message):
    bot.reply_to(message, "HI!")


try:
    
  print("Bot running")
  bot.polling()
except:
   print('Failed successfully 😅')