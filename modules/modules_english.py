"""The modules for Superior Bot (English).
"""
# Import needed packages
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

    def send_to(self, user_id: str, msg: str):
        """Sends a private msg to user_id.

        Args:
            user_id (str): The user's ID you want to send msg to.
            msg (str): The message you want to send.
        """
        requests.get(f"http://127.0.0.1:5700/send_private_msg?user_id={str(user_id)}&message={msg}")  # Do the request to send the message

    def calc(self, group_id: str, user_id: str, equation: str):
        """Calculates equation using eval(), and then sends the result to group_id while mentioning user_id.

        Args:
            group_id (str): The group's ID you want to send the result to.
            user_id (str): The user's ID you want to mention.
            equation (str): The equation to calculate.
        """
        try:
            self.calc_result = eval(equation)  # Get the result
        except Exception as e:  # Example: a/0
            self.send(group_id, user_id, e)
        # Nothing wrong, send the results and return them
        self.send(group_id, user_id, self.calc_result)

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
            try:
                self.mc_query_res = requests.get(f"http://127.0.0.1/json.php?host={host}&port=25565")  # Request to a PHP file with Apache to get the server's status
            except Exception:  # The query server is offline
                Modules.send(group_id, user_id, "Query server is offline! Please notify admin!")
            self.mc_query_result = self.mc_query_res.json()  # Get JSON data

            # Get server details
            # ADJUST THESE BELOW IF YOU ENCOUNTERED KeyError!!!
            if self.mc_query_result['status'] == 'Online':
                self.mc_query_online = self.mc_query_result['status']
                self.mc_query_motd = self.mc_query_result['motd']['clean']
                self.mc_query_online_players = self.mc_query_result['players']['online']
                self.mc_query_max_players = self.mc_query_result['players']['max']
                Modules.send(group_id, user_id, f"Status: {self.mc_query_online}\nMOTD: {self.mc_query_motd}\nOnline players: {self.mc_query_online_players}\nMax players: {self.mc_query_max_players}")  # Send results
            else:
                Modules.send(group_id, user_id, 'The server is offline!')  # The server is offline

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
            self.get_uuid(username)  # First, get UUID
            self.hyp_basic_info_res = requests.get(f'https://api.hypixel.net/player?key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}')  # Get basic info from Hypixel API
            self.hyp_basic_info_result = self.hyp_basic_info_res.json()  # Get JSON data from the response

            # Data
            try:
                self.hyp_basic_info_displayname = self.hyp_basic_info_result['player']['displayname']
                self.hyp_basic_info_rank = self.hyp_basic_info_result['player']['newPackageRank']
                self.hyp_basic_info_most_recent_game = self.hyp_basic_info_result['player']['mostRecentGameType']
            except KeyError:
                self.hyp_basic_info_most_recent_game = 'SKYBLOCK'

            Modules.send(group_id, uid, f'Hypixel basic information:\nDisplay name: {self.hyp_basic_info_displayname}\nRank: {self.hyp_basic_info_rank}\nMost recent game: {self.hyp_basic_info_most_recent_game}')

        def hyp_bedwars_info(self, group_id: str, user_id: str, username: str):
            """Get's a player's Hypixel bedwars status using their UUID, and then sends the result to group_id while mentioning user_id.

            Args:
                group_id (str): The group's ID you want to send the result to.
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
                Modules.send(group_id, user_id, 'Something is wrong with your Hypixel bedwars profile. Please notice admin!')

            Modules.send(group_id, user_id, f'Bedwars data:\nBedwars experience: {self.hyp_bedwars_info_exp}\nBedwars coins: {self.hyp_bedwars_info_coins}\nBedwars played: {self.hyp_bedwars_info_games_played}\nItems purchased: {self.hyp_bedwars_info_item_purchased}\nKills: {self.hyp_bedwars_info_kills}\nFinal kills: {self.hyp_bedwars_info_final_kills}\nDeaths: {self.hyp_bedwars_info_deaths}\nFinal deaths: {self.hyp_bedwars_info_final_deaths}\nBeds broken: {self.hyp_bedwars_info_beds_broken}\nBeds lost: {self.hyp_bedwars_info_beds_lost}\nGames won: {self.hyp_bedwars_info_games_won}\nWinstreak: {self.hyp_bedwars_info_winstreak}\nGames lost: {self.hyp_bedwars_info_games_lost}')  # Send results

        def hyp_skyblock_info(self, group_id: str, uid: str, username: str):
            """Get username's skyblock info and sends it to group_id while mentioning uid.

            Args:
                group_id (str): The group's ID you want to send the result to.
                uid (str): The user's ID you want to mention.
                username (str): The player's username, which will be feed into get_uuid to get the player's UUID.
            """
            self.get_uuid(username)  # Get the player's UUID
            # Get the player's profile ID
            self.hyp_skyblock_info_profile_res = requests.get(f'https://api.hypixel.net/skyblock/profiles?key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}')
            self.hyp_skyblock_info_profile_result = self.hyp_skyblock_info_profile_res.json()
            # Get the player's skyblock info
            self.hyp_skyblock_info_res = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}")
            self.hyp_skyblock_info_result = self.hyp_skyblock_info_res.json()

            for i in range(0, 4):
                try:
                    self.hyp_skyblock_info_profile = self.hyp_skyblock_info_profile_result['profiles'][i]['profile_id']
                except KeyError:  # No profile?
                    Modules.send(group_id, uid, "You don't have an Skyblock profile yet!")

                # Data
                self.hyp_skyblock_info_cute_name = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['cute_name']

                self.hyp_skyblock_info_armor_boots = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['items']['armor'][0]['display_name']
                self.hyp_skyblock_info_armor_leggings = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['items']['armor'][1]['display_name']
                self.hyp_skyblock_info_armor_chestplate = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['items']['armor'][2]['display_name']
                self.hyp_skyblock_info_armor_head = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['items']['armor'][3]['display_name']
                self.hyp_skyblock_info_armor_set = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['items']['armor_set']

                self.hyp_skyblock_info_fairy_souls_collected = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['fairy_souls']['collected']
                self.hyp_skyblock_info_fairy_souls_total = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['fairy_souls']['total']
            
                self.hyp_skyblock_info_taming_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['taming']['level']
                self.hyp_skyblock_info_farming_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['farming']['level']
                self.hyp_skyblock_info_mining_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['mining']['level']
                self.hyp_skyblock_info_combat_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['combat']['level']
                self.hyp_skyblock_info_foraging_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['foraging']['level']
                self.hyp_skyblock_info_fishing_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['fishing']['level']
                self.hyp_skyblock_info_enchanting_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['enchanting']['level']
                self.hyp_skyblock_info_alchemy_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['alchemy']['level']
                self.hyp_skyblock_info_carpentry_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['carpentry']['level']
                self.hyp_skyblock_info_runecrafting_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['runecrafting']['level']
                self.hyp_skyblock_info_social_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['social']['level']
                self.hyp_skyblock_info_average_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['average_level']
                self.hyp_skyblock_info_average_level = int(self.hyp_skyblock_info_average_level)  # Originaly it is a float
            
                # TODO: Slayer
                # TODO: Pets
                # TODO: Purse
                # TODO: Current area
            
                # TODO: Fairy souls & Levels
                # Send the result
                Modules.send(group_id, uid, f"Skyblock data:\n\nProfile ID: {self.hyp_skyblock_info_profile}\nProfile cute name: {self.hyp_skyblock_info_cute_name}\n\nArmor:\nHelmet: {self.hyp_skyblock_info_armor_head}\nChestplate: {self.hyp_skyblock_info_armor_chestplate}\nLeggings: {self.hyp_skyblock_info_armor_leggings}\nBoots: {self.hyp_skyblock_info_armor_boots}\nArmor set: {self.hyp_skyblock_info_armor_set}")

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

    def wotd(self, group_id: str):
        """Sends Bing's wallpaper to group_id without mentioning people.

        Args:
            group_id (str): The group's ID you want to send the result to.
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

    def get_news(self, group_id: str):
        """Get healine news from API and then sends it to chat without mentioning anyone.

        Args:
            group_id (str): The group's ID you want to send the result to.
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

        def tech_no(self, group_id: str):
            """If it is Jul 1, respond to 'techno' or 'technoblade'. Sends the respond to group_id.

            Args:
                group_id (str): The group's ID you want to send the result to.
            """
            if self.timed_localtime[4:10] == 'Jul  1':
                Modules.send_public_message(group_id, 'Technoblade Never Dies!!!')  # TECHNOBLADE NEVER DIES!!!
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

            with open('../storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.get_current_economy_stats = json.load(f)  # Get the coins this user have
                f.close()

            try:
                self.get_current_coins = self.get_current_economy_stats[uid]['coins']  # Get your coins
            except KeyError:  # No profile yet?
                self.get_current_economy_stats[uid]['coins'] = 0  # Create new profile
                with open('../storage/economy.json', 'w') as f:
                    json.dump(self.get_current_economy_stats, f)
                    f.close()
                Modules.send(group_id, uid, 'Your current economy status:\nCoins: 0')

            Modules.send(group_id, uid, f"Your current economy status:\nCoins: {self.get_current_coins}")  # Send the results

        def work(self, group_id: str, uid: str):
            """Work to earn coins.

            Args:
                group_id (str): The group's ID you want to send the result to.
                uid (str): The user's ID who worked.
            """
            uid = str(uid)  # Convert UID from int to str

            self.work_income = random.randint(-500, 1000)  # Random income

            with open('../storage/economy.json', 'r') as f:  # Open storage file and load the data
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

            with open('../storage/economy.json', 'w') as f:  # Dump the current status
                json.dump(self.work_economy_stats, f)
                f.close()

            if self.work_income > 0:  # You got some money!
                Modules.send(group_id, uid, f"You got ${self.work_income}.")
            elif self.work_income < 0:  # Too bad!
                Modules.send(group_id, uid, f"You lost ${self.work_income}.")
            elif self.work_income == 0:
                Modules.send(group_id, uid, 'Nothing happened...')

    def help_(self, group_id: str):
        """Sends a help message to Group ID without mentioning anyone.

        Args:
            group_id (str): The group's ID you want to send the result to.
        """
        self.send_public_message(group_id, "--- Keywords ---\n\nsb {Just a command to check whether the bot is online or not}\n\nquery [Server address] {Used to check the basic information about a Minecraft server. No response means that the server is offline}\n\nhyp [In game name] {Get your Hypixel basic info}\n\nbw [In game name] {Get your Hypixel bedwars info}\n\ncalc [Equation] {Calculate something}\n\nwotd {Get wallpaper of the day from Bing}\n\nsexypic {Get a pic from Pixiv. The result will be send to you via private chat. You need to add the bot as your friend before using. USE BY CAUTION}\n\nnews {Get the headline news}\n\n\n\n--- Economy ---\n\n^balance/^bal {How much cash do you have}\n\n^work {Work for cash.. or lose them}\n\n\n\n--- Timed keywords ---\n\nTechnoblade/Techno:\nAvailable: Jul 1")


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
                PersonalModules.send(user_id, "Query server is offline! Please notify admin!")
            self.mc_query_result = self.mc_query_res.json()  # Get JSON data

            # Get server details
            if self.mc_query_result['status'] == 'Online':
                self.mc_query_online = self.mc_query_result['status']
                self.mc_query_motd = self.mc_query_result['motd']['clean']
                self.mc_query_online_players = self.mc_query_result['players']['online']
                self.mc_query_max_players = self.mc_query_result['players']['max']
                PersonalModules.send(user_id, f"Status: {self.mc_query_online}\nMOTD: {self.mc_query_motd}\nOnline players: {self.mc_query_online_players}\nMax players: {self.mc_query_max_players}")  # Send results
            else:
                PersonalModules.send(user_id, 'The server is offline!')  # Server offline

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
                self.hyp_basic_info_most_recent_game = 'SKYBLOCK'

            PersonalModules.send(uid, f'Hypixel basic information:\nDisplay name: {self.hyp_basic_info_displayname}\nRank: {self.hyp_basic_info_rank}\nMost recent game: {self.hyp_basic_info_most_recent_game}')

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
                PersonalModules.send(user_id, 'Something is wrong with your Hypixel bedwars profile. Please notice admin!')

            PersonalModules.send(user_id, f'Bedwars data:\nBedwars experience: {self.hyp_bedwars_info_exp}\nBedwars coins: {self.hyp_bedwars_info_coins}\nBedwars played: {self.hyp_bedwars_info_games_played}\nItems purchased: {self.hyp_bedwars_info_item_purchased}\nKills: {self.hyp_bedwars_info_kills}\nFinal kills: {self.hyp_bedwars_info_final_kills}\nDeaths: {self.hyp_bedwars_info_deaths}\nFinal deaths: {self.hyp_bedwars_info_final_deaths}\nBeds broken: {self.hyp_bedwars_info_beds_broken}\nBeds lost: {self.hyp_bedwars_info_beds_lost}\nGames won: {self.hyp_bedwars_info_games_won}\nWinstreak: {self.hyp_bedwars_info_winstreak}\nGames lost: {self.hyp_bedwars_info_games_lost}')  # Send results

        def hyp_skyblock_info(self, uid: str, username: str):
            """Get username's skyblock info and sends it to Group ID while mentioning uid.

            Args:
                uid (str): The user's ID you want to mention.
                username (str): The player's username, which will be feed into get_uuid to get the player's UUID.
            """
            self.get_uuid(username)  # Get the player's UUID
            # Get the player's profile ID
            self.hyp_skyblock_info_profile_res = requests.get(f'https://api.hypixel.net/skyblock/profiles?key={self.hypixel_api_key}&uuid={self.get_uuid_uuid}')
            self.hyp_skyblock_info_profile_result = self.hyp_skyblock_info_profile_res.json()
            # Get the player's skyblock info
            self.hyp_skyblock_info_res = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}")
            self.hyp_skyblock_info_result = self.hyp_skyblock_info_res.json()

            try:
                self.hyp_skyblock_info_profile = self.hyp_skyblock_info_profile_result['profiles'][0]['profile_id']
            except KeyError:  # No profile?
                PersonalModules.send(uid, "You don't have an Skyblock profile yet!")

            # Data
            self.hyp_skyblock_info_cute_name = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['cute_name']
    
            self.hyp_skyblock_info_armor_boots = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['items']['armor'][0]['display_name']
            self.hyp_skyblock_info_armor_leggings = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['items']['armor'][1]['display_name']
            self.hyp_skyblock_info_armor_chestplate = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['items']['armor'][2]['display_name']
            self.hyp_skyblock_info_armor_head = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['items']['armor'][3]['display_name']
            self.hyp_skyblock_info_armor_set = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['items']['armor_set']

            self.hyp_skyblock_info_fairy_souls_collected = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['fairy_souls']['collected']
            self.hyp_skyblock_info_fairy_souls_total = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['fairy_souls']['total']
            
            self.hyp_skyblock_info_taming_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['taming']['level']
            self.hyp_skyblock_info_farming_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['farming']['level']
            self.hyp_skyblock_info_mining_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['mining']['level']
            self.hyp_skyblock_info_combat_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['combat']['level']
            self.hyp_skyblock_info_foraging_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['foraging']['level']
            self.hyp_skyblock_info_fishing_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['fishing']['level']
            self.hyp_skyblock_info_enchanting_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['enchanting']['level']
            self.hyp_skyblock_info_alchemy_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['alchemy']['level']
            self.hyp_skyblock_info_carpentry_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['carpentry']['level']
            self.hyp_skyblock_info_runecrafting_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['runecrafting']['level']
            self.hyp_skyblock_info_social_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['levels']['social']['level']
            self.hyp_skyblock_info_average_level = self.hyp_skyblock_info_result['profiles'][self.hyp_skyblock_info_profile]['data']['average_level']
            self.hyp_skyblock_info_average_level = int(self.hyp_skyblock_info_average_level)
            
            # TODO: Slayer
            # TODO: Pets
            # TODO: Purse
            # TODO: Current area
            
            # TODO: Levels
            # Send the result
            PersonalModules.send(uid, f"Skyblock data:\n\nProfile ID: {self.hyp_skyblock_info_profile}\nProfile cute name: {self.hyp_skyblock_info_cute_name}\n\nArmour:\nHelmet: {self.hyp_skyblock_info_armor_head}\nChestplate: {self.hyp_skyblock_info_armor_chestplate}\nLeggings: {self.hyp_skyblock_info_armor_leggings}\nBoots: {self.hyp_skyblock_info_armor_boots}\nArmor set: {self.hyp_skyblock_info_armor_set}")


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
                PersonalModules.send(uid, 'Technoblade Never Dies!!!')  # TECHNOBLADE NEVER DIES!!!
    class Economy:
        """Superior Bot's Economy system for private chat. Inspired by UnbelievaBoat the discord bot.
        """
        def get_current(self, uid: str):
            """Get uid's current coins.

            Args:
                uid (str): The user's ID you want to get the coins from.
            """
            uid = str(uid)  # Convert UID from int to str

            with open('../storage/economy.json', 'r') as f:  # Open storage file and load the data
                self.get_current_economy_stats = json.load(f)  # Get the coins this user have
                f.close()

            try:
                self.get_current_coins = self.get_current_economy_stats[uid]['coins']  # Get your coins
            except KeyError:  # No profile yet?
                self.get_current_economy_stats[uid]['coins'] = 0  # Create new profile
                with open('../storage/economy.json', 'w') as f:
                    f.write(self.get_current_economy_stats)
                    f.close()
                PersonalModules.send(uid, 'Your current economy status:\nCoins: 0')

            PersonalModules.send(uid, f"Your current economy status:\nCoins: {self.get_current_coins}")  # Send the results

        def work(self, uid: str):
            """Work to earn coins, and then sends the results to uid.

            Args:
                uid (str): The user's ID you want to sends the results to.
            """
            uid = str(uid)  # Convert UID from int to str

            self.work_income = random.randint(-500, 1000)  # Random income

            with open('../storage/economy.json', 'r') as f:  # Open storage file and load the data
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

            with open('../storage/economy.json', 'w') as f:  # Dump the current status
                json.dump(self.work_economy_stats, f)
                f.close()

            if self.work_income > 0:  # You got some money!
                PersonalModules.send(uid, f"You got ${self.work_income}.")
            elif self.work_income < 0:  # Too bad!
                PersonalModules.send(uid, f"You lost ${self.work_income}.")
            elif self.work_income == 0:
                PersonalModules.send(uid, 'Nothing happened...')

    def help_(self, uid: str):
        """Sends a help message to uid.

        Args:
            uid (str): The user's ID you want to send the help message.
        """
        self.send(uid, "--- Keywords ---\n\nsb {Just a command to check whether the bot is online or not}\n\nquery [Server address] {Used to check the basic information about a Minecraft server. No response means that the server is offline}\n\nhyp [In game name] {Get your Hypixel basic info}\n\nbw [In game name] {Get your Hypixel bedwars info}\n\ncalc [Equation] {Calculate something}\n\nwotd {Get wallpaper of the day from Bing}\n\nsexypic {Get a pic from Pixiv. The result will be send to you via private chat. You need to add the bot as your friend before using. USE BY CAUTION}\n\nnews {Get the headline news}\n\n\n\n--- Economy ---\n\n^balance/^bal {How much cash do you have}\n\n^work {Work for cash.. or lose them}\n\n\n\n--- Timed keywords ---\n\nTechnoblade/Techno:\nAvailable: Jul 1")