import sys
import json
import getpass
from datetime import datetime, timedelta
import time
from PyPtt import PTT

ptt_bot = PTT.API()
Year = datetime.now().year
ID = None
Password = None

def main():
    global ID, Password
    try:
        with open('Account.json') as AccountFile:
            Account = json.load(AccountFile)
            ID = Account['ID']
            Password = Account['Password']
    except FileNotFoundError:
        ID = input('your ID:')
        Password = getpass.getpass('your PW:')

    connect()

    newest_dt = datetime.today().replace(hour=0, minute=0)
    while True:
        try:
            newest_dt = watcher(newest_dt)
            time.sleep(5)
        except KeyboardInterrupt:
            break
        except:
            time.sleep(5)
            newest_dt = newest_dt + timedelta(minutes=-5)
            connect()
    try:
        ptt_bot.logout()
    except:
        pass

def connect():
    while True:
        try:
            ptt_bot.login(ID, Password, kick_other_login=True)
            break
        except KeyboardInterrupt:
            break
        except:
            time.sleep(5)

def watcher(newest_dt = datetime.today):
    this_newest_dt = newest_dt
    post_info = ptt_bot.get_post(
        'NSwitch',
        post_aid='1U3sZEM5'
    )
    if post_info is None:
        print('post_info is None')
        return newest_dt

    new_data = []
    for push_info in post_info.push_list:
        dt = parseStr2Datetime(push_info.time)
        if dt is not None and dt > newest_dt:
            print('{time} {author} -> {content}'.format(
                author=push_info.author.rjust(11), 
                time=push_info.time, 
                content=push_info.content))
            this_newest_dt = dt
    
    return this_newest_dt

def parseStr2Datetime(dt_str):
    try:
        return datetime.strptime(str(Year) + "/" + dt_str, "%Y/%m/%d %H:%M")
    except Exception as ex:
        print(ex)
        return None

if __name__ == '__main__':
    main()