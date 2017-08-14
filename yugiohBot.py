import praw
import time
import re
import requests
import json

# Location of file where id's of already visited comments are maintained
path = 'C:\\Users\\eptay\\Downloads\\ygo1-master\\ygo1-master\\commented.txt'

# Location of file where id's of already visited comments are maintained
class YgoCard(object):
    def __init__(self, name, average, cardID, rarity):
        self.name = name
        self.average = average
        self.cardID = cardID
        self.rarity = rarity

def authenticate():

    print('Authenticating...\n')
    reddit = praw.Reddit('yugiohBot', user_agent = 'yugiohBot v0.1 (by /u/talkingtomyselff)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def getCardData(cardID):

    url = 'http://yugiohprices.com/api/price_for_print_tag/{}'.format(cardID)
    myResponse = requests.get(url)
    print(myResponse)
    if(myResponse.ok):
        # convert response from bytes to string
        bytesValue = myResponse.content
        jData = json.loads(bytesValue.decode("utf-8"))
        print(jData)
        # Get necessary information from response: card name, average price, ID, rarity
        # yugiohprices api response format is very messy, includes unnecessary nested objects

        data = jData['data']

        cardName = data['name']
        print(cardName)

        price_data = data['price_data']
        rarity = price_data['rarity']
        print(rarity)

        price_data = price_data['price_data']
        data = price_data['data']
        prices = data['prices']
        average = prices['average']
        print(average)
        card = YgoCard(cardName, average, cardID, rarity)
        return card

def run_yugiohBot(reddit):
        card = None
        regex = r"[a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z][-][a-zA-Z][a-zA-Z]\d\d\d"
        for comment in reddit.subreddit('test').comments(limit = 250):

            match = re.search(regex, comment.body)

            if match:
                print("ID found in comment with comment ID: " + comment.id)
                cardID = match.string
                cardID.upper()
                file_obj_r = open(path,'r')
                print(cardID)

                try:
                    card = getCardData(cardID)
                except:
                    print('Exception!!! Possibly incorrect cardID...\n')
                else:
                    if comment.id not in file_obj_r.read().splitlines():
                        print('comment is unique.. posting price\n')
                        comment.reply('The average price of ' + str(card.cardID)  + ' ' + str(card.name) + ' is $' + str(card.average))

                        file_obj_r.close()

                        file_obj_w = open(path, 'a+')
                        file_obj_w.write(comment.id + '\n')
                        file_obj_w.close()

                    else:
                        print('Already gave price...no reply needed\n')
                time.sleep(10)

        print('Waiting 60 seconds...\n')
        time.sleep(60)

def main():
    reddit = authenticate()
    while True:
        run_yugiohBot(reddit)


if __name__ == '__main__':
    main()
