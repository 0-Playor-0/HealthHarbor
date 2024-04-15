from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit

import io

from werkzeug.utils import secure_filename
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import cv2
import numpy as np

import pytesseract
#pytesseract.pytesseract.tesseract_cmd = r'C:\USers\Ashish\AppData\Local\Program Files\Tesseract-OCR\tesseract.exe'

import requests

import datetime
from datetime import timezone
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

food_calories = {
    "artichoke": 60,
    "arugula": 1,
    "asparagus": 2,
    "aubergine": 115,
    "beetroot": 35,
    "bell pepper": 15,
    "black olives": 2,
    "broccoli": 207,
    "brussels sprouts": 8,
    "cabbage": 227,
    "capsicum": 12,
    "carrot": 25,
    "cauliflower": 3,
    "celery": 6,
    "chard": 9,
    "cherry tomato": 20,
    "chicory": 38,
    "chinese cabbage": 134,
    "chives": 1,
    "collard greens": 12,
    "corn": 562,
    "courgette": 33,
    "creamed spinach": 148,
    "cucumber": 66,
    "eggplant": 115,
    "endive": 87,
    "fennel": 73,
    "garlic": 4,
    "gherkin": 9,
    "gourd": 108,
    "green beans": 34,
    "green olives": 2,
    "green onion": 5,
    "horseradish": 7,
    "kale": 33,
    "kohlrabi": 108,
    "kumara": 112,
    "leek": 54,
    "lettuce": 90,
    "mushrooms": 1,
    "mustard greens": 15,
    "nori": 1,
    "okra": 4,
    "olives": 2,
    "onion": 34,
    "parsnips": 128,
    "peas": 79,
    "pepper": 20,
    "potato": 164,
    "pumpkin": 51,
    "radishes": 1,
    "red cabbage": 7,
    "rutabaga": 147,
    "shallots": 18,
    "spinach": 78,
    "squash": 88,
    "sweet potato": 112,
    "tomato": 20,
    "turnip greens": 34,
    "turnips": 34,
    "wasabi": 184,
    "winter squash": 147,
    "zucchini": 33,
    "acai": 20,
    "apple": 95,
    "applesauce": 167,
    "apricot": 17,
    "avocado": 320,
    "banana": 111,
    "blackberries": 62,
    "blood oranges": 70,
    "blueberries": 84,
    "cantaloupe": 23,
    "cherries": 4,
    "clementine": 35,
    "cranberries": 46,
    "currants": 63,
    "custard apple": 136,
    "dates": 20,
    "figs": 37,
    "fruit salad": 125,
    "grapes": 104,
    "greengage": 2,
    "guava": 37,
    "jackfruit": 143,
    "jujube": 22,
    "kiwi": 112,
    "lemon": 17,
    "lime": 20,
    "lychees": 7,
    "mandarin oranges": 47,
    "mango": 202,
    "minneola": 70,
    "mulberries": 60,
    "nectarine": 66,
    "orange": 62,
    "papaya": 215,
    "passion fruit": 17,
    "peach": 59,
    "pear": 101,
    "persimmon": 32,
    "physalis": 2,
    "pineapple": 453,
    "plantains": 218,
    "plum": 30,
    "pomegranate": 234,
    "quince": 52,
    "raisins": 434,
    "rambutan": 7,
    "raspberries": 64,
    "rhubarb": 11,
    "starfruit": 28,
    "strawberries": 49,
    "tamarind": 5,
    "tangerine": 47,
    "watermelon": 86,
    "baby back ribs": 360,
    "bacon and eggs": 539,
    "baked beans": 244,
    "bbq ribs": 360,
    "beef stew": 186,
    "biryani": 484,
    "black pudding": 101,
    "black rice": 323,
    "blt": 593,
    "brown rice": 670,
    "burrito": 326,
    "butter chicken": 490,
    "california roll": 33,
    "chicken caesar salad": 392,
    "chicken fried steak": 423,
    "chicken marsala": 2209,
    "chicken parmesan": 250,
    "chicken pot pie": 673,
    "chicken tikka masala": 195,
    "chili con carne": 266,
    "chimichanga": 418,
    "cobb salad": 632,
    "collard greens": 13,
    "corn dog": 438,
    "corned beef hash": 349,
    "cottage pie": 523,
    "dal": 304,
    "deviled eggs": 62,
    "dim sum": 37,
    "dosa": 287,
    "enchiladas": 323,
    "fajita": 290,
    "fish and chips": 585,
    "fried rice": 662,
    "fried shrimp": 75,
    "grilled cheese sandwich": 392,
    "ham and cheese sandwich": 352,
    "hummus": 435,
    "jambalaya": 250,
    "kebab": 774,
    "lasagne": 284,
    "mac and cheese": 699,
    "macaroni and cheese": 699,
    "mashed potatoes": 174,
    "meat pie": 290,
    "meatloaf": 721,
    "naan": 260,
    "orange chicken": 420,
    "pad thai": 375,
    "paella": 200,
    "paratha": 260,
    "pea soup": 190,
    "peanut butter sandwich": 200,
    "peking duck": 401,
    "philly cheese steak": 300,
    "pizza": 272,
    "pork chop": 295,
    "potato salad": 136,
    "pulled pork sandwich": 551,
    "ramen": 380,
    "ravioli": 134,
    "reuben sandwich": 641,
    "roast beef": 23,
    "roast dinner": 240,
    "samosa": 107,
    "sausage roll": 361,
    "sausage rolls": 101,
    "shepherds pie": 159,
    "shrimp cocktail": 130,
    "sloppy joe": 101,
    "sloppy joes": 397,
    "spaghetti bolognese": 374,
    "spring roll": 350,
    "spring rolls": 350,
    "taco": 213,
    "tandoori chicken": 198,
    "yorkshire pudding": 164
}


