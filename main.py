'''
The main file for Bot++.
'''
# Import needed packages
from flask import Flask, request  # For building a simple server to receiving messages
import requests  # For sending requests to the bot
import json  # For managing Minecraft server query response
import os  # Used to handle files
import time  # Used for timed keywords and others
import random  # For the economy module
import argparse  # Used to get arguments
from chatterbot import ChatBot  # Used for chat
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer  # Training the chatbot

app = Flask(__name__)  # Create the Flask APP
parser = argparse.ArgumentParser(description="Bot++ manual")  # Create the parser

chat = ChatBot("Toxic-Bot")  # Create the chatbot
trainer = ListTrainer(chat)  # Create the list trainer for the chatbot
corpus_trainer = ChatterBotCorpusTrainer(chat)  # Create the corpus trainer for the chatbot

parser.add_argument('Group_ID', type=int, help='You QQ group ID')  # Add the argument for group ID
args = parser.parse_args()  # Parse the args

group_id = args.Group_ID  # Get the group ID

# Initialize training
corpus_trainer.train(
    "chatterbot.corpus.english",
    "chatterbot.corpus.chinese",
)


class Modules:
    '''
    Modules for the QQ bot - You can always add more!
    '''
    def __init__(self):
        '''
        Initialize some variables.
        '''
        self.chat_stats = False  # Chat status

    def send(self, group_id, msg):
        '''
        Sends a message to the group.
        '''
        requests.get(f"http://127.0.0.1:5700/send_group_msg?group_id={str(group_id)}&message={msg}")  # Do the request to send the message

    def send_to(self, user_id, msg):
        '''
        Sends a message to someone.
        '''
        requests.get(f"http://127.0.0.1:5700/send_private_msg?user_id={str(user_id)}&message={msg}")  # Do the request to send the message

    def calc(self, msg):
        '''
        Calculate something and send the result.
        '''
        try:
            calc_result = eval(msg[6:])  # Get the result
        except Exception as e:  # Example: a/0
            self.send(group_id, e)
        else:  # Nothing wrong, send the results
            self.send(group_id, calc_result)

    def mc_query(self, host, port=25565):
        '''
        Detect whether a Minecraft server is online or not.
        '''
        try:
            query_response = requests.get(f"http://127.0.0.1/mcq/json.php?host={host}&port={port}")  # Request to a PHP file with Apache to get the server's status
        except Exception:  # The query server is offline
            self.send(group_id, "Query server is offline! Please notify admin!")
        else:
            # Write data into a json file to convert plain text to JSON data
            with open('cache/mcq.json', 'w') as f:
                f.write(query_response.text)  # Store plain text
                f.close()
            with open('cache/mcq.json', 'r') as f:
                mc_data = json.load(f)  # Read as JSON data
                f.close()

            # Get server details
            online = mc_data['status']
            motd = mc_data['motd']['clean']
            online_players = mc_data['players']['online']
            max_players = mc_data['players']['max']
            self.send(group_id, f"Status: {online}\nMOTD: {motd}\nOnline players: {online_players}\nMax players: {max_players}")  # Send results

            # Flush query data
            os.system('rm -rf mcq.json')
            os.system('touch mcq.json')

    def random_sexy(self, uid):
        '''
        Get an random sexy image from Pixiv and send it to chat.
        '''
        random_img_res = requests.get('http://api.lolicon.app/setu/v2?r18=0&num=1')  # Get raw data from API
        random_img_data = random_img_res.json()  # Convert raw data into JSON data

        # Get data
        author = random_img_data['data'][0]['author']
        pid = random_img_data['data'][0]['pid']
        title = random_img_data['data'][0]['title']
        img_url = random_img_data['data'][0]['urls']['original']
        file_type = random_img_data['data'][0]['ext']

        # Send to the user
        self.send_to(uid, f'[CQ:image,file={img_url}]')  # Send image
        self.send_to(uid, f'Author: {author}\nPID: {pid}\nTitle: {title}\nImage URL: {img_url}\nFile type: {file_type}')  # Send description

    def wotd(self):
        '''
        Get the wallpaper of the day and send it to chat.
        '''
        img_api = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'  # Wallpaper API from Bing
        img_res = requests.get(img_api)  # Get data
        img_data = img_res.json()  # Get JSON data

        # Get image details and the image itself
        cr = img_data['images'][0]['copyright']
        title = img_data['images'][0]['title']
        img_url = 'http://cn.bing.com' + img_data['images'][0]['url']

        self.send(group_id, f"[CQ:image,file={img_url[:img_url.find('&rf')]}]")  # Send image
        self.send(group_id, f'Title: {title}\nCopyright: {cr}')  # Send description

    def get_news(self):
        '''
        Get headline news.
        '''
        news_api = 'http://c.m.163.com/nc/article/headline/T1348647853363/0-40.html'  # Headline news API from Netease
        news_res = requests.get(news_api)  # Get data
        news_data = news_res.json()  # Get JSON data

        # Get details
        main_news = news_data['T1348647853363'][0]['title']
        other_news1 = news_data['T1348647853363'][1]['title']
        other_news2 = news_data['T1348647853363'][2]['title']
        other_news3 = news_data['T1348647853363'][3]['title']
        other_news4 = news_data['T1348647853363'][4]['title']

        self.send(group_id, f"1. {main_news}\n\n2. {other_news1}\n\n3. {other_news2}\n\n4. {other_news3}\n\n5. {other_news4}")  # Send result

    def chat(self, msg):
        '''
        Chat with others
        '''
        if self.chat_stats:  # Chat mode is on:
            if msg == '/chat-on':  # Do now respond to '/chat-on'
                pass
            else:
                chat_res = chat.get_response(msg)  # Get response form chatterbot
                self.send(group_id, chat_res)  # Send response
        else:  # Chat mode is off:
            pass
    
    class Timed:
        '''
        Timed keywords.
        '''
        def __init__(self):
            self.localtime = time.ctime()  # Get current time

        def tech_no(self):
            '''
            Technoblade! Noooooooooo!
            '''
            if self.localtime[4:10] == 'Jul  1':
                modules.send(group_id, 'Technoblade Never Dies!!!')  # TECHNOBLADE NEVER DIES!!!
    class Economy:
        '''
        Economy system in chat.
        '''
        def get_current(self, uid):
            '''
            Get the current economy status of someone.
            '''
            uid = str(uid)  # Convert UID from int to str

            with open('economy.json', 'r') as f:  # Open storage file and load the data
                economy_stats = json.load(f)  # Get the coins this user have
                f.close()

            coins = economy_stats[uid]  # Get your coins

            modules.send(group_id, f"Your current economy status:\nCoins: {coins}")  # Send the results

        def work(self, uid):
            '''
            Earn coins!
            '''
            uid = str(uid)  # Convert UID from int to str

            income = random.randint(-500, 1000)  # Random income

            with open('economy.json', 'r') as f:  # Open storage file and load the data
                economy_stats = json.load(f)
                f.close()

            coins = economy_stats[uid]  # Get your coins
            coins = int(coins)  # Convert coins to int so that we can add the income
            coins += income  # Change current status
            coins = str(coins)  # Convert coins to str so that we can dump them
            economy_stats[uid] = coins  # Save it to the dict

            with open('economy.json', 'w') as f:  # Dump the current status
                json.dump(economy_stats, f)
                f.close()

            if income > 0:  # You got some money!
                modules.send(group_id, f"You got ${income}.")  # How much did you earn?
            elif income < 0:  # Too bad!
                modules.send(group_id, f"You lost ${income}.")
            elif income == 0:
                modules.send(group_id, 'Nothing happened...')

    def help_(self):
        '''
        Send a help message.
        '''
        self.send(group_id, "Keywords:\n\ntb: Just a command to check whether the bot is alive or not.\n\n/query: Used to check the basic information about a Minecraft server. No response means that the server is offline.\nUsage: /query {Server address}\n\n/calc: Calculate something.\nUsage: /calc {Equation}\n\n/wotd: Get wallpaper of the day from Bing.\nUsage: /wotd\n\n/randomsexy: Get a sexy picture from Pixiv. The result will be send to you via private chat. You need to add the bot as your friend before using. USE BY CAUTION!\nUsage: /randomsexy\n\n/news: Get the headline news\nUsage: /news\n\n\n\nChat mode: Used to chat with the bot (BETA). While in this mode, every message will be given to the bot and the bot will give a response\nUsage:\n/chat-on: Turn the mode on.\n/chat-off: Turn the mode off.\n\nEconomy: No real use (for now)\nUsage:\n^bal: How much cash do you have?\n^work: Work for cash.. or lose them!\n\n\n\nTimed keywords:\n\nTechnoblade/Techno:\nAvailable: Jul 1")


