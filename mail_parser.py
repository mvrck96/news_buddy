import email
import os
import imaplib

with open("email_credits.txt", "r") as email_credits:
    user, pwd = [item.strip() for item in email_credits.readlines()]

print(user, pwd)