existingChats = []

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        quote = get_random_quote()
        greeting = get_greeting()
        posts = get_posts()
        users = get_users()
        total_calories = get_total_calories()
        step_count = get_total_steps() 
        return render_template('index.html', quote=quote, greeting=greeting, username=username, posts=posts, users=users, total_calories=total_calories, step_count=step_count)  
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        if username in users:
            return 'Username already exists'
        else:
            save_user(username, password)
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        username = session['username']
        users = get_users()
        if request.method == 'POST':
            age = request.form.get('age', '')
            location = request.form.get('location', '')
            weight = request.form.get('weight', '')
            height = request.form.get('height', '')
            goal = request.form.get('goal', '')
            activity = request.form.get('activity', '')
            points = users[username]['points']  
            users[username] = {
                'password': users[username]['password'],
                'age': age,
                'location': location,
                'weight': weight,
                'height': height,
                'goal': goal,
                'activity': activity,
                'points': points
            }
            with open('users.txt', 'w') as file:
                for user, data in users.items():
                    file.write(f"{user}:{data['password']}:{data['age']}:{data['location']}:{data['weight']}:{data['height']}:{data['goal']}:{data['activity']}:{data['points']}\n")
            session['profile'] = users[username]
            return redirect(url_for('index'))
        else:
            user_info = users.get(username, {})
            session['profile'] = user_info
            return render_template('profile.html', user_info=user_info)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('profile', None)
    return redirect(url_for('index'))



@app.route('/add_post', methods=['POST'])
def add_post():
    if 'username' in session:
        username = session['username']
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                # Save image file
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Save post data
                caption = request.form.get('caption', '')
                save_post(filename, caption, username)
    return redirect(url_for('index'))

def add_comment(post_index, comment):
    posts = get_posts()
    if post_index < len(posts):
        posts[post_index]['comments'].append(comment)
        update_posts(posts)

@app.route('/like_post/<int:post_index>', methods=['POST'])
def like_post(post_index):
    if 'username' in session:
        posts = get_posts()
        username = session['username']
        if post_index < len(posts):
            post = posts[post_index]
            if 'liked_posts' not in session:
                session['liked_posts'] = []
            if post_index not in session['liked_posts']:
                post['likes'] += 1
                session['liked_posts'].append(post_index)
                update_posts(posts)
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/comment_post/<int:post_index>', methods=['POST'])
def comment_post(post_index):
    if 'username' in session:
        comment = request.form.get('comment', '')
        if comment:
            add_comment(post_index, comment)
    return redirect(url_for('index'))

def update_posts(posts):
    with open('posts.txt', 'w') as file:
        for post in posts:
            comments = ','.join(post.get('comments', []))  
            file.write(f"{post['image'].split('/')[-1]}:{post['caption']}:{post['username']}:{post['likes']}:{comments}\n")

@app.route('/videos')
def search_videos():
    activity = request.args.get('activity')
    if not activity:
        return jsonify({'error': 'No activity provided'}), 400

    api_key = 'AIzaSyCa8CbpmSUMPu7yBkY0LXpCCpJl_KwufLQ'
  
    query = f'{activity} stock video'
    url = f'https://www.googleapis.com/youtube/v3/search?q={query}&key={api_key}&part=snippet&type=video&maxResults=1'
    response = requests.get(url)
    data = response.json()

    return jsonify(data)