def main(msg, uid):
    '''
    Get the keyword of a sentence, then send a proper request to the server.
    '''
    msg = msg.lower()

    # Wordlist for insult detection
    with open('insults.txt', 'r') as f:
        insults = f.readlines()
        insults = [i.strip('\n') for i in insults]
    # Insults detection
    for i in insults:
        if i in msg:
            modules.send(group_id, 'Language!')

    # Respond so that we know the bot is online
    if msg == 'bpp':
        modules.send(group_id, '?')

    # Minecraft server detect
    elif msg[0:6] == '/query':
        modules.mc_query(msg[7:])

    # Random images
    elif msg == '/randomsexy':
        modules.random_sexy(uid)
    elif msg == '/wotd':
        modules.wotd()

    # Calculator
    elif msg[0:5] == '/calc':
        modules.calc(msg)

    # News
    elif msg == '/news':
        modules.get_news()
    
    # Chat detection
    elif msg == '/chat-on':
        modules.send(group_id, "Chat mode ON.")
        modules.chat_stats = True
    elif msg == '/chat-off':
        modules.send(group_id, "Chat mode OFF.")
        modules.chat_stats = False

    # Times keywords
    elif 'technoblade' in msg or 'techno' in msg:
        timed.tech_no()

    # Economy
    # Command inspired from Discord bot: UnbelievaBoat
    elif msg == '^balance' or msg == '^bal':  # Current status
        economy.get_current(uid)
    elif msg == '^work':  # Get money
        economy.work(uid)

    # Send help
    elif msg == '/help':
        modules.help_()

    # Detect if chat mode is on or not
    modules.chat(msg)


@app.route('/', methods=["POST"])
def server():
    '''
    Get data of a received message.
    '''
    data = request.get_json()  #  Get JSON data
    message = data['raw_message']  #  Get the message
    user_id = data['sender']['user_id']  # The user id of the sender
    if data['message_type'] == 'group':  # Only respond to group messages!
        main(message, user_id)  # Send to the get_keyword function to extract the keyword


# Run the script
if __name__ == '__main__':
    # Initialize the modules
    modules = Modules()
    timed = Modules.Timed()
    economy = Modules.Economy()
    modules.send(group_id, "Bot-PP now ONLINE!")  # Inform others that the bot is online

    app.run(host='127.0.0.1', port=9000)
