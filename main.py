"""The main file for Superior Bot.
"""
# Import needed packages
from flask import Flask, request  # For building a simple server to receiving messages
import argparse  # Used to get arguments

# Import module files
from modules.modules_english import *  # English module

app = Flask(__name__)  # Create the Flask APP
parser = argparse.ArgumentParser(description="Superior Bot manual")  # Create the parser

parser.add_argument('Group_ID', type=int, help='Your QQ group ID')  # Group ID
parser.add_argument('Host', type=str, default='127.0.0.1', help='Your IP')  # IP for flask server
parser.add_argument('Port', type=str, default='9000', help='Your port')  # Port for flask server
args = parser.parse_args()  # Parse the args

group_id = args.Group_ID  # Get the group ID
host = args.Host  # IP
port = args.Port  # Port
bot = True  # If the bot if on or not


def main(msg: str, uid: str):
    """Get the keyword from msg and the sender's ID from the receive server, then do a correct response to it..

    Args:
        msg (str): The message someone sent.
        uid (str): The sender's ID.
    """
    msg = msg.lower()
    uid = str(uid)

    # Minecraft
    if msg[0:5] == 'query':  # Minecraft server detect
        minecraft.mc_query(group_id, uid, msg[6:])
    elif msg[0:3] == 'hyp':  # Hypixel basic info
        minecraft.hyp_basic_info(group_id, uid, msg[4:])
    elif msg[0:2] == 'bw':  # Hypixel bedwars info
        minecraft.hyp_bedwars_info(group_id, uid, msg[3:])
    elif msg[0:2] == 'sb':  # Hypixel skyblock info
        minecraft.hyp_skyblock_info(group_id, uid, msg[3:])

    elif msg == 'wotd':  # Wallpaper
        modules.wotd(group_id)

    elif msg[0:4] == 'calc':  # Calculator
        modules.calc(group_id, uid, msg[5:])

    elif msg == 'news':  # News
        modules.get_news(group_id)

    # Times keywords
    elif 'technoblade' in msg or 'techno' in msg:
        timed.tech_no(group_id)

    # Economy
    # Command inspired from Discord bot: UnbelievaBoat
    elif msg == '^balance' or msg == '^bal':  # Current status
        economy.get_current(group_id, uid)
    elif msg == '^work':  # Get money
        economy.work(group_id, uid)

    elif msg == 'help':  # Help
        modules.help_(group_id)


def personal_main(msg: str, uid: str):
    """Get the keyword from msg and the sender's ID from the receive server, then do a correct response to it.

    Args:
        msg (str): The message someone sent.
        uid (str): The sender's ID.
    """
    msg = msg.lower()
    uid = str(uid)

    # Minecraft
    if msg[0:5] == 'query':  # Minecraft server detect
        personal_minecraft.mc_query(uid, msg[6:])
    elif msg[0:3] == 'hyp':  # Hypixel basic info
        personal_minecraft.hyp_basic_info(uid, msg[4:])
    elif msg[0:2] == 'bw':  # Hypixel bedwars info
        personal_minecraft.hyp_bedwars_info(uid, msg[3:])
    elif msg[0:2] == 'sb':  # Hypixel skyblock info
        personal_minecraft.hyp_skyblock_info(uid, msg[3:])

    elif msg == 'sexypic':  # Random sexypic
        personal_modules.sexypic(uid)
    elif msg == 'wotd':  # Wallpaper
        personal_modules.wotd(uid)

    elif msg[0:4] == 'calc':  # Calculator
        personal_modules.calc(uid, msg[5:])

    elif msg == 'news':  # News
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

    elif msg == 'help':  # Help
        personal_modules.help_(uid)


@app.route('/', methods=["POST"])
def server():
    """Get data of a receive message.
    """
    global bot

    data = request.get_json()  #  Get JSON data
    message = data['raw_message']  #  Get the message
    user_id = data['user_id']  # The user id of the sender
    if data['message_type'] == 'group':  # Only respond to group messages!
        if bot:
            main(message, user_id)  # Send to the get_keyword function to extract the keyword
        
        if message == 'bot':
            modules.send_public_message(group_id, '?')
        elif message == 'bot on':
            bot = True
            modules.send_public_message(group_id, 'Superior Bot now ON.')
        elif message == 'bot off':
            bot = False
            modules.send_public_message(group_id, 'Superior Bot now OFF.')
        elif message == 'bot stats':
            if bot:
                modules.send_public_message(group_id, 'Superior Bot now ON.')
            else:
                modules.send_public_message(group_id, 'Superior Bot now OFF.')
    elif data['message_type'] == 'private':
        if bot:
            personal_main(message, user_id)

        if message == 'bot':
            personal_modules.send(user_id, '?')
        elif message == 'bot on':
            if user_id == 2812862107:
                bot = True
                personal_modules.send(user_id, 'Superior Bot now ON.')
            else:
                personal_modules.send(user_id, 'Unauthorized.')
        elif message == 'bot off':
            if user_id == 2812862107:
                bot = False
                personal_modules.send(user_id, 'Superior Bot now OFF.')
            else:
                personal_modules.send(user_id, 'Unauthorized.')
        elif message == 'bot stats':
            if bot:
                personal_modules.send(user_id, 'Superior Bot now ON.')
            else:
                personal_modules.send(user_id, 'Superior Bot now OFF.')


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

    app.run(host=host, port=port)