@app.route('/add_food', methods=['POST'])
def add_food():
    food_item = request.form['food_item']
    if food_item.lower() in food_calories:
        calories = food_calories[food_item.lower()]
        tracker_filename = f'tracker_{session["username"]}.txt'
        with open(tracker_filename, 'a') as tracker_file:
            tracker_file.write(f"Food:{food_item.capitalize()}:{calories}\n")
        return redirect(url_for('index'))
    else:
        return "Food item not found in the database"

@app.route('/share_post/<int:post_index>')
def share_post(post_index):
    
    return redirect(url_for('index'))


@app.route('/sleep', methods=['GET', 'POST'])
def sleep():
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            sleep_start_str = request.form.get('sleep_start', '')
            sleep_end_str = request.form.get('sleep_end', '')
            if sleep_start_str and sleep_end_str:
                try:
                    sleep_start = datetime.datetime.strptime(sleep_start_str, '%Y-%m-%dT%H:%M')
                    sleep_end = datetime.datetime.strptime(sleep_end_str, '%Y-%m-%dT%H:%M')
                    if sleep_end > sleep_start:
                        sleep_duration = sleep_end - sleep_start
                        hours, remainder = divmod(sleep_duration.seconds, 3600)
                        minutes, _ = divmod(remainder, 60)
                        total_hours = hours + (minutes / 60)
                        print(total_hours)
                        points_earned = int(total_hours) * 10
                        print(points_earned)
                        tracker_filename = f'tracker_{username}.txt'
                        if not os.path.exists(tracker_filename):
                            with open(tracker_filename, 'w') as tracker_file:
                                tracker_file.write('Sleep tracker\n\n')
                        with open(tracker_filename, 'a') as tracker_file:
                            tracker_file.write(f"{sleep_start.strftime('%Y-%m-%d %H:%M:%S')} - {sleep_end.strftime('%Y-%m-%d %H:%M:%S')} ({total_hours:.1f} hours)\n")
                        users = get_users()
                        users[username]['points'] = str(int(users[username]['points']) + points_earned)
                        update_users(users)
                        return redirect(url_for('index'))
                    else:
                        return 'End time should be after start time'
                except ValueError:
                    return 'Invalid date format'
        return render_template('sleep.html')
    return redirect(url_for('login'))


rooms = {}
UserData = None

