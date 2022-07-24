# Superior Bot

English version: [here](https://github.com/fToxicw5916/Superior-Bot/blob/release/README.md)     中文版本：[这里](https://github.com/fToxicw5916/Superior-Bot/blob/release/README-ch.md)

The best chat bot ever - Superior Bot!

## What is it?
Superior Bot is a bot that can be used easily for QQ. It supports a lot of functions and can be easily set up on your own computer.

## Basic-usage
First, you need Python 3 in order to run Superior Bot. You can download and install it [here](https://python.org/).

Then, you will need Go-CQHttp to support Superior Bot to receive and send messages. You can download it [here](https://docs.go-cqhttp.org/). **You need to configure Go-CQHttp to fit you before use! You can find out how to do that [here](https://docs.go-cqhttp.org/guide/#go-cqhttp)!** I strongly suggest you put the binary file in the Superior Bot's folder. That can save you a lot of trouble.

At last, you need to download the Superior Bot itself. You can find it at the right side of this page - Release. Unzip it before use.

Then, open up your terminal and use the `cd` command to get to Superior Bot's folder. For example, `cd ~/Downloads/Superior-Bot`. Then, run:
```bash
pip install -r requirements.txt
```
to install the required packages.

Now, you are ready to go!

First, boot up Go-CQHttp. Run:
```bash
sudo ./go-cqhttp
```
and wait until it is fully boot up.

Then, run:
```bash
python main.py {Your target group ID} {Your IP, default 127.0.0.1} {Your port, default 9000}
```
to boot up Superior-Bot. **Your IP and port should fit your settings in Go-CQHttp!**

If nothing went wrong, in the target group, you should see a message `Superior-Bot now ONLINE!`. Try to send `/help` into the chat to get some help from Superior Bot!

# Advanced settings
You should noticed that there is a users.txt file in the Superior-Bot's folder. If you want to tell someone via private chat that the Superior Bot is online, you can put their ID into that file. Then, when Superior Bot boot up, it should send a message to everyone in that file `Superior-Bot now ONLINE!`.
