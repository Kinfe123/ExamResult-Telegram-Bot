import os
import telebot
import json
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()
url = os.getenv("SUPABASE_URL")
key =  os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)


API_TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(API_TOKEN)

with open('data.json') as f:
    data = json.load(f)

@bot.message_handler(commands=["start"])
def send_message(message):
    user = message.from_user
    user_created = supabase.table('bot_users').insert({'user_id': user.username}).execute()
    bot.send_message(chat_id=user.id , text= f"👋 Hello 👤 {user.first_name}(@{user.username}) Welcome To Yaberus Result Bot 🚀 , where you can explore your result and acadamic status 📊 , Just send us your ID over here  ")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    user = message.from_user
    help_message = f"""
   To check you result , You have to give the id that the school has provided for you.

   Like YW/12121/912

   🚀 For more info , you can contact - +251 92 273 0604


"""
    bot.send_message(chat_id=user.id, text=help_message)

@bot.message_handler(commands=['dev'])
def send_dev(message):
    user = message.from_user

    help_message = f"""
   Developed by 💻 - @Kinfe123
🚀 For more info , you can contact - +251 92 273 0604


"""
    bot.send_message(chat_id=user.id , text=help_message)


@bot.message_handler(func=lambda message: True)
def message_handler(message):
    
    with open('data.json') as f:
      data = json.load(f)
    # Get the user's name from the message text
    name = message.text
    user = message.from_user

    user_database_info = supabase.table('bot_users').select("*").eq("user_id" , user.username).execute()
    view_count = user_database_info.data[0]['count']
    
    view_count -= 1
    update_count  = supabase.table("bot_users").update({ "count":view_count}).eq("user_id" , user.username).execute()
    if update_count.data[0]['count'] >= 1:
       
    
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
            # data , count = supabase.table("bot_users").insert({"user_id": user.username  }).execute()
            # print(data , count )
            to_be_send = f"""

            .
                \t
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
            bot.send_message(chat_id=message.chat.id , text=f'You have left with {view_count} views\n\n\nPlease provide your ID to view results') 
        else:
            bot.send_message(chat_id=message.chat.id , text=f"No such student 👤 with ID - {id_from_user}")

    else:
       bot.send_message(chat_id=message.chat.id , text="Please you have run out of your free plan , You can again start view results after sending 10 ETB Birr to 0919866517 and contacting here - @Kinfe123. Peace ✌ ")

@bot.message_handler(commands=['hello'])
def send_welcome(message):
    bot.reply_to(message, "HI!")




try:
    
  print("Bot running")
  bot.polling()
except supabase.exceptions.ClientError as error:
   print('Failed successfully 😅')