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

app = Flask(__name__)  # Create the Flask APP
parser = argparse.ArgumentParser(description="Bot++ manual")  # Create the parser

parser.add_argument('Group_ID', type=int, help='You QQ group ID')  # Add the argument for group ID
args = parser.parse_args()  # Parse the args

group_id = args.Group_ID  # Get the group ID


class Modules:
    '''
    Modules for the QQ bot - You can always add more!
    '''
    def __init__(self):
        '''
        Initialize some variables.
        '''
        # APIs
        self.random_sexy_api = 'https://api.lolicon.app/setu/v2?r18=0&num=1'  # API for random sexy
        self.wotd_api = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'  # Wallpaper API from Bing
        self.news_api = 'http://c.m.163.com/nc/article/headline/T1348647853363/0-40.html'  # Headline news API from Netease

    def send(self, group_id, user_id, msg):
        '''
        Sends a message to the group.
        '''
        requests.get(f"http://127.0.0.1:5700/send_group_msg?group_id={str(group_id)}&message=[CQ:at,qq={user_id}]\n{msg}")  # Do the request to send the message

    def send_public_message(self, group_id, msg):
        '''
        Sends a message to the group without @ing people.
        '''
        requests.get(f"http://127.0.0.1:5700/send_group_msg?group_id={str(group_id)}&message={msg}")  # Do the request to send the message

    def send_to(self, user_id, msg):
        '''
        Sends a message to someone.
        '''
        requests.get(f"http://127.0.0.1:5700/send_private_msg?user_id={str(user_id)}&message={msg}")  # Do the request to send the message

    def calc(self, user_id, equation):
        '''
        Calculate something and send the result.
        '''
        try:
            self.calc_result = eval(equation[6:])  # Get the result
        except Exception as e:  # Example: a/0
            self.send(group_id, user_id, e)
        else:  # Nothing wrong, send the results
            self.send(group_id, user_id, self.calc_result)

    class Minecraft:
        def __init__(self):
            '''
            Initialize some APIs.
            '''
            self.minecraft_uuid_api = 'https://api.mojang.com/users/profiles/minecraft/'  # Get a player's UUID
            self.hypixel_api_key = '38bf6dbd-03e6-4c1d-ba9c-ce5f10903c45'  # Hypixel API key

        def mc_query(self, user_id, host):
            '''
            Detect whether a Minecraft server is online or not.
            '''
            try:
                self.mc_query_res = requests.get(f"http://127.0.0.1/mcq/json.php?host={host}&port=25565")  # Request to a PHP file with Apache to get the server's status
            except Exception:  # The query server is offline
                modules.send(group_id, user_id, "Query server is offline! Please notify admin!")
            # Write data into a json file to convert plain text to JSON data
            with open('storage/mcq.json', 'w') as f:
                f.write(self.mc_query_res.text)  # Store plain text
                f.close()

            with open('storage/mcq.json', 'r') as f:
                self.mc_query_data = json.load(f)  # Read as JSON data
                f.close()

            # Get server details
            self.mc_query_online = self.mc_query_data['status']
            self.mc_query_motd = self.mc_query_data['motd']['clean']
            self.mc_query_online_players = self.mc_query_data['players']['online']
            self.mc_query_max_players = self.mc_query_data['players']['max']
            modules.send(group_id, user_id, f"Status: {self.mc_query_online}\nMOTD: {self.mc_query_motd}\nOnline players: {self.mc_query_online_players}\nMax players: {self.mc_query_max_players}")  # Send results

            # Flush query data
            os.system('rm -rf storage/mcq.json')
            os.system('touch storage/mcq.json')

        def get_uuid(self, username):
            '''
            Get the UUID of a player.
            '''
            self.get_uuid_res = requests.get(self.minecraft_uuid_api + username)

            with open('storage/uuid.json', 'w') as f:
                f.write(self.get_uuid_res.text)
                f.close()
            
            with open('storage/uuid.json', 'r') as f:
                self.get_uuid_result = json.load(f)
                f.close()

            self.get_uuid_uuid = self.get_uuid_result['id']

            os.system('rm -rf storage/uuid.json')
            os.system('touch storage/uuid.json')

        def hyp_info(self, user_id, username):
            '''
            Get the basic information of a player in Hypixel.
            '''
            self.get_uuid(username)
            self.hyp_info_res = requests.get('https://api.hypixel.net/player?' + f'key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}')

            with open('storage/hyp.json', 'w') as f:
                f.write(self.hyp_info_res.text)
                f.close()
            
            with open('storage/hyp.json', 'r') as f:
                self.hyp_info_result = json.load(f)
                f.close()

            # Player data
            self.hyp_displayname = self.hyp_info_result['player']['displayname']  # Display name

            # Bedwars data
            self.hyp_bedwars_exp = self.hyp_info_result['player']['stats']['Bedwars']['Experience']
            self.hyp_bedwars_games_played = self.hyp_info_result['player']['stats']['Bedwars']['games_played_bedwars']
            self.hyp_bedwars_coins = self.hyp_info_result['player']['stats']['Bedwars']['coins']
            self.hyp_bedwars_item_purchased = self.hyp_info_result['player']['stats']['Bedwars']['_items_purchased_bedwars']
            self.hyp_bedwars_kills = self.hyp_info_result['player']['stats']['Bedwars']['kills_bedwars']
            self.hyp_bedwars_final_kills = self.hyp_info_result['player']['stats']['Bedwars']['final_kills_bedwars']
            self.hyp_bedwars_deaths = self.hyp_info_result['player']['stats']['Bedwars']['deaths_bedwars']
            self.hyp_bedwars_final_deaths = self.hyp_info_result['player']['stats']['Bedwars']['final_deaths_bedwars']
            # TODO: Beds broken
            self.hyp_bedwars_beds_lost = self.hyp_info_result['player']['stats']['Bedwars']['beds_lost_bedwars']
            self.hyp_bedwars_games_won = self.hyp_info_result['player']['stats']['Bedwars']['wins_bedwars']
            self.hyp_bedwars_winstreak = self.hyp_info_result['player']['stats']['Bedwars']['winstreak']
            self.hyp_bedwars_games_lost = self.hyp_info_result['player']['stats']['Bedwars']['losses_bedwars']

            modules.send(group_id, user_id, f'Hypixel player information:\n\nPlayer data:\nPlayer display name: {self.hyp_displayname}\n\nBedwars data:\nBedwars experience: {self.hyp_bedwars_exp}\nBedwars coins: {self.hyp_bedwars_coins}\nBedwars played: {self.hyp_bedwars_games_played}\nItems purchased: {self.hyp_bedwars_item_purchased}\nKills: {self.hyp_bedwars_kills}\nFinal kills: {self.hyp_bedwars_final_kills}\nDeaths: {self.hyp_bedwars_deaths}\nFinal deaths: {self.hyp_bedwars_final_deaths}\nGames won: {self.hyp_bedwars_games_won}\nWinstreak: {self.hyp_bedwars_winstreak}\nGames lost: {self.hyp_bedwars_games_lost}')

            # Flush cache
            os.system('rm -rf storage/hyp.json')
            os.system('touch storage/hyp.json')

    def random_sexy(self, user_id):
        '''
        Get an random sexy image from Pixiv and send it to chat.
        '''
        self.random_sexy_res = requests.get(self.random_sexy_api)  # Get raw data from API
        self.random_sexy_result = self.random_sexy_res.json()  # Convert raw data into JSON data

        # Get data
        self.random_sexy_painter = self.random_sexy_result['data'][0]['author']
        self.random_sexy_pid = self.random_sexy_result['data'][0]['pid']
        self.random_sexy_title = self.random_sexy_result['data'][0]['title']
        self.random_sexy_img_url = self.random_sexy_result['data'][0]['urls']['original']
        self.random_sexy_file_type = self.random_sexy_result['data'][0]['ext']

        # Send to the user
        self.send_to(user_id, f'[CQ:image,file={self.random_sexy_img_url}]')  # Send image
        self.send_to(user_id, f'Author: {self.random_sexy_painter}\nPID: {self.random_sexy_pid}\nTitle: {self.random_sexy_title}\nImage URL: {self.random_sexy_img_url}\nFile type: {self.random_sexy_file_type}')  # Send description

    def wotd(self):
        '''
        Get the wallpaper of the day and send it to chat.
        '''
        self.wotd_res = requests.get(self.wotd_api)  # Get data
        if self.wotd_res.content:
            self.wotd_result = self.wotd_res.json()  # Get JSON data

        # Get image details and the image itself
        self.wotd_copyright = self.wotd_result['images'][0]['copyright']
        self.wotd_title = self.wotd_result['images'][0]['title']
        self.wotd_img_url = 'https://cn.bing.com' + self.wotd_result['images'][0]['url']

        self.send_public_message(group_id, f"[CQ:image,file={self.wotd_img_url[:self.wotd_img_url.find('&rf')]}]")  # Send the image
        self.send_public_message(group_id, f'Title: {self.wotd_title}\nCopyright: {self.wotd_copyright}')  # Send description

    def get_news(self):
        '''
        Get headline news.
        '''
        self.get_news_res = requests.get(self.news_api)  # Get data
        self.get_news_result = self.get_news_res.json()  # Get JSON data

        # Get details
        self.get_news_news1 = self.get_news_result['T1348647853363'][0]['title']
        self.get_news_news2 = self.get_news_result['T1348647853363'][1]['title']
        self.get_news_news3 = self.get_news_result['T1348647853363'][2]['title']
        self.get_news_news4 = self.get_news_result['T1348647853363'][3]['title']
        self.get_news_news5 = self.get_news_result['T1348647853363'][4]['title']

        self.send_public_message(group_id, f"1. {self.get_news_news1}\n2. {self.get_news_news2}\n3. {self.get_news_news3}\n4. {self.get_news_news4}\n5. {self.get_news_news5}")  # Send result

    class Timed:
        '''
        Timed keywords.
        '''
        def __init__(self):
            self.timed_localtime = time.ctime()  # Get current time

        def tech_no(self):
            '''
            Technoblade! Noooooooooo!
            '''
            if self.timed_localtime[4:10] == 'Jul  1':
                modules.send_public_message(group_id, 'Technoblade Never Dies!!!')  # TECHNOBLADE NEVER DIES!!!
    class Economy:
        '''
        Economy system in chat.
        '''
        def get_current(self, uid):
            '''
            Get the current economy status of someone.
            '''
            uid = str(uid)  # Convert UID from int to str

            with open('storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.get_current_economy_stats = json.load(f)  # Get the coins this user have
                f.close()

            self.get_current_coins = self.get_current_economy_stats[uid]['coins']  # Get your coins

            modules.send(group_id, uid, f"Your current economy status:\nCoins: {self.get_current_coins}")  # Send the results

        def work(self, uid):
            '''
            Earn coins!
            '''
            uid = str(uid)  # Convert UID from int to str

            self.work_income = random.randint(-500, 1000)  # Random income

            with open('storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.work_economy_stats = json.load(f)
                f.close()

            coins = self.work_economy_stats[uid]['coins']  # Get your coins
            coins = int(coins)  # Convert coins to int so that we can add the income
            coins += self.work_income  # Change current status
            coins = str(coins)  # Convert coins to str so that we can dump them
            self.work_economy_stats[uid]['coins'] = coins  # Save it to the dict

            with open('storage/economy.json', 'w') as f:  # Dump the current status
                json.dump(self.work_economy_stats, f)
                f.close()

            if self.work_income > 0:  # You got some money!
                modules.send(group_id, uid, f"You got ${self.work_income}.")
            elif self.work_income < 0:  # Too bad!
                modules.send(group_id, uid, f"You lost ${self.work_income}.")
            elif self.work_income == 0:
                modules.send(group_id, uid, 'Nothing happened...')

    def help_(self):
        '''
        Send a help message.
        '''
        self.send_public_message(group_id, "Keywords:\n\nbpp: Just a command to check whether the bot is alive or not.\n\n/query: Used to check the basic information about a Minecraft server. No response means that the server is offline.\nUsage: /query {Server address}\n\n/hyp-stats: Get your Hypixel status.\nUsage: /hyp-stats {Username}\n\n/calc: Calculate something.\nUsage: /calc {Equation}\n\n/wotd: Get wallpaper of the day from Bing.\nUsage: /wotd\n\n/randomsexy: Get a sexy picture from Pixiv. The result will be send to you via private chat. You need to add the bot as your friend before using. USE BY CAUTION!\nUsage: /randomsexy\n\n/news: Get the headline news\nUsage: /news\n\n\n\nEconomy: No real use (for now)\nUsage:\n^balance/^bal: How much cash do you have?\n^work: Work for cash.. or lose them!\n\n\n\nTimed keywords:\n\nTechnoblade/Techno:\nAvailable: Jul 1")


class PersonalModules:
    '''
    Modules for the QQ bot - You can always add more!
    '''
    def __init__(self):
        '''
        Initialize some variables.
        '''
        # APIs
        self.random_sexy_api = 'https://api.lolicon.app/setu/v2?r18=0&num=1'  # API for random sexy
        self.wotd_api = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'  # Wallpaper API from Bing
        self.news_api = 'http://c.m.163.com/nc/article/headline/T1348647853363/0-40.html'  # Headline news API from Netease

    def send(self, user_id, msg):
        '''
        Sends a message to someone.
        '''
        requests.get(f"http://127.0.0.1:5700/send_private_msg?user_id={str(user_id)}&message={msg}")  # Do the request to send the message

    def calc(self, user_id, equation):
        '''
        Calculate something and send the result.
        '''
        try:
            self.calc_result = eval(equation[6:])  # Get the result
        except Exception as e:  # Example: a/0
            self.send(user_id, e)
        else:  # Nothing wrong, send the results
            self.send(user_id, self.calc_result)

    class Minecraft:
        def __init__(self):
            '''
            Initialize some APIs.
            '''
            self.minecraft_uuid_api = 'https://api.mojang.com/users/profiles/minecraft/'  # Get a player's UUID
            self.hypixel_api_key = '38bf6dbd-03e6-4c1d-ba9c-ce5f10903c45'  # Hypixel API key

        def mc_query(self, user_id, host):
            '''
            Detect whether a Minecraft server is online or not.
            '''
            try:
                self.mc_query_res = requests.get(f"http://127.0.0.1/mcq/json.php?host={host}&port=25565")  # Request to a PHP file with Apache to get the server's status
            except Exception:  # The query server is offline
                personal_modules.send(user_id, "Query server is offline! Please notify admin!")
            # Write data into a json file to convert plain text to JSON data
            with open('storage/mcq.json', 'w') as f:
                f.write(self.mc_query_res.text)  # Store plain text
                f.close()

            with open('storage/mcq.json', 'r') as f:
                self.mc_query_data = json.load(f)  # Read as JSON data
                f.close()

            # Get server details
            self.mc_query_online = self.mc_query_data['status']
            self.mc_query_motd = self.mc_query_data['motd']['clean']
            self.mc_query_online_players = self.mc_query_data['players']['online']
            self.mc_query_max_players = self.mc_query_data['players']['max']
            personal_modules.send(user_id, f"Status: {self.mc_query_online}\nMOTD: {self.mc_query_motd}\nOnline players: {self.mc_query_online_players}\nMax players: {self.mc_query_max_players}")  # Send results

            # Flush query data
            os.system('rm -rf storage/mcq.json')
            os.system('touch storage/mcq.json')

        def get_uuid(self, username):
            '''
            Get the UUID of a player.
            '''
            self.get_uuid_res = requests.get(self.minecraft_uuid_api + username)

            with open('storage/uuid.json', 'w') as f:
                f.write(self.get_uuid_res.text)
                f.close()
            
            with open('storage/uuid.json', 'r') as f:
                self.get_uuid_result = json.load(f)
                f.close()

            self.get_uuid_uuid = self.get_uuid_result['id']

            os.system('rm -rf storage/uuid.json')
            os.system('touch storage/uuid.json')

        def hyp_info(self, user_id, username):
            '''
            Get the basic information of a player in Hypixel.
            '''
            self.get_uuid(username)
            self.hyp_info_res = requests.get('https://api.hypixel.net/player?' + f'key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}')

            with open('storage/hyp.json', 'w') as f:
                f.write(self.hyp_info_res.text)
                f.close()
            
            with open('storage/hyp.json', 'r') as f:
                self.hyp_info_result = json.load(f)
                f.close()

            # Player data
            self.hyp_displayname = self.hyp_info_result['player']['displayname']  # Display name

            # Bedwars data
            self.hyp_bedwars_exp = self.hyp_info_result['player']['stats']['Bedwars']['Experience']
            self.hyp_bedwars_games_played = self.hyp_info_result['player']['stats']['Bedwars']['games_played_bedwars']
            self.hyp_bedwars_coins = self.hyp_info_result['player']['stats']['Bedwars']['coins']
            self.hyp_bedwars_item_purchased = self.hyp_info_result['player']['stats']['Bedwars']['_items_purchased_bedwars']
            self.hyp_bedwars_kills = self.hyp_info_result['player']['stats']['Bedwars']['kills_bedwars']
            self.hyp_bedwars_final_kills = self.hyp_info_result['player']['stats']['Bedwars']['final_kills_bedwars']
            self.hyp_bedwars_deaths = self.hyp_info_result['player']['stats']['Bedwars']['deaths_bedwars']
            self.hyp_bedwars_final_deaths = self.hyp_info_result['player']['stats']['Bedwars']['final_deaths_bedwars']
            # TODO: Beds broken
            self.hyp_bedwars_beds_lost = self.hyp_info_result['player']['stats']['Bedwars']['beds_lost_bedwars']
            self.hyp_bedwars_games_won = self.hyp_info_result['player']['stats']['Bedwars']['wins_bedwars']
            self.hyp_bedwars_winstreak = self.hyp_info_result['player']['stats']['Bedwars']['winstreak']
            self.hyp_bedwars_games_lost = self.hyp_info_result['player']['stats']['Bedwars']['losses_bedwars']

            personal_modules.send(user_id, f'Hypixel player information:\n\nPlayer data:\nPlayer display name: {self.hyp_displayname}\n\nBedwars data:\nBedwars experience: {self.hyp_bedwars_exp}\nBedwars coins: {self.hyp_bedwars_coins}\nBedwars played: {self.hyp_bedwars_games_played}\nItems purchased: {self.hyp_bedwars_item_purchased}\nKills: {self.hyp_bedwars_kills}\nFinal kills: {self.hyp_bedwars_final_kills}\nDeaths: {self.hyp_bedwars_deaths}\nFinal deaths: {self.hyp_bedwars_final_deaths}\nGames won: {self.hyp_bedwars_games_won}\nWinstreak: {self.hyp_bedwars_winstreak}\nGames lost: {self.hyp_bedwars_games_lost}')

            # Flush cache
            os.system('rm -rf storage/hyp.json')
            os.system('touch storage/hyp.json')

    def random_sexy(self, user_id):
        '''
        Get an random sexy image from Pixiv and send it to chat.
        '''
        self.random_sexy_res = requests.get(self.random_sexy_api)  # Get raw data from API
        self.random_sexy_result = self.random_sexy_res.json()  # Convert raw data into JSON data

        # Get data
        self.random_sexy_painter = self.random_sexy_result['data'][0]['author']
        self.random_sexy_pid = self.random_sexy_result['data'][0]['pid']
        self.random_sexy_title = self.random_sexy_result['data'][0]['title']
        self.random_sexy_img_url = self.random_sexy_result['data'][0]['urls']['original']
        self.random_sexy_file_type = self.random_sexy_result['data'][0]['ext']

        # Send to the user
        self.send(user_id, f'[CQ:image,file={self.random_sexy_img_url}]')  # Send image
        self.send(user_id, f'Author: {self.random_sexy_painter}\nPID: {self.random_sexy_pid}\nTitle: {self.random_sexy_title}\nImage URL: {self.random_sexy_img_url}\nFile type: {self.random_sexy_file_type}')  # Send description

    def wotd(self, uid):
        '''
        Get the wallpaper of the day and send it to chat.
        '''
        self.wotd_res = requests.get(self.wotd_api)  # Get data
        if self.wotd_res.content:
            self.wotd_result = self.wotd_res.json()  # Get JSON data

        # Get image details and the image itself
        self.wotd_copyright = self.wotd_result['images'][0]['copyright']
        self.wotd_title = self.wotd_result['images'][0]['title']
        self.wotd_img_url = 'https://cn.bing.com' + self.wotd_result['images'][0]['url']

        self.send(uid, f"[CQ:image,file={self.wotd_img_url[:self.wotd_img_url.find('&rf')]}]")  # Send the image
        self.send(uid, f'Title: {self.wotd_title}\nCopyright: {self.wotd_copyright}')  # Send description

    def get_news(self, uid):
        '''
        Get headline news.
        '''
        self.get_news_res = requests.get(self.news_api)  # Get data
        self.get_news_result = self.get_news_res.json()  # Get JSON data

        # Get details
        self.get_news_news1 = self.get_news_result['T1348647853363'][0]['title']
        self.get_news_news2 = self.get_news_result['T1348647853363'][1]['title']
        self.get_news_news3 = self.get_news_result['T1348647853363'][2]['title']
        self.get_news_news4 = self.get_news_result['T1348647853363'][3]['title']
        self.get_news_news5 = self.get_news_result['T1348647853363'][4]['title']

        self.send(uid, f"1. {self.get_news_news1}\n2. {self.get_news_news2}\n3. {self.get_news_news3}\n4. {self.get_news_news4}\n5. {self.get_news_news5}")  # Send result

    class Timed:
        '''
        Timed keywords.
        '''
        def __init__(self):
            self.timed_localtime = time.ctime()  # Get current time

        def tech_no(self, uid):
            '''
            Technoblade! Noooooooooo!
            '''
            if self.timed_localtime[4:10] == 'Jul  1':
                personal_modules.send(uid, 'Technoblade Never Dies!!!')  # TECHNOBLADE NEVER DIES!!!
    class Economy:
        '''
        Economy system in chat.
        '''
        def get_current(self, uid):
            '''
            Get the current economy status of someone.
            '''
            uid = str(uid)  # Convert UID from int to str

            with open('storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.get_current_economy_stats = json.load(f)  # Get the coins this user have
                f.close()

            self.get_current_coins = self.get_current_economy_stats[uid]['coins']  # Get your coins

            personal_modules.send(uid, f"Your current economy status:\nCoins: {self.get_current_coins}")  # Send the results

        def work(self, uid):
            '''
            Earn coins!
            '''
            uid = str(uid)  # Convert UID from int to str

            self.work_income = random.randint(-500, 1000)  # Random income

            with open('storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.work_economy_stats = json.load(f)
                f.close()

            coins = self.work_economy_stats[uid]['coins']  # Get your coins
            coins = int(coins)  # Convert coins to int so that we can add the income
            coins += self.work_income  # Change current status
            coins = str(coins)  # Convert coins to str so that we can dump them
            self.work_economy_stats[uid]['coins'] = coins  # Save it to the dict

            with open('storage/economy.json', 'w') as f:  # Dump the current status
                json.dump(self.work_economy_stats, f)
                f.close()

            if self.work_income > 0:  # You got some money!
                personal_modules.send(uid, f"You got ${self.work_income}.")
            elif self.work_income < 0:  # Too bad!
                personal_modules.send(uid, f"You lost ${self.work_income}.")
            elif self.work_income == 0:
                personal_modules.send(uid, 'Nothing happened...')

    def help_(self, uid):
        '''
        Send a help message.
        '''
        self.send(uid, "Keywords:\n\nbpp: Just a command to check whether the bot is alive or not.\n\n/query: Used to check the basic information about a Minecraft server. No response means that the server is offline.\nUsage: /query {Server address}\n\n/hyp-stats: Get your Hypixel status.\nUsage: /hyp-stats {Username}\n\n/calc: Calculate something.\nUsage: /calc {Equation}\n\n/wotd: Get wallpaper of the day from Bing.\nUsage: /wotd\n\n/randomsexy: Get a sexy picture from Pixiv. The result will be send to you via private chat. You need to add the bot as your friend before using. USE BY CAUTION!\nUsage: /randomsexy\n\n/news: Get the headline news\nUsage: /news\n\n\n\nEconomy: No real use (for now)\nUsage:\n^balance/^bal: How much cash do you have?\n^work: Work for cash.. or lose them!\n\n\n\nTimed keywords:\n\nTechnoblade/Techno:\nAvailable: Jul 1")


def main(msg, uid):
    '''
    Get the keyword of a sentence, then send a proper request to the server.
    '''
    msg = msg.lower()
    uid = str(uid)

    # Wordlist for insult detection
    with open('insults.txt', 'r') as f:
        insults = f.readlines()
        insults = [i.strip('\n') for i in insults]
        f.close()
    # Insults detection
    for i in insults:
        if i in msg:
            modules.send(group_id, uid, 'Language!')

    # Respond so that we know the bot is online
    if msg == 'bpp':
        modules.send(group_id, '?')

    # Minecraft
    # Minecraft server detect
    elif msg[0:6] == '/query':
        minecraft.mc_query(msg[7:])
    elif msg[0:10] == '/hyp-stats':
        minecraft.hyp_info(msg[11:])

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


def personal_main(msg, uid):
    '''
    Get the keyword of a sentence, then send a proper request to the server.
    '''
    msg = msg.lower()
    uid = str(uid)

    # Wordlist for insult detection
    with open('insults.txt', 'r') as f:
        insults = f.readlines()
        insults = [i.strip('\n') for i in insults]
        f.close()
    # Insults detection
    for i in insults:
        if i in msg:
            modules.send(group_id, uid, 'Language!')

    # Respond so that we know the bot is online
    if msg == 'bpp':
        personal_modules.send(uid, '?')

    # Minecraft
    # Minecraft server detect
    elif msg[0:6] == '/query':
        personal_minecraft.mc_query(uid, msg[7:])
    elif msg[0:10] == '/hyp-stats':
        personal_minecraft.hyp_info(uid, msg[11:])

    # Random images
    elif msg == '/randomsexy':
        personal_modules.random_sexy(uid)
    elif msg == '/wotd':
        personal_modules.wotd(uid)

    # Calculator
    elif msg[0:5] == '/calc':
        personal_modules.calc(uid, msg)

    # News
    elif msg == '/news':
        personal_modules.get_news(uid)

    # Times keywords
    elif 'technoblade' in msg or 'techno' in msg:
        personal_timed.tech_no(uid)

    # Economy
    # Command inspired from Discord bot: UnbelievaBoat
    elif msg == '^balance' or msg == '^bal':  # Current status
        personal_economy.get_current(uid)
    elif msg == '^work':  # Get money
        personal_economy.work(uid)

    # Send help
    elif msg == '/help':
        personal_modules.help_(uid)


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
    elif data['message_type'] == 'private':
        personal_main(message, user_id)


# Run the script
if __name__ == '__main__':
    # Initialize the modules for groups
    modules = Modules()
    minecraft = Modules.Minecraft()
    timed = Modules.Timed()
    economy = Modules.Economy()

    # Initialize the modules for personal
    personal_modules = PersonalModules()
    personal_minecraft = PersonalModules.Minecraft()
    personal_timed = PersonalModules.Timed()
    personal_economy = PersonalModules.Economy()

    with open('users.txt', 'r') as f:
        users = f.readlines()
        users = [i.strip('\n') for i in users]
        f.close()

    modules.send_public_message(group_id, "Bot-PP now ONLINE!")  # Inform others that the bot is online
    for i in users:
        personal_modules.send(i, 'Bot-PP now ONLINE!')

    app.run(host='127.0.0.1', port=9000)
