import imaplib
import re
import email.header
import requests

class Mailbox:
  def __init__(self, mail, mailbox, password, folder = 'Inbox'):
    if not mail or not mailbox or not password:
      raise Exception('Each parameter must not be empty') 
    self.mail = mail
    self.mailbox = mailbox
    self.__password = password
    self.folder = folder
    self.__login()
    
  def __login(self):
    try:
      self.__imap = imaplib.IMAP4_SSL(self.mail)
      self.__imap.login(self.mailbox, self.__password)
      uids = self.__getUnseenUids()
      self.__lastUid = max(uids) if len(uids) > 0 else -1
    except:
      raise Exception('Access denied. Check the data or the server permissions.')
    
  def getUnseenMails(self, allUnread = False):
    uids = self.__getUnseenUids()

    if not allUnread:
      uids = [int(uid) for uid in uids if int(uid) > self.__lastUid]

    if len(uids) == 0:
      return []
    
    mails = []
    for uid in uids:
      mail = {}
      try:
        tmp, text = self.__imap.uid('fetch', str(uid).encode('utf-8'), '(FLAGS RFC822.HEADER)')
        text = text[0][1].decode()
      except:
        continue
      else:
        # An easier way to get sender and subject is to use mail.parser.Parser
        mail['sender'] = self.__extractMailData(text, '\r\nFrom: (.*?)\r\n[\w]')
        mail['subject'] = self.__extractMailData(text, '\r\nSubject: (.*?)\r\n[\w]')
        mails.append(mail)
    
    if len(uids) > 0:
      self.__lastUid = max(uids)
    
    return mails
    
  def __extractMailData(self, source, regex):
    result = ''
    try: 
      data = re.search(regex, source, re.DOTALL)
      data = data.group(1)
      data = email.header.decode_header(data)
      for d in data:
        try:
          result += d[0].decode()
        except:
          result += d[0]
    except:
      result = ''
    finally:
      return result

  def __getUnseenUids(self):
    try:
      self.__imap.select(self.folder)
      result, uids = self.__imap.uid('search', None, "UNSEEN")
      uids = uids[0].decode().split(' ')
      uids = [int(uid) for uid in uids]
    except:
      return []
    else:
      return uids

class TgSender:
  
  __sendMessageUrl = 'https://api.telegram.org/bot<token>/sendMessage'

  def __init__(self, token, chatId):
    if not token or not chatId:
      raise Exception('Each parameter must not be empty') 
    self.__tgApiToken = token
    self.__sendMessageUrl = self.__sendMessageUrl.replace('<token>', token)
    self.__chatId = chatId
    
  def send(self, text):
    data = {'chat_id': self.__chatId, 'text': text}
    try:
      requests.post(self.__sendMessageUrl, data=data)
    except:
      print('Failed to send notification. Check the availability of Telegram servers (for example, Telegram website) from place where the script is running')
