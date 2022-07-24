# Superior Bot

English version: [here](https://github.com/fToxicw5916/Superior-Bot/blob/release/README.md)     中文版本：[这里](https://github.com/fToxicw5916/Superior-Bot/blob/release/README-ch.md)

有史以来最好的聊天机器人 - Superior Bot!

## 这是什么？
Superior Bot是一个可以在QQ内使用的聊天机器人。它支持很多个功能，并且你可以快捷的在自己的电脑上运行。

## 功能
- 计算器
- 我的世界服务器基础信息查询
- Hypixel信息查询
- Hypixel起床战争信息查询
- 新闻
- Sexy pic
- 必应的每日壁纸
- 还有更多！

## 基本使用方法
首先，你需要Python 3才能运行Superior Bot。你可以在[这里](https://python.org/)下载到它。

然后，你需要Go-CQHttp才能让Superior Bot发送/接受消息。你可以在[这里](https://docs.go-cqhttp.org/)下载到它。**注意！你需要在运行Go-CQHttp之前配置它！你可以在[这里](https://docs.go-cqhttp.org/guide/#go-cqhttp)找到如何做到这一点。**

我的世界服务器查询功能需要一个查询服务器来工作。首先，下载并安装[小皮面板](https://www.xp.cn/download.html)。启动服务器。找到服务器的运行目录，在里面新建一个叫做`mcp`的文件夹，然后把[这些](https://github.com/MCNewsTools/PHP-Minecraft-Query-API)文件放到`mcp`文件夹里。

然后，你需要下载Superior Bot本身。你可以在这个页面的右边 - Release里面找到它。请在使用前解压。

最后，打开你的命令行，使用`cd`命令来切换到Superior Bot的文件夹内。例如：`cd ~/Downloads/Superior-Bot`。然后，运行：
```bash
pip install -r requirements.txt
```
来安装需要的包。

现在，你已经准备完成，可以运行了！

首先，启动Go-CQHttp。运行：
```bash
sudo ./go-cqhttp
```
来启动。

然后，运行：
```bash
python main.py {你的QQ群号} {你的IP，默认127.0.0.1} {你的端口，默认9000}
```
来启动Superior Bot。**你的IP和端口应该和Go-CQHttp中你的配置相符！**

如果没有出现任何问题，你的群内，应该会收到一条消息：`Superior Bot now ONLINE!` 在聊天内发送`/help`来获取帮助。

## 高级设置
你应该注意到了，Superior Bot的文件夹内有一个叫做users.txt的文件。如果在机器人启动时你想使用私信告诉某个人，就把他的QQ号放到这个文件下。等机器人下一次启动时，那个文件内的所有人应该都会收到一条消息：`Superior Bot now ONLINE!`
