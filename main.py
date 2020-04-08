import mailbot
import time

chatId = '-123456789'
tgApiToken = '123456789:abc'
mailServer = 'mail.example.com'
mailAddress = 'user@example.com'
mailPassword = 'password'
mailFolder = 'Inbox'

mailbox = mailbot.Mailbox(mailServer, mailAddress, mailPassword, mailFolder)
sender = mailbot.TgSender(tgApiToken, chatId)

print('Start checking..')
while(1):
	emails = mailbox.getUnseenMails(False)

	for email in emails:
		print(email)
		data = str(email['sender']) + '\n\n' + str(email['subject'])
		sender.send(data)

	time.sleep(30)
		
		