@app.route("/community", methods=["POST", "GET"])
def community():
    UserDataF = open('storage\\userData.txt','r')
    UsersData = eval(UserDataF.read())
    myUser = session['username']
    existsClient1 = False
    
    print(rooms)

    if len(UsersData)>0:
        for ClientUser in UsersData:
            if ClientUser['user'] == myUser:
                existsClient1 = True
                break
    #Adding the new member when accessed:
    #Now you can use the chat_name variable in your Flask route logic
    #Adding the new member when accessed

    if request.method == "POST":
        chat_name = request.form.get('newChatName')
        chat_code = request.form.get('newChatCode')
        room = chat_name
        
        if room not in rooms:
            rooms[room] = {"members": 0, "messages": []}
            session['room'] = room
        
        currentChatName = request.form.get('chatName')
        memberName = request.form.get('memberName')
        print(memberName,currentChatName)
        Saved = None
        if len(UsersData)>0:
            existsClient = False
            for ClientUser in UsersData:
                existsChat = False
                if ClientUser['user'] == myUser:
                    existsClient = True
                    if len(ClientUser['chat_spaces'])>0:
                        for ChatSpaceOfUser in ClientUser['chat_spaces']:
                            if memberName!=None:
                                print(ChatSpaceOfUser, ClientUser)
                                if ChatSpaceOfUser['chat_name'] == currentChatName and memberName not in ChatSpaceOfUser['chat_members']:
                                    ChatSpaceOfUser['chat_members'].append(memberName)
                                    doesExist = False
                                    Saved = ChatSpaceOfUser
                                    if len(ChatSpaceOfUser['chat_members'])>1:
                                        for ClientUserX in UsersData:
                                            if ClientUserX['user'] == memberName:
                                                if Saved != None:
                                                    ClientUserX['chat_spaces'].append(Saved)
                                            with open('storage\\userData.txt','w') as file:
                                                file.write(str(UsersData))
                                                file.close()
                                            if ClientUserX['user'] != myUser and ClientUserX['user']!=memberName and ClientUserX['user'] in ChatSpaceOfUser['chat_members']:
                                                for ChatSpaceOfUserX in ClientUserX['chat_spaces']:
                                                    if ChatSpaceOfUserX['chat_name'] == currentChatName:
                                                        ChatSpaceOfUserX['chat_members'] = ChatSpaceOfUser['chat_members']
                                            if ClientUserX['user']==memberName:
                                                doesExist = True

                                    if doesExist == False:
                                        ClientUserNew = {'user':memberName,'chat_spaces':[]}
                                        if Saved != None:
                                            ClientUserNew['chat_spaces'].append(Saved)
                                        UsersData.append(ClientUserNew)
                                    with open('storage\\userData.txt','w') as file:
                                        file.write(str(UsersData))
                                        file.close()
                                
                                    
                                    
                            
                            if ChatSpaceOfUser['chat_name'] == chat_name:
                                existsChat = True
                                
                    if existsChat != True and chat_name != None and chat_code != None:
                        ChatSpaceOfUser = {'chat_name':chat_name,'chat_code':chat_code,'chat_members':[myUser]}
                        ClientUser['chat_spaces'].append(ChatSpaceOfUser)
                        with open('storage\\userData.txt','w') as file:
                            file.write(str(UsersData))
                            file.close()
                        
                        
                        # Pass UserData to the frontend
                        return render_template("chat.html", existingChats=existingChats, userData=ClientUser['chat_spaces'])
                        
                    else:
                        return render_template("chat.html",userData = ClientUser['chat_spaces'])
                    
            
                        
                                

            
            if existsClient == False and chat_name!=None and chat_code !=None:
                ClientUser = {'user':myUser,'chat_spaces':[]}
                ChatSpaceOfUser = {'chat_name':chat_name,'chat_code':chat_code,'chat_members':[myUser]}
                ClientUser['chat_spaces'].append(ChatSpaceOfUser)
                UsersData.append(ClientUser)
                with open('storage\\userData.txt','w') as file:
                    file.write(str(UsersData))
                    file.close()
                
                # If the request method is GET, simply render the chat.html template
                return render_template("chat.html", existingChats=existingChats, userData=ClientUser['chat_spaces'])

        else:
            if chat_name != None and chat_code != None:
                ClientUser = {'user':myUser,'chat_spaces':[]}
                ChatSpaceOfUser = {'chat_name':chat_name,'chat_code':chat_code,'chat_members':[myUser]}
                ClientUser['chat_spaces'].append(ChatSpaceOfUser)
                UsersData.append(ClientUser)
                with open('storage\\userData.txt','w') as file:
                    file.write(str(UsersData))
                    file.close()
                
                # If the request method is GET, simply render the chat.html template
                return render_template("chat.html", existingChats=existingChats, userData=ClientUser['chat_spaces'])
            else:
                if len(UsersData)>0 and existsClient1 == True:
                    return render_template("chat.html",userData=ClientUser['chat_spaces'])
                else:
                    return render_template("chat.html")
        
    else:
        if len(UsersData)>0 and existsClient1 == True:
            return render_template("chat.html",userData=ClientUser['chat_spaces'])
        else:
            return render_template("chat.html")
        
@app.route("/community/<room_name>")
def roomF(room_name):
    print(room_name)
    room = str(room_name)
    session['room'] = str(room_name)
    #Based on the room_name and currentUser find out the roomCode.
    print(rooms)
    if room is None or room not in rooms:
        rooms[room] = {"members": 0, "messages": []}
        return render_template("room.html", code=room, messages=rooms[room]["messages"], name = session['username'])

    return render_template("room.html", room_name=room, messages=rooms[room]["messages"], name=session['username'])



@app.route('/leaderboard')
def leaderboard():
    users = get_users()
    sorted_users = sorted(users.items(), key=lambda x: int(x[1]['points']), reverse=True)
    leaderboard_data = [{'username': username, 'points': user_info['points']} for username, user_info in sorted_users]
    UserClient = session['username']
    for user in range(len(leaderboard_data)):
        if UserClient == leaderboard_data[user]['username']:
            position = user
            break
    print(position+1)
    return render_template('leaderboard.html', leaderboard=leaderboard_data)

@app.route('/step_tracker', methods=['POST'])
def step_tracker():
    step_count = get_step_count()
    return step_count

#Extra Code for API's and easy access ---------------------------------------------------------------------------->

