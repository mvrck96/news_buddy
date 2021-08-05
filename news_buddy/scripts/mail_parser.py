import imaplib


with open("email_credits.txt", "r") as email_credits:
    # Use yandex app passwords for better security
    user, pwd = [item.strip() for item in email_credits.readlines()]
if user.split("@")[1].split(".")[0] == "yandex":
    imap = imaplib.IMAP4_SSL("imap.yandex.ru", 993)
else:
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(user, pwd)
status, messages = imap.select("INBOX")
messages = int(messages[0])
print(messages)
