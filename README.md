# Telegram email notifications

Sometimes mail client notifications don't work very well. There is a script that checks the mailbox and sends notifications of new email messages via Telegram

1. Find **@botfather** bot in Telegram
2. Get API Token of the bot and set it to a variable **tgApiToken** in the script
3. Get updates of the bot via the next link **`https://api.telegram.org/bot<token>/getUpdates`**. It will be empty, but `{ ok: true }`

4. You need to get chatId of the chat which the bot will send notifications. If you have a team I recommend using a group because it's easy to manage notification recipients simply by managing group members

  - If you want to use bot with a group you should create a group with the bot. I noticed that when you add a second administrator to the group, *your group becomes a supergroup and changes Id*. I recommend adding a second administrator at once (this may be the bot itself). When the group is created, the bot is added and you have two or more administrators, for the next step you should write something to the group

  - If you want to get notifications in personal chat with the bot you should write to bot directly

5. Get updates of the bot via the link **`https://api.telegram.org/bot<token>/getUpdates`**. You can see your message with chat Id in the response. The group chat Id must be a negative number. If there is empty, you can write something to the group or remove the bot from the group and add it, then check the link again

6. Set the variable **chatId** in the script with chat Id you get from the previous step

7. You should set mailServer, mailAddress and mailPassword variables
- **mailServer** - typically it looks like **mail.example.com**
- **mailAddress** - typically it looks like **user@example.com**, but sometimes it can be without @ (at) and domain like just **user**
- **mailPassword** - password of the account
	
8. Run script for testing **`python3 main.py`**. Send some mails to your mailbox

9. Run script in background **`python3 main.py &`**
	
---

Typical problems
1. Users in a mail server can be without @ (at) and domain name
2. If Telegram is blocked in your country and you try to open getUpdates link or run the script on your computer it may not be work
3. Some services like Gmail block untrusted connections. You should check permissions if the script fails