def get_users():
    with open('users.txt', 'r') as file:
        users = {}
        for line in file.readlines():
            user_data = line.strip().split(':')
            if len(user_data) >= 9:
                username = user_data[0]
                password = user_data[1]
                age = user_data[2]
                location = user_data[3]
                weight = user_data[4]
                height = user_data[5]
                goal = user_data[6]
                activity = user_data[7]
                points = user_data[8]
                user_info = {
                    'password': password,
                    'age': age,
                    'location': location,
                    'weight': weight,
                    'height': height,
                    'goal': goal,
                    'activity': activity,
                    'points': points
                }
                users[username] = user_info
        return users
    
def save_user(username, password, age='', location='', weight='', height='', goal='', activity='', points='0'):
    tracker_filename = f'tracker_{username}.txt'
    if not os.path.exists(tracker_filename):
        with open(tracker_filename, 'w') as tracker_file:
            tracker_file.write('Sleep tracker\n\n')
    with open('users.txt', 'a') as file:
        file.write(f'{username}:{password}:{age}:{location}:{weight}:{height}:{goal}:{activity}:{points}\n')

def update_users(users):
    with open('users.txt', 'w') as file:
        for username, data in users.items():
            file.write(f"{username}:{data['password']}:{data['age']}:{data['location']}:{data['weight']}:{data['height']}:{data['goal']}:{data['activity']}:{data['points']}\n")

def get_random_quote():
    response = requests.get('https://api.quotable.io/random')
    if response.status_code == 200:
        data = response.json()
        return data['content']
    return 'No quote available'

def get_greeting():
  current_time = datetime.datetime.now()
  print(current_time)
  if current_time.hour < 12:
      return 'Good morning'
  elif 12 <= current_time.hour < 18:
      return 'Good afternoon'
  else:
      return 'Good evening'
  

def get_posts():
    posts = []
    if os.path.exists('posts.txt'):
        with open('posts.txt', 'r') as file:
            for line in reversed(file.readlines()): 
                post_data = line.strip().split(':')
                if len(post_data) >= 4:  
                    post = {
                        'image': url_for('static', filename='uploads/' + post_data[0]),
                        'caption': post_data[1],
                        'username': post_data[2],
                        'likes': int(post_data[3]),
                        'index': len(posts),
                        'comments': post_data[4].split(',')
                    }
                    posts.append(post)
    return posts

def save_post(image_filename, caption, username):
    with open('posts.txt', 'a') as file:
        file.write(f'{image_filename}:{caption}:{username}:0:\n')



from PIL import Image    

def get_total_calories():
    tracker_filename = f'tracker_{session["username"]}.txt'
    total_calories = 0
    with open(tracker_filename, 'r') as tracker_file:
        for line in tracker_file:
            parts = line.strip().split(':')
            if len(parts) == 3 and parts[0] == 'Food':
                try:
                    calories = int(parts[2])
                    total_calories += calories
                except ValueError:
                    pass
    return total_calories   


def get_total_steps():
    tracker_filename = f'tracker_{session["username"]}.txt'
    total_steps = 0
    with open(tracker_filename, 'r') as tracker_file:
        for line in tracker_file:
            parts = line.strip().split(':')
            if len(parts) == 2 and parts[0] == 'Steps':
                try:
                    steps = int(parts[1])
                    total_steps += steps
                except ValueError:
                    pass
    return total_steps

import json
import requests
url = 'http://127.0.0.1:8000/toxicity_pred'
furl = 'http://127.0.0.1:8002/feeling_pred'

import re

