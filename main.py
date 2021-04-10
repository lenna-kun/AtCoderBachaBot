import discord
# import asyncio
# import io
import textwrap

import datetime
import json
import random
import requests

def create_bacha(year, month, day, hour, minute, query):
    dt = datetime.datetime(year, month, day, hour, minute
        , tzinfo=datetime.timezone(datetime.timedelta(hours=9))
    )
    epoch = int(dt.timestamp())
    cookies = dict(token='**************************')
    response = requests.post(
        'https://kenkoooo.com/atcoder/internal-api/contest/create',
        json.dumps({
            'title': 'ABC Random Contest',
            'memo': '',
            'start_epoch_second': epoch,
            'duration_second': 3600,
            'mode': None,
            'penalty_second': 300,
            'is_public': False
        }),
        headers={'Content-Type': 'application/json'},
        cookies=cookies
    )
    contest_id = response.json()['contest_id']
    problems = []
    for i in range(len(query)):
        problems.append({
            'id': f'abc{random.randrange(126, 195)}_{query[i]}',
            'point': 100*(ord(query[i])-ord('a')+1),
            'order': i
        })
    response = requests.post(
        'https://kenkoooo.com/atcoder/internal-api/contest/item/update',
        json.dumps({
            'contest_id': contest_id,
            'problems': problems
        }),
        headers={'Content-Type': 'application/json'},
        cookies=cookies
    )
    return f'https://kenkoooo.com/atcoder/#/contest/show/{contest_id}'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('#create'):
        query = message.content.split()
        date = query[1].split('/')
        time = date[3].split(':')
        if len(query[2]
            .replace('a', '')
            .replace('b', '')
            .replace('c', '')
            .replace('d', '')
            .replace('e', '')
            .replace('f', '')) > 0:
            await message.reply('Failed.')
            return

        url = create_bacha(int(date[0]), int(date[1]), int(date[2])
            , int(time[0]), int(time[1]), query[2])
        await message.reply(textwrap.dedent(f"""\
            Successfully created!
            {url}\
        """))

client.run('**************************')