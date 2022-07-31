"""The modules for Superior Bot (English).
"""
# Import needed packages
import profile
import requests  # For sending requests to the bot
import json  # For managing Minecraft server query response
import time  # Used for timed keywords and others
import random  # For the economy module


class Modules:
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

    class Minecraft:
        """Minecraft modules for Superior Bot.
        """
        def __init__(self):
            self.minecraft_uuid_api = 'https://api.mojang.com/users/profiles/minecraft/'  # Get a player's UUID
            self.hypixel_api_key = '38bf6dbd-03e6-4c1d-ba9c-ce5f10903c45'  # Hypixel API key

        def mc_query(self, group_id: str, user_id: str, host: str):
            """Query whether a Minecraft server is online or not, then sends the result to group_id while mentioning user_id. Using this module requires you to have an API for it running on your computer. If you encountered KeyError, please adjust the keys of the results.

            Args:
                group_id (str): The group's ID you want to send the result to.
                user_id (str): The user's ID you want to mention.
                host (str): The Minecraft server's IP/URL.
            """
            modules.send(group_id, user_id, "Received, processing...")
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
                modules.send(group_id, user_id, f"""Status: {self.mc_query_online}

MOTD: {self.mc_query_motd}
Online players: {self.mc_query_online_players}
Max players: {self.mc_query_max_players}""")  # Send results
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

        def hyp_basic_info(self, group_id: str, uid: str, username: str):
            """Get the basic Hypixel information of a player using their UUID, and then sends the results to group_id while mentioning uid.

            Args:
                group_id (str): The group's ID you want to send the result to.
                uid (str): The user's ID you want to mention.
                username (str): The player's username, which will be the input get get_uuid, which will get the player's UUID to be queried.
            """
            modules.send(group_id, uid, "Received, processing...")
            self.get_uuid(username)  # First, get UUID
            self.hyp_basic_info_res = requests.get(f'https://api.hypixel.net/player?key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}')  # Get basic info from Hypixel API
            self.hyp_basic_info_result = self.hyp_basic_info_res.json()  # Get JSON data from the response
            self.hyp_basic_info_guild_res = requests.get(f"https://api.hypixel.net/guild?key={self.hypixel_api_key}&player={self.get_uuid_uuid}")  # Get guild info
            self.hyp_basic_info_guild_result = self.hyp_basic_info_guild_res.json()  # Guild data in JSON

            # Data
            try:
                self.hyp_basic_info_displayname = self.hyp_basic_info_result['player']['displayname']
                self.hyp_basic_info_karma = self.hyp_basic_info_result['player']['karma']
                self.hyp_basic_info_rank = self.hyp_basic_info_result['player']['newPackageRank']
                self.hyp_basic_info_guild = self.hyp_basic_info_guild_result['guild']['name']
                self.hyp_basic_info_most_recent_game = self.hyp_basic_info_result['player']['mostRecentGameType']
                self.hyp_basic_info_pet = self.hyp_basic_info_result['player']['currentPet']
                self.hyp_basic_info_gadget = self.hyp_basic_info_result['player']['currentGadget']
                self.hyp_basic_info_language = self.hyp_basic_info_result['player']['userLanguage']
            except KeyError:
                self.hyp_basic_info_most_recent_game = 'SKYBLOCK'
                self.hyp_basic_info_pet = 'NONE'
                self.hyp_basic_info_gadget = 'NONE'
                self.hyp_basic_info_language = 'NONE'

            modules.send(group_id, uid, f"""Hypixel basic information:

Display name: {self.hyp_basic_info_displayname}
Karma: {self.hyp_basic_info_karma}
Rank: {self.hyp_basic_info_rank}
Guild: {self.hyp_basic_info_guild}
Most recent game: {self.hyp_basic_info_most_recent_game}
Current pet: {self.hyp_basic_info_pet}
Current gadget: {self.hyp_basic_info_gadget}
Language: {self.hyp_basic_info_language}""")

        def hyp_bedwars_info(self, group_id: str, user_id: str, username: str):
            """Get's a player's Hypixel bedwars status using their UUID, and then sends the result to group_id while mentioning user_id.

            Args:
                group_id (str): The group's ID you want to send the result to.
                user_id (str): The user's ID you want to mention.
                username (str): The player's username, which will be feed into get_uuid to get the player's UUID.
            """
            modules.send(group_id, user_id, "Received, processing...")
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

            modules.send(group_id, user_id, f"""Bedwars data:

Bedwars experience: {self.hyp_bedwars_info_exp}
Bedwars coins: {self.hyp_bedwars_info_coins}
Bedwars played: {self.hyp_bedwars_info_games_played}
Items purchased: {self.hyp_bedwars_info_item_purchased}

Kills: {self.hyp_bedwars_info_kills}
Final kills: {self.hyp_bedwars_info_final_kills}
Deaths: {self.hyp_bedwars_info_deaths}
Final deaths: {self.hyp_bedwars_info_final_deaths}

Beds broken: {self.hyp_bedwars_info_beds_broken}
Beds lost: {self.hyp_bedwars_info_beds_lost}
Games won: {self.hyp_bedwars_info_games_won}
Winstreak: {self.hyp_bedwars_info_winstreak}
Games lost: {self.hyp_bedwars_info_games_lost}""")  # Send results

        def hyp_skyblock_list(self, group_id: str, uid: str, username: str):
            """List the profile IDs.

            Args:
                group_id (str): The group's ID you want to send the results to.
                uid (str): The user's ID you want to mention.
                username (str): The player's username, which will be feed into get_uuid().
            """
            modules.send(group_id, uid, "Received, processing...")
            self.get_uuid(username)  # Get UUID
            self.hyp_skyblock_list_res = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}")
            self.hyp_skyblock_list_result = self.hyp_skyblock_list_res.json()

            for i in range(0, 2):  # 3 profile for each player
                self.profile_id = self.hyp_skyblock_list_result['profiles'][i]['profile_id']
                self.profile_cute_name = self.hyp_skyblock_list_result['profiles'][i]['cute_name']
                modules.send(group_id, uid, f"{self.profile_cute_name}: {self.profile_id}")  # Send results

        def hyp_skyblock_info(self, group_id: str, uid: str, username: str, profile_id: str):
            """Get username's skyblock info and sends it to group_id while mentioning uid.

            Args:
                group_id (str): The group's ID you want to send the result to.
                uid (str): The user's ID you want to mention.
                username (str): The player's username, which will be feed into get_uuid to get the player's UUID.
                profile_id (str): The player's profile ID.
            """
            modules.send(group_id, uid, "Received, processing...")
            profile_id = profile_id.strip("\"")
            # Get the player's skyblock info
            self.hyp_skyblock_info_res = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}")  # Get data
            self.hyp_skyblock_info_result = self.hyp_skyblock_info_res.json()  # Get JSON data

            # Data
            # Armor
            self.hyp_skyblock_info_armor_boots = self.hyp_skyblock_info_result['profiles'][profile_id]['items']['armor'][0]['display_name']
            self.hyp_skyblock_info_armor_leggings = self.hyp_skyblock_info_result['profiles'][profile_id]['items']['armor'][1]['display_name']
            self.hyp_skyblock_info_armor_chestplate = self.hyp_skyblock_info_result['profiles'][profile_id]['items']['armor'][2]['display_name']
            self.hyp_skyblock_info_armor_head = self.hyp_skyblock_info_result['profiles'][profile_id]['items']['armor'][3]['display_name']
            try:
                self.hyp_skyblock_info_armor_set = self.hyp_skyblock_info_result['profiles'][profile_id]['items']['armor_set']
            except KeyError:
                self.hyp_skyblock_info_armor_set = "NONE"

            # Fairy souls
            self.hyp_skyblock_info_fairy_souls_collected = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['fairy_souls']['collected']
            self.hyp_skyblock_info_fairy_souls_total = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['fairy_souls']['total']

            # Levels
            self.hyp_skyblock_info_taming_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['taming']['level']
            self.hyp_skyblock_info_farming_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['farming']['level']
            self.hyp_skyblock_info_mining_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['mining']['level']
            self.hyp_skyblock_info_combat_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['combat']['level']
            self.hyp_skyblock_info_foraging_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['foraging']['level']
            self.hyp_skyblock_info_fishing_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['fishing']['level']
            self.hyp_skyblock_info_enchanting_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['enchanting']['level']
            self.hyp_skyblock_info_alchemy_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['alchemy']['level']
            self.hyp_skyblock_info_carpentry_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['carpentry']['level']
            self.hyp_skyblock_info_runecrafting_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['runecrafting']['level']
            self.hyp_skyblock_info_social_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['social']['level']
            self.hyp_skyblock_info_average_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['average_level']
            self.hyp_skyblock_info_average_level = int(self.hyp_skyblock_info_average_level)  # Originaly it is a float

            # Slayer
            self.hyp_skyblock_spider_slayer_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['slayers']['spider']['level']['currentLevel']
            self.hyp_skyblock_spider_slayer_level_progress = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['slayers']['spider']['level']['progress']
            self.hyp_skyblock_spider_slayer_level_left = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['slayers']['spider']['level']['xpForNext']
            # TODO: Pets
            # TODO: Purse
            # TODO: Current area

            # TODO: Fairy souls & Levels
            # Send the result
            modules.send(group_id, uid, f"""Skyblock data:

Profile ID: {profile_id}

Armor:
Helmet: {self.hyp_skyblock_info_armor_head}
Chestplate: {self.hyp_skyblock_info_armor_chestplate}
Leggings: {self.hyp_skyblock_info_armor_leggings}
Boots: {self.hyp_skyblock_info_armor_boots}
Armor set: {self.hyp_skyblock_info_armor_set}

Slayer:
""")

    class Timed:
        """Timed keywords: Keywords that only works during a specific time.
        """
        def __init__(self):
            self.timed_localtime = time.ctime()  # Get current time

        def tech_no(self, group_id: str):
            """If it is Jul 1, respond to 'techno' or 'technoblade'. Sends the respond to group_id.

            Args:
                group_id (str): The group's ID you want to send the result to.
            """
            if self.timed_localtime[4:10] == 'Jul  1':
                modules.send_public_message(group_id, 'Technoblade Never Dies!!!')  # TECHNOBLADE NEVER DIES!!!
    class Economy:
        """Economy modules, inspired by UnbelievaBoat the discord bot.
        """
        def get_current(self, group_id: str, uid: str):
            """Get uid's coins.

            Args:
                group_id (str): The group's ID you want to send the result to.
                uid (str): The user's ID you want to get the coins.
            """
            uid = str(uid)  # Convert UID from int to str

            with open('/Users/wangyinuo/Documents/Superior-Bot/storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.get_current_economy_stats = json.load(f)  # Get the coins this user have
                f.close()

            try:
                self.get_current_coins = self.get_current_economy_stats[uid]['coins']  # Get your coins
            except KeyError:  # No profile yet?
                self.get_current_economy_stats[uid]['coins'] = 0  # Create new profile
                with open('/Users/wangyinuo/Documents/Superior-Bot/storage/economy.json', 'w') as f:
                    json.dump(self.get_current_economy_stats, f)
                    f.close()
                modules.send(group_id, uid, 'Your current economy status:\nCoins: 0')

            modules.send(group_id, uid, f"Your current economy status:\nCoins: {self.get_current_coins}")  # Send the results

        def work(self, group_id: str, uid: str):
            """Work to earn coins.

            Args:
                group_id (str): The group's ID you want to send the result to.
                uid (str): The user's ID who worked.
            """
            uid = str(uid)  # Convert UID from int to str

            self.work_income = random.randint(-500, 1000)  # Random income

            with open('/Users/wangyinuo/Documents/Superior-Bot/storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.work_economy_stats = json.load(f)
                f.close()

            try:
                coins = self.work_economy_stats[uid]['coins']  # Get your coins
                coins = int(coins)  # Convert coins to int so that we can add the income
                coins += self.work_income  # Change current status
                coins = str(coins)  # Convert coins to str so that we can dump them
                self.work_economy_stats[uid]['coins'] = coins  # Save it to the dict
            except KeyError:
                self.work_economy_stats[uid]['coins'] = 0 + self.work_income

            with open('/Users/wangyinuo/Documents/Superior-Bot/storage/economy.json', 'w') as f:  # Dump the current status
                json.dump(self.work_economy_stats, f)
                f.close()

            if self.work_income > 0:  # You got some money!
                modules.send(group_id, uid, f"You got ${self.work_income}.")
            elif self.work_income < 0:  # Too bad!
                modules.send(group_id, uid, f"You lost ${self.work_income}.")
            elif self.work_income == 0:
                modules.send(group_id, uid, 'Nothing happened...')

    def help_(self, group_id: str):
        """Sends a help message to Group ID without mentioning anyone.

        Args:
            group_id (str): The group's ID you want to send the result to.
        """
        self.send_public_message(group_id, """--- Keywords ---

help {Get the help message}
query [Server address] {Used to check the basic information about a Minecraft server. No response means that the server is offline}
hyp [In game name] {Get your Hypixel basic info}
bw [In game name] {Get your Hypixel bedwars info}
sblist [In game name] {Get your list of profile in Hypixel Skyblock}
sb [In game name] \"[Profile ID]\" {Get your Hypixel Skyblock basic info}

--- Economy ---
^balance/^bal {How much cash do you have}
^work {Work for cash.. or lose them}

--- Timed keywords ---
Technoblade/Techno: Available: Jul 1""")


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
            personal_modules.send(user_id, "Received, processing...")
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
                personal_modules.send(user_id, f"""Status: {self.mc_query_online}

MOTD: {self.mc_query_motd}
Online players: {self.mc_query_online_players}
Max players: {self.mc_query_max_players}""")  # Send results
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
            """Get the basic Hypixel information of a player using their UUID, and then sends the results to group_id while mentioning uid.

            Args:
                uid (str): The user's ID you want to mention.
                username (str): The player's username, which will be the input get get_uuid, which will get the player's UUID to be queried.
            """
            personal_modules.send(uid, "Received, processing...")
            self.get_uuid(username)  # First, get UUID
            self.hyp_basic_info_res = requests.get(f'https://api.hypixel.net/player?key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}')  # Get basic info from Hypixel API
            self.hyp_basic_info_result = self.hyp_basic_info_res.json()  # Get JSON data from the response
            self.hyp_basic_info_guild_res = requests.get(f"https://api.hypixel.net/guild?key={self.hypixel_api_key}&player={self.get_uuid_uuid}")  # Get guild info
            self.hyp_basic_info_guild_result = self.hyp_basic_info_guild_res.json()  # Guild data in JSON

            # Data
            try:
                self.hyp_basic_info_displayname = self.hyp_basic_info_result['player']['displayname']
                self.hyp_basic_info_karma = self.hyp_basic_info_result['player']['karma']
                self.hyp_basic_info_rank = self.hyp_basic_info_result['player']['newPackageRank']
                self.hyp_basic_info_guild = self.hyp_basic_info_guild_result['guild']['name']
                self.hyp_basic_info_most_recent_game = self.hyp_basic_info_result['player']['mostRecentGameType']
                self.hyp_basic_info_pet = self.hyp_basic_info_result['player']['currentPet']
                self.hyp_basic_info_gadget = self.hyp_basic_info_result['player']['currentGadget']
                self.hyp_basic_info_language = self.hyp_basic_info_result['player']['userLanguage']
            except KeyError:
                self.hyp_basic_info_most_recent_game = 'SKYBLOCK'
                self.hyp_basic_info_pet = 'NONE'
                self.hyp_basic_info_gadget = 'NONE'
                self.hyp_basic_info_language = 'NONE'

            personal_modules.send(uid, f"""Hypixel basic information:

Display name: {self.hyp_basic_info_displayname}
Karma: {self.hyp_basic_info_karma}
Rank: {self.hyp_basic_info_rank}
Guild: {self.hyp_basic_info_guild}
Most recent game: {self.hyp_basic_info_most_recent_game}
Current pet: {self.hyp_basic_info_pet}
Current gadget: {self.hyp_basic_info_gadget}
Language: {self.hyp_basic_info_language}""")


        def hyp_bedwars_info(self, user_id: str, username: str):
            """Get username's basic Hypixel bedwars status and then sends it to user_id.

            Args:
                user_id (str): The user's ID you want to send the results to.
                username (str): The player's name.
            """
            personal_modules.send(user_id, "Received, processing...")
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

            personal_modules.send(user_id, f"""Bedwars data:

Bedwars experience: {self.hyp_bedwars_info_exp}
Bedwars coins: {self.hyp_bedwars_info_coins}
Bedwars played: {self.hyp_bedwars_info_games_played}
Items purchased: {self.hyp_bedwars_info_item_purchased}

Kills: {self.hyp_bedwars_info_kills}
Final kills: {self.hyp_bedwars_info_final_kills}
Deaths: {self.hyp_bedwars_info_deaths}
Final deaths: {self.hyp_bedwars_info_final_deaths}

Beds broken: {self.hyp_bedwars_info_beds_broken}
Beds lost: {self.hyp_bedwars_info_beds_lost}
Games won: {self.hyp_bedwars_info_games_won}
Winstreak: {self.hyp_bedwars_info_winstreak}
Games lost: {self.hyp_bedwars_info_games_lost}""")  # Send results

        def hyp_skyblock_list(self, uid: str, username: str):
            """List the profile IDs.

            Args:
                uid (str): The user's ID you want to mention.
                username (str): The player's username, which will be feed into get_uuid().
            """
            personal_modules.send(uid, "Received, processing...")
            self.get_uuid(username)
            self.hyp_skyblock_list_res = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}")
            self.hyp_skyblock_list_result = self.hyp_skyblock_list_res.json()

            for i in range(0, 2):
                self.profile_id = self.hyp_skyblock_list_result['profiles'][i]['profile_id']
                self.profile_cute_name = self.hyp_skyblock_list_result['profiles'][i]['cute_name']
                personal_modules.send(uid, f"{self.profile_cute_name}: {self.profile_id}")

        def hyp_skyblock_info(self, uid: str, username: str, profile_id: str):
            """Get username's skyblock info and sends it to Group ID while mentioning uid.

            Args:
                uid (str): The user's ID you want to mention.
                username (str): The player's username, which will be feed into get_uuid to get the player's UUID.
                profile_id (str): The player's profile ID.
            """
            personal_modules.send(uid, "Received, processing...")
            profile_id = profile_id.strip("\"")
            # Get the player's skyblock info
            self.hyp_skyblock_info_res = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}")
            self.hyp_skyblock_info_result = self.hyp_skyblock_info_res.json()

            # Data
            # Armor
            self.hyp_skyblock_info_armor_boots = self.hyp_skyblock_info_result['profiles'][profile_id]['items']['armor'][0]['display_name']
            self.hyp_skyblock_info_armor_leggings = self.hyp_skyblock_info_result['profiles'][profile_id]['items']['armor'][1]['display_name']
            self.hyp_skyblock_info_armor_chestplate = self.hyp_skyblock_info_result['profiles'][profile_id]['items']['armor'][2]['display_name']
            self.hyp_skyblock_info_armor_head = self.hyp_skyblock_info_result['profiles'][profile_id]['items']['armor'][3]['display_name']
            try:
                self.hyp_skyblock_info_armor_set = self.hyp_skyblock_info_result['profiles'][profile_id]['items']['armor_set']
            except KeyError:
                self.hyp_skyblock_info_armor_set = "NONE"

            # Fairy souls
            self.hyp_skyblock_info_fairy_souls_collected = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['fairy_souls']['collected']
            self.hyp_skyblock_info_fairy_souls_total = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['fairy_souls']['total']

            # Levels
            self.hyp_skyblock_info_taming_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['taming']['level']
            self.hyp_skyblock_info_farming_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['farming']['level']
            self.hyp_skyblock_info_mining_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['mining']['level']
            self.hyp_skyblock_info_combat_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['combat']['level']
            self.hyp_skyblock_info_foraging_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['foraging']['level']
            self.hyp_skyblock_info_fishing_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['fishing']['level']
            self.hyp_skyblock_info_enchanting_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['enchanting']['level']
            self.hyp_skyblock_info_alchemy_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['alchemy']['level']
            self.hyp_skyblock_info_carpentry_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['carpentry']['level']
            self.hyp_skyblock_info_runecrafting_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['runecrafting']['level']
            self.hyp_skyblock_info_social_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['levels']['social']['level']
            self.hyp_skyblock_info_average_level = self.hyp_skyblock_info_result['profiles'][profile_id]['data']['average_level']
            self.hyp_skyblock_info_average_level = int(self.hyp_skyblock_info_average_level)  # Originaly a float

            # TODO: Slayer
            # TODO: Pets
            # TODO: Purse
            # TODO: Current area

            # TODO: Levels
            # Send the result
            personal_modules.send(uid, f"""Skyblock data:

Profile ID: {profile_id}

Armor:
Helmet: {self.hyp_skyblock_info_armor_head}
Chestplate: {self.hyp_skyblock_info_armor_chestplate}
Leggings: {self.hyp_skyblock_info_armor_leggings}
Boots: {self.hyp_skyblock_info_armor_boots}
Armor set: {self.hyp_skyblock_info_armor_set}""")

    def sexypic(self, user_id: str):
        """Get 5 random sexy pic from Pixiv and then sends it to user_id

        Args:
            user_id (str): The user's ID you want to send the results to.
        """
        personal_modules.send(user_id, "Received, processing...")
        self.random_sexy_res = requests.get(self.random_sexy_api)  # Get raw data from API
        self.random_sexy_result = self.random_sexy_res.json()  # Convert raw data into JSON data

        # Get data
        for i in range(0, 4):
            self.random_sexy_painter = self.random_sexy_result['data'][i]['author']
            self.random_sexy_pid = self.random_sexy_result['data'][i]['pid']
            self.random_sexy_title = self.random_sexy_result['data'][i]['title']
            self.random_sexy_img_url = self.random_sexy_result['data'][i]['urls']['original']
            self.random_sexy_file_type = self.random_sexy_result['data'][i]['ext']

            # Send to the user
            self.send(user_id, f'[CQ:image,file={self.random_sexy_img_url}]\nAuthor: {self.random_sexy_painter}\nPID: {self.random_sexy_pid}\nTitle: {self.random_sexy_title}\nImage URL: {self.random_sexy_img_url}\nFile type: {self.random_sexy_file_type}')  # Send image

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

            with open('/Users/wangyinuo/Documents/Superior-Bot/storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.get_current_economy_stats = json.load(f)  # Get the coins this user have
                f.close()

            try:
                self.get_current_coins = self.get_current_economy_stats[uid]['coins']  # Get your coins
            except KeyError:  # No profile yet?
                self.get_current_economy_stats[uid]['coins'] = 0  # Create new profile
                with open('/Users/wangyinuo/Documents/Superior-Bot/storage/economy.json', 'w') as f:
                    f.write(self.get_current_economy_stats)
                    f.close()
                personal_modules.send(uid, 'Your current economy status:\nCoins: 0')

            personal_modules.send(uid, f"Your current economy status:\nCoins: {self.get_current_coins}")  # Send the results

        def work(self, uid: str):
            """Work to earn coins, and then sends the results to uid.

            Args:
                uid (str): The user's ID you want to sends the results to.
            """
            uid = str(uid)  # Convert UID from int to str

            self.work_income = random.randint(-500, 1000)  # Random income

            with open('/Users/wangyinuo/Documents/Superior-Bot/storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.work_economy_stats = json.load(f)
                f.close()

            try:
                coins = self.work_economy_stats[uid]['coins']  # Get your coins
                coins = int(coins)  # Convert coins to int so that we can add the income
                coins += self.work_income  # Change current status
                coins = str(coins)  # Convert coins to str so that we can dump them
                self.work_economy_stats[uid]['coins'] = coins  # Save it to the dict
            except KeyError:
                self.work_economy_stats[uid]['coins'] = 0 + self.work_income

            with open('/Users/wangyinuo/Documents/Superior-Bot/storage/economy.json', 'w') as f:  # Dump the current status
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
        self.send(uid, """--- Keywords ---

help {Get the help message}
query [Server address] {Used to check the basic information about a Minecraft server. No response means that the server is offline}
hyp [In game name] {Get your Hypixel basic info}
bw [In game name] {Get your Hypixel bedwars info}
sblist [In game name] {Get your list of profile in Hypixel Skyblock}
sb [In game name] \"[Profile ID]\" {Get your Hypixel Skyblock basic info}
sexypic {Get 5 sexy pics from Pixiv. USE BY CAUTION}

--- Economy ---
^balance/^bal {How much cash do you have}
^work {Work for cash.. or lose them}

--- Timed keywords ---
Technoblade/Techno: Available: Jul 1""")


# Initialize modules
modules = Modules()
minecraft = Modules.Minecraft()
timed = Modules.Timed()
economy = Modules.Economy()

personal_modules = PersonalModules()
personal_minecraft = PersonalModules.Minecraft()
personal_timed = PersonalModules.Timed()
personal_economy = PersonalModules.Economy()