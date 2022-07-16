# Bot++
The best chat bot ever - Bot++!

## What is it?
Bot++ is a bot that can be used easily for QQ. It supports a lot of functions and can be easily set up on your own computer.

## Usage
### Pre-installation
First, you will need Python 3 to run Bot++. You can download it [here](https://www.python.org/).

Then, you will need Go-CQHttp for Bot++. Go-CQHttp is a application so that the bot can send messages and receive messages from QQ. You can download it [here](https://github.com/Mrs4s/go-cqhttp/releases). I suggest you download the lastest version and the binary file instead of the zip file. **You need to configure Go-CQHttp before use! You can find how to do that [here](https://docs.go-cqhttp.org/guide/#go-cqhttp)**

Then, download Bot++. Just download it's source code by cloning the repo using Git or just download it. Unzip the file before you use!

Next, open your terminal. Use `cd` to get to the directory where Bot++ is. Use
```bash
pip install -r requirements.txt
```
to install the packages.

Now, you are ready to go!

### How can you use it?
First, boot up Go-CQHttp: (**Configure before use!!!**)
```bash
sudo ./go-cqhttp
```
Then, You can run Bot++ by using the following command:
```bash
python main.py {Your group ID here}
```
where "{Your group ID here}" should be replaced to the group's ID you want Bot++ to be in.