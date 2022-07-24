# Superior Bot

English version: [here](https://github.com/fToxicw5916/Superior-Bot/blob/release/README.md)     中文版本：[这里](https://github.com/fToxicw5916/Superior-Bot/blob/release/README-ch.md)

有史以来最好的聊天机器人 - Superior Bot!

## 这是什么？
Superior Bot是一个可以在QQ内使用的聊天机器人。它支持很多个功能，并且你可以快捷的在自己的电脑上运行。

## 基本使用方法
首先，你需要Python 3才能运行Superior Bot。你可以在[这里](https://python.org/)下载到它。

然后，你需要Go-CQHttp才能让Superior Bot发送/接受消息。你可以在[这里](https://docs.go-cqhttp.org/)下载到它。**注意！你需要在运行Go-CQHttp之前配置它！你可以在[这里](https://docs.go-cqhttp.org/guide/#go-cqhttp)找到如何做到这一点。**我强烈建议你把Go-CQHttp的二进制文件放到Superior Bot的文件夹里，这样可以给你节省不少时间。

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