@socketio.on("message")
def message(data):
    session['feeling'] = "okay"
    # Update user points
    if 'message' not in data:
        print("Error: 'message' property is missing in the data")
        return
    
    users = get_users()
    UserClient = session.get('username')
    if UserClient in users:
        session['points'] = int(users[UserClient]['points'])

    print("Message received:", data)
    room = session.get('room')
    if room not in rooms:
        return 
    
    # The code for toxicity detection and content filtering remains unchanged

    input_data_for_model = {
        'StringInput': str(data.get("message"))
    }

    input_json = json.dumps(input_data_for_model)
    response = requests.post(url, data=input_json)

    if response.status_code == 200:
        response_text = str(response.text.strip().strip('"'))
        print(response_text)
    else:
        print(f"Error: {response.status_code} {response.text}")    
        return

    response_lines = response_text.strip().split('\\n')
    print(response_lines)

    flag = None
    for line in response_lines:
        print(line)
        if ':' in line:
            key, value = line.split(':', 1)
            if value.strip() == 'True':
                flag = key.strip()
                break

    if flag:
        content = {
            "name": "",
            "message": f"This message has been censored due to being {flag}."
        }
    else:       
        content = {
            "name": session.get('username', ""),
            "message": data.get("message", "")
        }
    
    fesponse = requests.post(furl, data=input_json)

    if fesponse.status_code == 200:
        fesponse_text = str(fesponse.text.strip().strip('"'))
    else:
        print(f"Error: {fesponse.status_code} {fesponse.text}")    

    fesponse_lines = fesponse_text.strip().split('\\n')
    print(fesponse_lines)

    Flag = None
    for line in fesponse_lines:
        print(line)
        if ':' in line:
            key, value = line.split(':', 1)
            if value.strip() == 'True':
                Flag = key.strip()
                break
    feeling_content = {}
    if Flag == None:        
        session['points'] += 5
        if not data.get("message").strip().lower().startswith("@fitbot"):
            session['feeling'] = "Ok"
    else:
        session['feeling'] = Flag
        if Flag == "liwc_negative_emotion":
            Flag = "negative"
        # Prepare content for Fitbot response
        feeling_content = {
            "name": "Fitbot",
            "message": "Hey! are you feeling alright? "+ session['username'] +". We have noticed that you are feeling " + Flag + ". Would you like to talk about it?"
        }
        
        
    
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('username')} said: {data.get('message', '')}")

    # Send Fitbot response to the room
    send(feeling_content, to=room)
    rooms[room]["messages"].append(feeling_content)

    # Check if the message starts with "@Fitbot" (case insensitive)
    if data.get("message").strip().lower().startswith("@fitbot"):
        import openai

        # Call ChatGPT API to generate a response
        input_text = f"Scenario: I am feeling {session['feeling']}.Keep what im feeling in mind while responding Query: " + data.get("message")
        input_text = str(input_text)        
        # Call function to generate response from ChatGPT model
        fitbot_response = generate_chatgpt_response(input_text)
        
        # Prepare content for Fitbot response
        fitbot_content = {
            "name": "Fitbot",
            "message": fitbot_response
        }
        
        # Send Fitbot response to the room
        send(fitbot_content, to=room)
        rooms[room]["messages"].append(fitbot_content)
        
        # Update user points
        session['points'] -= 5
    # Check if the message starts with "@Fitbot" (case insensitive)
    if data.get("message").strip().lower().startswith("@picbot"):
        import openai



        # Call ChatGPT API to generate a response
        input_text = data['message']
        input_text = str(input_text)        
        # Call function to generate response from ChatGPT model
        picbot_response = generate_dalle_response(input_text)
        
        # Prepare content for Fitbot response
        picbot_content = {
            "name": "Picbot",
            "message": picbot_response
        }
        
        # Send Fitbot response to the room
        send(picbot_content, to=room)
        rooms[room]["messages"].append(picbot_content)
        
        # Update user points
        session['points'] -= 5

    

@socketio.on("connect")
def connect(auth):
    if 'room' not in session:
        # Handle the case where 'room' key is not set in the session
        # Log an error or return an error response
        return

    room = session['room']
    name = session.get('username')
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session['room']
    name = session['username']
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

def generate_dalle_response(message):
    import openai


    prompt = message

    image_resp = openai.create(prompt="message", n=4, size="512x512")

    print(image_resp.data[0].url)

    return image_resp.data[0].url


def generate_chatgpt_response(message):
    import openai

    # API key here

    prompt = message

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful chat assistant fitbot who helps users with fitness, mental health and meditation related queries. Also you keep the users engaged."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=250,
    )

    return response.choices[0].message.content.strip()


def get_step_count():
    if 'image' not in request.files:
        return '0'

    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))

    ocr_text = pytesseract.image_to_string(image)
    step_count = extract_numerical_part(ocr_text)

    
    username = session.get('username')
    if username:
        tracker_filename = f'tracker_{username}.txt'
        with open(tracker_filename, 'a') as tracker_file:
            tracker_file.write(f"Steps:{step_count}\n")

   
        users = get_users()
        if username in users:
            users[username]['points'] = str(int(users[username]['points']) + step_count // 1000 * 10)
            update_users(users)

    return redirect(url_for('index'))

def extract_numerical_part(text):
    numerical_part = ''.join(filter(str.isdigit, text))
    return int(numerical_part) if numerical_part else 0

    
if __name__ == '__main__':
    socketio.run(app)