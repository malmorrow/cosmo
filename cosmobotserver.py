import requests
import datetime

from django.contrib.auth.models import User


static_parties = '''
PinkParty 2018-10-06
HalloweenParty 2018-11-03
ChristmasParty 2018-12-01
NewYearsParty 2019-01-05
ValentinesParty 2019-02-02
'''

class BotHandler:


    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{token}/".format(token=token)
        self.updates = []
        self.last_update_id = 0
        self.timeout = 10


    def get_updates(self, offset=None, timeout=None):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        response = requests.get(self.api_url + method, data=params)
        result_json = response.json()['result']
        return result_json


    def send_message(self, chat_id, text):
        method = 'sendMessage'
        params = {'chat_id': chat_id, 'text': text}
        response = requests.post(self.api_url + method, params)
        return response


    def get_next_update(self):
        while len(self.updates) == 0:
            # Wait for get_updates to receive some updates from the bot
            print('No updates received, fetching more...')
            self.updates = self.get_updates(offset=self.last_update_id+1, timeout=self.timeout)
        # Now we have a list of updates, pop the first one
        next_update = self.updates.pop(0)
        # Store its update_id so that, if it's the last one, we wait for its successor the next time
        self.last_update_id = next_update['update_id']
        # return the update to the caller for processing
        return next_update


    def register(self, chat_id, username, first_name):
        user = User.objects.create_user(username=username, first_name=first_name)
        user.save()
        self.send_message(chat_id, '{username}, you are now registered as a Cosmo member.'.format(username=username))


    def unregister(self, chat_id, username):
        self.send_message(chat_id, '{username}, you are no longer registered as a Cosmo member.'.format(username=username))


    def listparties(self, chat_id):
        self.send_message(chat_id, static_parties)


token = '604198924:AAHZnFA40TlxJkp6yixiSpJ997AF8TaoTHw'
cosmo_bot = BotHandler(token)

help_text = '''
*CosmoBot*
I will help you register for Cosmo and attend Cosmo parties.
/help - This help text
/register - Register your Telegram user with Cosmo
/unregister - Remove your Telegram user from Cosmo
/list parties - List up-coming Cosmo parties
'''

extended_help_text = '''
/attend <partyname> - Attend a named party
/attend <yyyy-dd-mm> - Attend a party on a particular date
/attend next party - Attend the next party
'''

error_unknown_text = '''
@CosmoZaBot does not understand {text}
'''

def main():
    while True:
        update = cosmo_bot.get_next_update()
        update_id = update['update_id']
        chat_text = update['message']['text']
        chat_id = update['message']['chat']['id']
        username = update['message']['from']['username']
        first_name = update['message']['from']['first_name']
        if chat_text.lower() == '/help':
            cosmo_bot.send_message(chat_id, help_text)
        elif chat_text.lower() == '/register':
            cosmo_bot.register(chat_id, username, first_name)
        elif chat_text.lower() == '/unregister':
            cosmo_bot.unregister(chat_id, username)
        elif chat_text.lower() == '/list parties':
            cosmo_bot.listparties(chat_id)
        else:
            cosmo_bot.send_message(chat_id, error_unknown_text.format(text=chat_text))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

