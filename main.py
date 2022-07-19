"""The main file for Superior Bot.
"""
# Import needed packages
from typing import NoReturn  # Doc string
from flask import Flask, request  # For building a simple server to receiving messages
import requests  # For sending requests to the bot
import json  # For managing Minecraft server query response
import time  # Used for timed keywords and others
import random  # For the economy module
import argparse  # Used to get arguments

app = Flask(__name__)  # Create the Flask APP
parser = argparse.ArgumentParser(description="Superior Bot manual")  # Create the parser

parser.add_argument('Group_ID', type=int, help='You QQ group ID')  # Add the argument for group ID
args = parser.parse_args()  # Parse the args

group_id = args.Group_ID  # Get the group ID


class Modules:
    """The modules for Superior Bot.
    """
    def __init__(self):
        self.random_sexy_api = 'https://api.lolicon.app/setu/v2?r18=0&num=5'  # Setu API for random sexy
        self.wotd_api = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'  # Wallpaper API from Bing
        self.news_api = 'http://c.m.163.com/nc/article/headline/T1348647853363/0-40.html'  # Headline news API from Netease

    def send(self, group_id: str, user_id: str, msg: str):
        """Sends msg to group_id while mentioning user_id.

        Args:
            group_id (str): The group's ID you want to send msg to.
            user_id (str): The user's ID you want to mention.
            msg (str): The message you want to send.
        """
        requests.get(f"http://127.0.0.1:5700/send_group_msg?group_id={group_id}&message=[CQ:at,qq={user_id}]\n{msg}")  # Do the request to send the message

    def send_public_message(self, group_id: str, msg: str):
        """Sends msg to group_id without mentioning others.

        Args:
            group_id (str): The group'd ID you want to send msg to.
            msg (str): The message you want to send.
        """
        requests.get(f"http://127.0.0.1:5700/send_group_msg?group_id={group_id}&message={msg}")  # Do the request to send the message

    def send_to(self, user_id: str, msg: str):
        """Sends a private msg to user_id.

        Args:
            user_id (str): The user's ID you want to send msg to.
            msg (str): The message you want to send.
        """
        requests.get(f"http://127.0.0.1:5700/send_private_msg?user_id={str(user_id)}&message={msg}")  # Do the request to send the message

    def calc(self, user_id: str, equation: str):
        """Calculates equation using eval(), and then sends the result to Group ID while mentioning user_id.

        Args:
            user_id (str): The user's ID you want to mention.
            equation (str): The equation to calculate.
        """
        try:
            self.calc_result = eval(equation)  # Get the result
        except Exception as e:  # Example: a/0
            self.send(group_id, user_id, e)
        else:  # Nothing wrong, send the results and return them
            self.send(group_id, user_id, self.calc_result)

    class Minecraft:
        """Minecraft modules for Superior Bot.
        """
        def __init__(self):
            self.minecraft_uuid_api = 'https://api.mojang.com/users/profiles/minecraft/'  # Get a player's UUID
            self.hypixel_api_key = '38bf6dbd-03e6-4c1d-ba9c-ce5f10903c45'  # Hypixel API key

        def mc_query(self, user_id: str, host: str):
            """Query whether a Minecraft server is online or not, then sends the result to Group ID while mentioning user_id. Using this module requires you to have an API for it running on your computer. If you encountered KeyError, please adjust the keys of the results.

            Args:
                user_id (str): The user's ID you want to mention.
                host (str): The Minecraft server's IP/URL.
            """
            try:
                self.mc_query_res = requests.get(f"http://127.0.0.1/json.php?host={host}&port=25565")  # Request to a PHP file with Apache to get the server's status
            except Exception:  # The query server is offline
                modules.send(group_id, user_id, "Query server is offline! Please notify admin!")
            self.mc_query_result = self.mc_query_res.json()  # Get JSON data

            # Get server details
            # ADJUST THESE BELOW IF YOU ENCOUNTERED KeyError!!!
            if self.mc_query_result['status'] == 'Online':
                self.mc_query_online = self.mc_query_result['status']
                self.mc_query_motd = self.mc_query_result['motd']['clean']
                self.mc_query_online_players = self.mc_query_result['players']['online']
                self.mc_query_max_players = self.mc_query_result['players']['max']
                modules.send(group_id, user_id, f"Status: {self.mc_query_online}\nMOTD: {self.mc_query_motd}\nOnline players: {self.mc_query_online_players}\nMax players: {self.mc_query_max_players}")  # Send results
            else:
                modules.send(group_id, user_id, 'The server is offline!')  # The server is offline

        def get_uuid(self, username: str):
            """Gets the UUID of a player and then stores it to get_uuid_uuid.

            Args:
                username (str): The player's username.
            """
            self.get_uuid_res = requests.get(self.minecraft_uuid_api + username)  # Get data from API
            self.get_uuid_result = self.get_uuid_res.json()  # Get JSON data

            self.get_uuid_uuid = self.get_uuid_result['id']  # UUID

        def hyp_basic_info(self, uid: str, username: str):
            """Get the basic Hypixel information of a player using their UUID, and then sends the results to Group ID while mentioning uid.

            Args:
                uid (str): The user's ID you want to mention.
                username (str): The player's username, which will be the input get get_uuid, which will get the player's UUID to be queried.
            """
            self.get_uuid(username)  # First, get UUID
            self.hyp_basic_info_res = requests.get(f'https://api.hypixel.net/player?key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}')  # Get basic info from Hypixel API
            self.hyp_basic_info_result = self.hyp_basic_info_res.json()  # Get JSON data from the response

            # Data
            try:
                self.hyp_basic_info_displayname = self.hyp_basic_info_result['player']['displayname']
                self.hyp_basic_info_rank = self.hyp_basic_info_result['player']['newPackageRank']
                self.hyp_basic_info_most_recent_game = self.hyp_basic_info_result['player']['mostRecentGameType']
            except KeyError:
                modules.send(group_id, uid, 'Something is wrong about your Hypixel profile. Please notice admin!')

            modules.send(group_id, uid, f'Hypixel basic information:\nDisplay name: {self.hyp_basic_info_displayname}\nRank: {self.hyp_basic_info_rank}\nMost recent game: {self.hyp_basic_info_most_recent_game}')

        def hyp_bedwars_info(self, user_id: str, username: str):
            """Get's a player's Hypixel bedwars status using their UUID, and then sends the result to Group ID while mentioning user_id.

            Args:
                user_id (str): The user's ID you want to mention.
                username (str): The player's username, which will be feed into get_uuid to get the player's UUID.
            """
            self.get_uuid(username)  # Get the player's UUID first
            self.hyp_bedwars_info_res = requests.get(f'https://api.hypixel.net/player?key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}')  # Get info from API
            self.hyp_bedwars_info_result = self.hyp_bedwars_info_res.json()  # Get JSON data

            # Data
            try:
                self.hyp_bedwars_info_exp = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['Experience']
                self.hyp_bedwars_info_games_played = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['games_played_bedwars']
                self.hyp_bedwars_info_coins = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['coins']
                self.hyp_bedwars_info_item_purchased = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['_items_purchased_bedwars']
                self.hyp_bedwars_info_kills = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['kills_bedwars']
                self.hyp_bedwars_info_final_kills = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['final_kills_bedwars']
                self.hyp_bedwars_info_deaths = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['deaths_bedwars']
                self.hyp_bedwars_info_final_deaths = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['final_deaths_bedwars']
                self.hyp_bedwars_info_beds_broken = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['beds_broken_bedwars']
                self.hyp_bedwars_info_beds_lost = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['beds_lost_bedwars']
                self.hyp_bedwars_info_games_won = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['wins_bedwars']
                self.hyp_bedwars_info_winstreak = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['winstreak']
                self.hyp_bedwars_info_games_lost = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['losses_bedwars']
            except KeyError:
                modules.send(group_id, user_id, 'Something is wrong with your Hypixel bedwars profile. Please notice admin!')

            modules.send(group_id, user_id, f'Bedwars data:\nBedwars experience: {self.hyp_bedwars_info_exp}\nBedwars coins: {self.hyp_bedwars_info_coins}\nBedwars played: {self.hyp_bedwars_info_games_played}\nItems purchased: {self.hyp_bedwars_info_item_purchased}\nKills: {self.hyp_bedwars_info_kills}\nFinal kills: {self.hyp_bedwars_info_final_kills}\nDeaths: {self.hyp_bedwars_info_deaths}\nFinal deaths: {self.hyp_bedwars_info_final_deaths}\nBeds broken: {self.hyp_bedwars_info_beds_broken}\nBeds lost: {self.hyp_bedwars_info_beds_lost}\nGames won: {self.hyp_bedwars_info_games_won}\nWinstreak: {self.hyp_bedwars_info_winstreak}\nGames lost: {self.hyp_bedwars_info_games_lost}')  # Send results

    def sexypic(self, user_id: str):
        """Fetches 5 sexy pics from Pixiv and them sends to result via private chat to user_id.

        Args:
            user_id (str): The user's ID you want to send the pics to.
        """
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
        """Sends Bing's wallpaper to Group ID without mentioning people.
        """
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
        """Get healine news from API and then sends it to chat without mentioning anyone.
        """
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
        """Timed keywords: Keywords that only works during a specific time.
        """
        def __init__(self):
            self.timed_localtime = time.ctime()  # Get current time

        def tech_no(self):
            """If it is Jul 1, respond to 'techno' or 'technoblade'. Sends the respond to Group ID.
            """
            if self.timed_localtime[4:10] == 'Jul  1':
                modules.send_public_message(group_id, 'Technoblade Never Dies!!!')  # TECHNOBLADE NEVER DIES!!!
    class Economy:
        """Economy modules, inspired by UnbelievaBoat the discord bot.
        """
        def get_current(self, uid: str):
            """Get uid's coins.

            Args:
                uid (str): The user's ID you want to get the coins.
            """
            uid = str(uid)  # Convert UID from int to str

            with open('storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.get_current_economy_stats = json.load(f)  # Get the coins this user have
                f.close()

            self.get_current_coins = self.get_current_economy_stats[uid]['coins']  # Get your coins

            modules.send(group_id, uid, f"Your current economy status:\nCoins: {self.get_current_coins}")  # Send the results

        def work(self, uid: str):
            """Work to earn coins.

            Args:
                uid (str): The user's ID who worked.
            """
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
        """Sends a help message to Group ID without mentioning anyone.
        """
        self.send_public_message(group_id, "Keywords:\n\nsb: Just a command to check whether the bot is alive or not.\n\n/query: Used to check the basic information about a Minecraft server. No response means that the server is offline.\nUsage: /query {Server address}\n\n/hyp-info: Get your Hypixel basic info.\nUsage: /hyp-info {Username}\n\n/bw: Get your Hypixel bedwars info.\nUsage: /bw {Username}\n\n/calc: Calculate something.\nUsage: /calc {Equation}\n\n/wotd: Get wallpaper of the day from Bing.\nUsage: /wotd\n\n/sexypic: Get a picture from Pixiv. The result will be send to you via private chat. You need to add the bot as your friend before using. USE BY CAUTION!\nUsage: /randomsexy\n\n/news: Get the headline news\nUsage: /news\n\n\n\nEconomy: No real use (for now)\nUsage:\n^balance/^bal: How much cash do you have?\n^work: Work for cash.. or lose them!\n\n\n\nTimed keywords:\n\nTechnoblade/Techno:\nAvailable: Jul 1")


class PersonalModules:
    """Modules for Superior Bot private chat.
    """
    def __init__(self):
        # APIs
        self.random_sexy_api = 'https://api.lolicon.app/setu/v2?r18=0&num=5'  # Setu API for random sexy
        self.wotd_api = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'  # Wallpaper API from Bing
        self.news_api = 'http://c.m.163.com/nc/article/headline/T1348647853363/0-40.html'  # Headline news API from Netease

    def send(self, user_id: str, msg: str):
        """Sends msg to user_id via private chat.

        Args:
            user_id (str): The user's ID you want to send msg to.
            msg (str): The message you want to send.
        """
        requests.get(f"http://127.0.0.1:5700/send_private_msg?user_id={str(user_id)}&message={msg}")  # Do the request to send the message

    def calc(self, user_id: str, equation: str):
        """Calculate equation using eval() and then sends the result.

        Args:
            user_id (str): The user's ID you want to send the result to.
            equation (str): The equation to be calculated.
        """
        try:
            self.calc_result = eval(equation)  # Get the result
        except Exception as e:  # Example: a/0
            self.send(user_id, e)
        else:  # Nothing wrong, send the results
            self.send(user_id, self.calc_result)

    class Minecraft:
        """Minecraft modules for Superior Bot private chat.
        """
        def __init__(self):
            self.minecraft_uuid_api = 'https://api.mojang.com/users/profiles/minecraft/'  # Get a player's UUID
            self.hypixel_api_key = '38bf6dbd-03e6-4c1d-ba9c-ce5f10903c45'  # Hypixel API key

        def mc_query(self, user_id: str, host: str):
            """Query whether Minecraft server host is online or not, and then sends the results to user_id.

            Args:
                user_id (str): The user's ID you want to send the results to.
                host (str): The IP of the Minecraft server to be queried.
            """
            try:
                self.mc_query_res = requests.get(f"http://127.0.0.1/json.php?host={host}&port=25565")  # Request to a PHP file with Apache to get the server's status
            except Exception:  # The query server is offline
                personal_modules.send(user_id, "Query server is offline! Please notify admin!")
            self.mc_query_result = self.mc_query_res.json()  # Get JSON data

            # Get server details
            if self.mc_query_result['status'] == 'Online':
                self.mc_query_online = self.mc_query_result['status']
                self.mc_query_motd = self.mc_query_result['motd']['clean']
                self.mc_query_online_players = self.mc_query_result['players']['online']
                self.mc_query_max_players = self.mc_query_result['players']['max']
                personal_modules.send(user_id, f"Status: {self.mc_query_online}\nMOTD: {self.mc_query_motd}\nOnline players: {self.mc_query_online_players}\nMax players: {self.mc_query_max_players}")  # Send results
            else:
                personal_modules.send(user_id, 'The server is offline!')  # Server offline

        def get_uuid(self, username: str):
            """Get username's UUID.

            Args:
                username (str): The player's name you want to get the UUID from.
            """
            self.get_uuid_res = requests.get(self.minecraft_uuid_api + username)  # Get data from API
            self.get_uuid_result = self.get_uuid_res.json()  # Get JSON data

            self.get_uuid_uuid = self.get_uuid_result['id']  # UUID

        def hyp_basic_info(self, uid: str, username: str):
            """Get username's basic Hypixel information and then sends it to uid.

            Args:
                uid (str): The user's ID you want to send the results to.
                username (str): The player's name.
            """
            self.get_uuid(username)  # First, get UUID
            self.hyp_basic_info_res = requests.get(f'https://api.hypixel.net/player?key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}')  # Get basic info from Hypixel API
            self.hyp_basic_info_result = self.hyp_basic_info_res.json()  # Get JSON data from the response

            # Data
            try:
                self.hyp_basic_info_displayname = self.hyp_basic_info_result['player']['displayname']
                self.hyp_basic_info_rank = self.hyp_basic_info_result['player']['newPackageRank']
                self.hyp_basic_info_most_recent_game = self.hyp_basic_info_result['player']['mostRecentGameType']
            except KeyError:
                personal_modules.send(uid, 'Something is wrong with your Hypixel profile. Please notice admin!')

            personal_modules.send(uid, f'Hypixel basic information:\nDisplay name: {self.hyp_basic_info_displayname}\nRank: {self.hyp_basic_info_rank}\nMost recent game: {self.hyp_basic_info_most_recent_game}')

        def hyp_bedwars_info(self, user_id: str, username: str):
            """Get username's basic Hypixel bedwars status and then sends it to user_id.

            Args:
                user_id (str): The user's ID you want to send the results to.
                username (str): The player's name.
            """
            self.get_uuid(username)
            self.hyp_bedwars_info_res = requests.get('https://api.hypixel.net/player?' + f'key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}')  # Get info from API
            self.hyp_bedwars_info_result = self.hyp_bedwars_info_res.json()  # Get JSON data

            # Bedwars data
            try:
                self.hyp_bedwars_info_exp = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['Experience']
                self.hyp_bedwars_info_games_played = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['games_played_bedwars']
                self.hyp_bedwars_info_coins = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['coins']
                self.hyp_bedwars_info_item_purchased = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['_items_purchased_bedwars']
                self.hyp_bedwars_info_kills = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['kills_bedwars']
                self.hyp_bedwars_info_final_kills = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['final_kills_bedwars']
                self.hyp_bedwars_info_deaths = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['deaths_bedwars']
                self.hyp_bedwars_info_final_deaths = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['final_deaths_bedwars']
                self.hyp_bedwars_info_beds_broken = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['beds_broken_bedwars']
                self.hyp_bedwars_info_beds_lost = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['beds_lost_bedwars']
                self.hyp_bedwars_info_games_won = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['wins_bedwars']
                self.hyp_bedwars_info_winstreak = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['winstreak']
                self.hyp_bedwars_info_games_lost = self.hyp_bedwars_info_result['player']['stats']['Bedwars']['losses_bedwars']
            except KeyError:
                personal_modules.send(user_id, 'Something is wrong with your Hypixel bedwars profile. Please notice admin!')

            personal_modules.send(user_id, f'Bedwars data:\nBedwars experience: {self.hyp_bedwars_info_exp}\nBedwars coins: {self.hyp_bedwars_info_coins}\nBedwars played: {self.hyp_bedwars_info_games_played}\nItems purchased: {self.hyp_bedwars_info_item_purchased}\nKills: {self.hyp_bedwars_info_kills}\nFinal kills: {self.hyp_bedwars_info_final_kills}\nDeaths: {self.hyp_bedwars_info_deaths}\nFinal deaths: {self.hyp_bedwars_info_final_deaths}\nBeds broken: {self.hyp_bedwars_info_beds_broken}\nBeds lost: {self.hyp_bedwars_info_beds_lost}\nGames won: {self.hyp_bedwars_info_games_won}\nWinstreak: {self.hyp_bedwars_info_winstreak}\nGames lost: {self.hyp_bedwars_info_games_lost}')  # Send results

    def sexypic(self, user_id: str):
        """Get 5 random sexy pic from Pixiv and then sends it to user_id

        Args:
            user_id (str): The user's ID you want to send the results to.
        """
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

    def wotd(self, uid: str):
        """Get Bing's wallpaper and then sends it to uid.

        Args:
            uid (str): The user's ID you want to send the wallpaper to.
        """
        self.wotd_res = requests.get(self.wotd_api)  # Get data
        if self.wotd_res.content:
            self.wotd_result = self.wotd_res.json()  # Get JSON data

        # Get image details and the image itself
        self.wotd_copyright = self.wotd_result['images'][0]['copyright']
        self.wotd_title = self.wotd_result['images'][0]['title']
        self.wotd_img_url = 'https://cn.bing.com' + self.wotd_result['images'][0]['url']

        self.send(uid, f"[CQ:image,file={self.wotd_img_url[:self.wotd_img_url.find('&rf')]}]")  # Send the image
        self.send(uid, f'Title: {self.wotd_title}\nCopyright: {self.wotd_copyright}')  # Send description

    def get_news(self, uid: str):
        """Get the headline news and then sends it to uid.

        Args:
            uid (str): The user's ID you want to send the news to.
        """
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
        """Timed keywords: Keywords that can only work during a specific time.
        """
        def __init__(self):
            self.timed_localtime = time.ctime()  # Get current time

        def tech_no(self, uid: str):
            """If today is Jul 1, respond to 'techno' or 'technoblade'.

            Args:
                uid (str): The user's ID you want to send the respond to.
            """
            if self.timed_localtime[4:10] == 'Jul  1':
                personal_modules.send(uid, 'Technoblade Never Dies!!!')  # TECHNOBLADE NEVER DIES!!!
    class Economy:
        """Superior Bot's Economy system for private chat. Inspired by UnbelievaBoat the discord bot.
        """
        def get_current(self, uid: str):
            """Get uid's current coins.

            Args:
                uid (str): The user's ID you want to get the coins from.
            """
            uid = str(uid)  # Convert UID from int to str

            with open('storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.get_current_economy_stats = json.load(f)  # Get the coins this user have
                f.close()

            self.get_current_coins = self.get_current_economy_stats[uid]['coins']  # Get your coins

            personal_modules.send(uid, f"Your current economy status:\nCoins: {self.get_current_coins}")  # Send the results

        def work(self, uid: str):
            """Work to earn coins, and then sends the results to uid.

            Args:
                uid (str): The user's ID you want to sends the results to.
            """
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

    def help_(self, uid: str):
        """Sends a help message to uid.

        Args:
            uid (str): The user's ID you want to send the help message.
        """
        self.send(uid, "Keywords:\n\nsb: Just a command to check whether the bot is alive or not.\n\n/query: Used to check the basic information about a Minecraft server. No response means that the server is offline.\nUsage: /query {Server address}\n\n/hyp-info: Get your Hypixel basic info.\nUsage: /hyp-info {Username}\n\n/bw: Get your Hypixel bedwars info.\nUsage: /bw {Username}\n\n/calc: Calculate something.\nUsage: /calc {Equation}\n\n/wotd: Get wallpaper of the day from Bing.\nUsage: /wotd\n\n/sexypic: Get a sexy picture from Pixiv. The result will be send to you via private chat. You need to add the bot as your friend before using. USE BY CAUTION!\nUsage: /randomsexy\n\n/news: Get the headline news\nUsage: /news\n\n\n\nEconomy: No real use (for now)\nUsage:\n^balance/^bal: How much cash do you have?\n^work: Work for cash.. or lose them!\n\n\n\nTimed keywords:\n\nTechnoblade/Techno:\nAvailable: Jul 1")


def main(msg: str, uid: str):
    """Get the keyword from msg and the sender's ID from the receive server, then do a correct response to it..

    Args:
        msg (str): The message someone sent.
        uid (str): The sender's ID.
    """
    msg = msg.lower()
    uid = str(uid)

    # Respond so that we know the bot is online
    if msg == 'sb':
        modules.send_public_message(group_id, '?')

    # Minecraft
    elif msg[0:6] == '/query':  # Minecraft server detect
        minecraft.mc_query(uid, msg[7:])
    elif msg[0:9] == '/hyp-info':  # Hypixel basic info
        minecraft.hyp_basic_info(uid, msg[10:])
    elif msg[0:3] == '/bw':  # Hypixel bedwars info
        minecraft.hyp_bedwars_info(uid, msg[4:])

    # Random images
    elif msg == '/sexypic':
        modules.sexypic(uid)
    elif msg == '/wotd':
        modules.wotd()

    # Calculator
    elif msg[0:5] == '/calc':
        modules.calc(msg[6:])

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


def personal_main(msg: str, uid: str):
    """Get the keyword from msg and the sender's ID from the receive server, then do a correct response to it.

    Args:
        msg (str): The message someone sent.
        uid (str): The sender's ID.
    """
    msg = msg.lower()
    uid = str(uid)

    # Respond so that we know the bot is online
    if msg == 'sb':
        personal_modules.send(uid, '?')

    # Minecraft
    elif msg[0:6] == '/query':  # Minecraft server detect
        personal_minecraft.mc_query(uid, msg[7:])
    elif msg[0:9] == '/hyp-info':  # Hypixel basic info
        personal_minecraft.hyp_basic_info(uid, msg[10:])
    elif msg[0:3] == '/bw':  # Hypixel bedwars info
        personal_minecraft.hyp_bedwars_info(uid, msg[4:])

    # Random images
    elif msg == '/sexypic':
        personal_modules.sexypic(uid)
    elif msg == '/wotd':
        personal_modules.wotd(uid)

    # Calculator
    elif msg[0:5] == '/calc':
        personal_modules.calc(uid, msg[6:])

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
    """Get data of a receive message.
    """
    data = request.get_json()  #  Get JSON data
    message = data['raw_message']  #  Get the message
    user_id = data['user_id']  # The user id of the sender
    if data['message_type'] == 'group':  # Only respond to group messages!
        main(message, user_id)  # Send to the get_keyword function to extract the keyword
    elif data['message_type'] == 'private':
        personal_main(message, user_id)


if __name__ == '__main__':
    """Run Superior Bot!
    """
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

    modules.send_public_message(group_id, "Superior Bot now ONLINE!")  # Inform others that the bot is online
    for user in users:
        personal_modules.send(user, 'Superior Bot now ONLINE!')

    app.run(host='127.0.0.1', port=9000)
