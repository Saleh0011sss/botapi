# -*- coding: utf-8 -*-
import telebot # Library of API bot.
from telebot import types # Types from API bot
import time 
import random
import datetime
import codecs
import sys
import json
from os.path import exists
import os
import re
import logging
import urllib
import urllib2
reload(sys)
sys.setdefaultencoding("utf-8")

owner = 184018132
TOKEN = 'your token here'
bot = telebot.TeleBot(TOKEN) # Creating our bot object.
bot.skip_pending=True
#######################################
#TRIGGERS SECTION
triggers = {}
tfile = "triggers.json"
ignored = []
separator = '/'
#user = [line.rstrip('\n') for line in open('user.txt','rt')]

#Check if Triggers file exists and load, if not, is created.
if exists('triggers.json'):
    with open('triggers.json') as f:
        triggers = json.load(f)
    print('Triggers file loaded.')
else:
    with open('triggers.json', 'w') as f:
        json.dump({}, f)

#Function to save Triggers - Response
def save_triggers():
    with open('triggers.json', 'w') as f:
        json.dump(triggers, f)
    print('Triggers file saved.')
    
#Function to get triggers list for a group.
def get_triggers(group_id):
    if(str(group_id) in triggers.keys()):
        return triggers[str(group_id)]
    else:
        return False
    
#Function to check if a message is too old(60 seconds) to answer.
def is_recent(m):
    return (time.time() - m.date) < 60   


added_message = '''
New Trigger Created:
Trigger [{}]
Response [{}]
'''
#END TRIGGERS SECTION
######################################

######################################
#Triggers Management Section
#Adds another trigger-response. ex: "/add Hi / Hi!! :DD"
@bot.message_handler(commands=['add'])
def add(m):
    if(m.reply_to_message):
        if(m.reply_to_message.text):
            if(len(m.reply_to_message.text.split()) < 2):
                bot.reply_to(m, 'Bad Arguments. Try with /add [trigger] / [response]')
                return
            trigger_word = m.text.split(' ', 1)[1].strip()
            trigger_response = m.reply_to_message.text.strip()
        else:
            bot.reply_to(m, 'Only text triggers are supported.')
            return
    else:    
        if(len(m.text.split()) < 2):
            bot.reply_to(m, 'Bad Arguments. Try with /add [trigger] / [response]')
            return
        if(m.text.find(separator, 1) == -1):
            bot.reply_to(m, 'Separator not found. Try with /add [trigger] / [response]')
            return
        rest_text = m.text.split(' ', 1)[1]
        trigger_word = rest_text.split(separator)[0].strip()
        trigger_response = rest_text.split(separator, 1)[1].strip()

    if(len(trigger_word) < 2):
        bot.reply_to(m, 'Trigger too short. [chars < 2]')
        return
    if(len(trigger_response) < 1):
        bot.reply_to(m, 'Invalid Response.')
        return
    if(m.chat.type in ['group', 'supergroup']):
        if(get_triggers(m.chat.id)):
            get_triggers(m.chat.id)[trigger_word] = trigger_response
        else:
            triggers[str(m.chat.id)] = {trigger_word : trigger_response}
        msg = added_message.format(trigger_word, trigger_response)
        bot.reply_to(m, msg)
        save_triggers()
    else:
        if(m.chat.id != owner):
            return

@bot.message_handler(commands=['del'])
def delete(m):
    if(len(m.text.split()) < 2):
        bot.reply_to(m, 'Bad Arguments')
        return
    del_text = m.text.split(' ', 1)[1].strip()
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg and del_text in trg.keys()):
            trg.pop(del_text)
            bot.reply_to(m, 'Trigger [{}] deleted.'.format(del_text))
            save_triggers()
        else:
            bot.reply_to(m, 'Trigger [{}] not found.'.format(del_text))

#Answers with the size of triggers.
@bot.message_handler(commands=['size'])
def size(m):
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg):
            msg = 'Size of Triggers List = {}'.format(len(trg))
            bot.reply_to(m, msg)
        else:
            bot.reply_to(m, 'Size of Triggers List = 0')

@bot.message_handler(commands=['all'])
def all(m):
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg):
            if(len(trg.keys()) == 0):
                bot.reply_to(m, 'This group doesn\'t have triggers.')
            else:
                bot.reply_to(m,'Trigers:\n' + '\n'.join(trg))
        else:
            bot.reply_to(m, 'This group doesn\'t have triggers.')

#End Triggers Management Section
#######################################

# Search function used as easter eggs
#find_python = re.compile(r"(?i)\bPYTHON\b").search

@bot.message_handler(commands=['hhelp']) 
def command_ayuda(m): 
    cid = m.chat.id
    bot.send_message( cid, "*Triggers settings(Groups only!)*\n/add trigger/answer \n/del trigger \n/size \n/all \n*Markdown settings* \n/format *hi* _hi_ `hi`\n*Others* \n/weather city \n/map city \n/arz \n/spotify artist|song \n/whois url \n/qr text  \n/time \n/hola \n/hello \n/roll \n/id \n*Extras* \n/fuckyou \n/coding \n/attack \n🐙Squidward v1") #

@bot.message_handler(commands=['creator', 'ping']) 
def command_creator(m): 
    cid = m.chat.id 
    bot.send_message( cid, '🔵Squidward V.1 by Electrovirus')

@bot.message_handler(commands=['start']) 
def command_start(m): 
    cid = m.chat.id 
    bot.send_message( cid, '🐙Hello \n🐙Wellcome to squidwardBot V.1 \n🐙A fun bot based on python \n🐙Developed by Electrovirus \n\n🐙Use /help to see bot commands')

@bot.message_handler(commands=['help'])
def welcome(m):
        bot.send_chat_action(m.chat.id, 'typing')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Squidward Bot ', callback_data='next'))
        markup.add(types.InlineKeyboardButton('Version 1 ', switch_inline_query=''))
        bot.send_message(m.chat.id,
        """
<b>Wellcome 
I am squidward the tentacle
These are what i can do</b>

<i>/help 《show this text》
/format [Text]  《*bold* _italic_ `code`》
/time 《local time》 
/dog [Text] 《dogify》
/gif [Text] 《make gifs》
/qr [text] 《make qr codes》
/short [link] 《link shorter》
/kickme 《leave group》
/id 《Your id & info》
/logo [Url] 《Website logo》
/imdb [movie name] 《movie info in imdb》
/voice [text] 《text to speech》
/whois [domain name] 《domain informations》
/love [name] [name] 《make a love queto photo》
/map [City] 《Map screen》
/spotify [Name Track] 《track info》
/weather [City] 《shows city weather》
/webshot [URL] 《Take a photo of url》
/arz 《Arz And Gold price》
/roll 《roll a dice》
/hello 《say hello》
/hola 《say hola》</i>

<b>Triggers settings</b> *Groups only

<i>/add trigger / reaponse 《add a trigger》
/del trigger 《delete a trigger》
/size 《count of the triggers》
/all 《list of triggers》</i>

<b>Extras</b>

<i>/fuckyou 
/coding
/attack</i>


        """, parse_mode='HTML', reply_markup=markup)

@bot.message_handler(commands=['id', 'ids', 'info', 'me'])
def id(m):      # info menu
    cid = m.chat.id
    title = m.chat.title
    usr = m.chat.username
    f = m.chat.first_name
    l = m.chat.last_name
    t = m.chat.type
    d = m.date
    text = m.text
    p = m.pinned_message
    fromm = m.forward_from
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("\xF0\x9F\x98\x8A Squidward bot \xF0\x9F\x98\x8A", url="https://telegram.me/squidward_bot"))
#info text
    bot.send_chat_action(cid, "typing")
    bot.reply_to(m, "*ID from* : ```{}``` \n\n *Chat name* : ```{}``` \n\n\n *Your Username* : ```{}``` \n\n *Your First Name* : ```{}```\n\n *Your Last Name* : ```{}```\n\n *Type From* : ```{}``` \n\n *Msg data* : ```{}```\n\n *Your Msg* : ```{}```\n\n* pind msg * : ```{}```\n\n *from* : ```{}```".format(cid,title,usr,f,l,t,d,text,p,fromm), parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=['gif'])
def aparat(m):
    text = m.text.replace('/gif ','')
    url = "http://www.flamingtext.com/net-fu/image_output.cgi?_comBuyRedirect=false&script=blue-fire&text={}&symbol_tagname=popular&fontsize=70&fontname=futura_poster&fontname_tagname=cool&textBorder=15&growSize=0&antialias=on&hinting=on&justify=2&letterSpacing=0&lineSpacing=0&textSlant=0&textVerticalSlant=0&textAngle=0&textOutline=off&textOutline=false&textOutlineSize=2&textColor=%230000CC&angle=0&blueFlame=on&blueFlame=false&framerate=75&frames=5&pframes=5&oframes=4&distance=2&transparent=off&transparent=false&extAnim=gif&animLoop=on&animLoop=false&defaultFrameRate=75&doScale=off&scaleWidth=240&scaleHeight=120&&_=1469943010141".format(text)
    res = urllib.urlopen(url)
    parsed_json = json.loads(res.read())
    gif = parsed_json['src']
    link = parsed_json['gimpHost']
    urllib.urlretrieve("{}".format(gif), "gif.gif")
    bot.send_document(m.chat.id, open('gif.gif'), caption="@Squidward_Bot")


@bot.message_handler(regexp='^(/download) (.*)')
def all(m):
    text = m.text.split()[1]
    id = m.from_user.id
      try:
         if m.chat.type == 'private':
             if re.match('(http|https)://.*.(png)$',text):
                 msg = bot.send_message(m.chat.id, '*Downloading.....*',parse_mode='Markdown')
                 dw(text,'file.png')
                 bot.send_photo(m.chat.id, open('file.png'),caption='@Squidward_bot')
                 os.remove('file.png')
             if re.match('(http|https)://.*.(apk)$',text):
                 msg = bot.send_message(m.chat.id, '*Downloading .....*',parse_mode='Markdown')
                 dw(text,'app.apk')
                 bot.send_document(m.chat.id, open('app.apk'),caption='@Squidward_bot')
                 os.remove('app.apk')
             if re.match('(http|https)://.*.(html|htm)$',text):
                 msg = bot.send_message(m.chat.id, '* Downloading .....*',parse_mode='Markdown')
                 dw(text,'file.html')
                 bot.send_document(m.chat.id, open('file.html'),caption='@Squidward_bot')
                 os.remove('file.html')
             if re.match('(http|https)://.*.(jpg)$',text):
                 msg = bot.send_message(m.chat.id, '* Downloading .....*',parse_mode='Markdown')
                 dw(text,'s.jpg')
                 bot.send_photo(m.chat.id, open('s.jpg') ,caption='@Squidward_bot')
                 os.remove('s.jpg')
             if re.match('(http|https)://.*.(gif)$',text):
                 msg = bot.send_message(m.chat.id, '* Downloading .....*',parse_mode='Markdown')
                 dw(text,'s.gif')
                 bot.send_photo(m.chat.id, open('s.gif'),caption='@Squidward_bot')
                 os.remove('s.gif')
             if re.match('(http|https)://.*.(zip|rar)$',text):
                 msg = bot.send_message(m.chat.id, '* Downloading .....*',parse_mode='Markdown')
                 dw(text,'file.zip')
                 bot.send_document(m.chat.id, open('file.zip'),caption='@Squidward_bot')
                 os.remove('file.zip')
             if re.match('(http|https)://.*.(webp)$',text):
                 msg = bot.send_message(m.chat.id, '* Downloading .....*',parse_mode='Markdown')
                 dw(text,'file.webp')
                 bot.send_sticker(m.chat.id, open('file.webp'))
                 os.remove('file.webp')
      except IndexError:
                 bot.send_message(m.chat.id, '*Error!\nURL Or Format Is Invalid!*',parse_mode='Markdown')

@bot.message_handler(commands=['weather'])
def wt(m):
        try:
            icons = {'01d': '🌞',
             '01n': '🌚',
             '02d': '⛅️',
             '02n': '⛅️',
             '03d': '☁️',
             '03n': '☁️',
             '04d': '☁️',
             '04n': '☁️',
             '09d': '🌧',
             '09n': '🌧',
             '10d': '🌦',
             '10n': '🌦',
             '11d': '🌩',
             '11n': '🌩',
             '13d': '🌨',
             '13n': '🌨',
             '50d': '🌫',
             '50n': '🌫',
             }
            icons_file = {
            '01d': '01d',
            '01n': '01n',
            '02d': '02d',
            '02n': '02n',
            '03d': '03d',
            '03n': '03n',
            '04d': '04d',
            '04n': '04n',
            '09d': '09d',
            '09n': '09n',
            '10d': '10d',
            '10n': '10n',
            '11d': '11d',
            '11n': '11n',
            '13d': '13d',
            '13n': '13n',
            '50d': '50d',
            '50n': '50n',
            }
            text = m.text.split(' ',1)[1]
            url = urllib.urlopen('http://api.openweathermap.org/data/2.5/weather?q={}&appid=269ed82391822cc692c9afd59f4aabba'.format(text))
            d = url.read()
            data = json.loads(d)
            wt = data['main']['temp']
            feshar = data['main']['pressure']
            wind = data['wind']['speed']
            icon = data['weather'][0]['icon']
            texttt = icons[icon]
            wt_data = int(wt)-273.15
            bot.send_message(m.chat.id, '\xD8\xAF\xD9\x85\xD8\xA7 : {}\n\n\xD8\xB3\xD8\xB1\xD8\xB9\xD8\xAA\x20\xD8\xA8\xD8\xA7\xD8\xAF : {}/s\n\n\xD9\x81\xD8\xB4\xD8\xA7\xD8\xB1\x20\xD9\x87\xD9\x88\xD8\xA7 : {}\n\n {}'.format(wt_data,wind,feshar,texttt))
            texty = icons_file[icon]
            files = open('./weather/'+texty+'.png')
            bot.send_sticker(m.chat.id, files)
        except (IndexError):
            bot.send_message(m.chat.id, 'Error\n/weather tehran')
        except IOError:
            print 'not send sticker weather'

@bot.message_handler(commands=['kickme'])
def answer(m):
    bot.kick_chat_member(m.chat.id, m.from_user.id)

@bot.message_handler(commands=['short'])
def send_pic(m):
      try:
        text = m.text.replace("/short ","")
        res = urllib.urlopen("http://yeo.ir/api.php?url={}".format(text)).read()
        bot.send_message(m.chat.id, "*Your Shorten Link :* {}".format(res), parse_mode="Markdown", disable_web_page_preview=True)
      except:
        bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

@bot.message_handler(regexp='^(/love) (.*) (.*)')
def love(m):
        text = m.text.split()[1]
        tezt = m.text.split()[2]
        urllib.urlretrieve("http://www.iloveheartstudio.com/-/p.php?t={}%20%EE%BB%AE%20{}&bc=000000&tc=FFFFFF&hc=ff0000&f=c&uc=true&ts=true&ff=PNG&w=500&ps=sq".format(text,tezt), "love.png")
        bot.send_sticker(m.chat.id, open('love.png'))

@bot.message_handler(regexp='^(/imdb) (.*)')
def m(m):
        try:
            r = urllib.urlopen('http://www.omdbapi.com/?t={}&'.format(m.text.replace('/imdb','')))
            data = r.read()
            pjson = json.loads(data)
            title = pjson['Title']
            year = pjson['Year']
            runtime = pjson['Runtime']
            genre = pjson['Genre']
            language = pjson['Language']
            poster = pjson['Poster']
            urllib.urlretrieve(poster, 'imdb.jpg')
            bot.send_message(m.chat.id, """
<b>Movie name</b> : {}
<b>Year of action</b> : {}
<b>Movie time</b> : {}
<b>Movie sort</b> : {}
<b>Language</b> : {}
            """.format(title,year,runtime,genre,language), parse_mode='HTML')
            bot.send_sticker(m.chat.id, open('imdb.jpg'))
        except IOError:
            bot.send_message(m.chat.id, """
<b>Movie name</b> : {}
<b>Year of action</b> : {}
<b>Movie time</b> : {}
<b>Movie sort</b> : {}
<b>Language</b> : {}
            """.format(title,year,runtime,genre,language), parse_mode='HTML')
        except KeyError:
            bot.send_message(m.chat.id, 'Error')

@bot.message_handler(regexp='^(/logo) (.*)')
def log(m):
        if m.text.split()[1]:
            text = m.text.split()[1]
            urllib.urlretrieve("http://logo.clearbit.com/{}?size=500&".format(text), "logo.png")
            bot.send_sticker(m.chat.id, open('logo.png'))

@bot.message_handler(regexp='^(/voice) (.*)')
def voice(m):
        urllib.urlretrieve("http://tts.baidu.com/text2audio?lan=en&ie=UTF-8&text={}&".format(m.text.replace('/voice', '')), "voice.ogg")
        bot.send_voice(m.chat.id, open('voice.ogg'))

@bot.message_handler(commands=['dog'])
def d(m):
        text = m.text.replace('/dog', '')
        urllib.urlretrieve("http://dogr.io/{}.png?split=false&s.png".format(text), "s.png")
        bot.send_photo(m.chat.id, open('s.png'))

@bot.message_handler(regexp='^(/webshot) (.*)')
def web(m):
        urllib.urlretrieve("http://api.screenshotmachine.com/?key=b645b8&size=X&url={}".format(m.text.replace('/webshot', '')), "web.jpg")
        bot.send_photo(m.chat.id, open('web.jpg'))

@bot.message_handler(commands=['qr'])
def qr(m):
        text = m.text.replace('/qr', '')
        urllib.urlretrieve("https://api.qrserver.com/v1/create-qr-code/?size=1200x800&data={}&bgcolor=ffff00&".format(text), "qr.png")
        bot.send_photo(m.chat.id, open('qr.png'))
   
@bot.message_handler(regexp='^(/kick) (.*)')
def cap(m):
    if str(m.from_user.id) == owner:
        text = m.text.split()[1]
        bot.kick_chat_member(m.chat.id, text)
        bot.send_message(m.chat.id, 'Kicked {}'.format(text))
        return
    if str(m.from_user.id) not in owner:
        bot.send_message(m.chat.id, 'Just bot owner')
        return

@bot.message_handler(commands=['kick'])
def kick(m):    
    if m.from_user.id == owner:
        if m.reply_to_message:
            bot.kick_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            bot.send_message(m.chat.id, 'kicked <code>{}</code>'.format(m.reply_to_message.from_user.id), parse_mode='HTML')

@bot.message_handler(commands=['map'])
def map(m):
        try:
            text = m.text.split(" ", 1)[1]
            data = text.encode('utf-8')
            urllib.urlretrieve('https://maps.googleapis.com/maps/api/staticmap?center={}&zoom=14&size=400x400&maptype=hybrid&key=AIzaSyBmZVQKUXYXYVpY7l0b2fNso4z82H5tMvE'.format(data), 'map.png')
            bot.send_sticker(m.chat.id, open('map.png'))
            os.remove('map.png')
        except IndexError:
            bot.send_message(m.chat.id, '<b>Error</b>',parse_mode='HTML')

@bot.message_handler(commands=['arz'])
def arz(m):
        url = urllib.urlopen('http://exchange.nalbandan.com/api.php?action=json')
        data = url.read()
        js = json.loads(data)
        dollar = js['dollar']['value']
        euro = js['euro']['value']
        gold_per_geram = js['gold_per_geram']['value']
        pond = js['pond']['value']
        text = '\xD8\xAF\xD9\x84\xD8\xA7\xD8\xB1 : '+dollar+'\n\xDB\x8C\xD9\x88\xD8\xB1\xD9\x88 : '+euro+'\n\xD8\xB7\xD9\x84\xD8\xA7\xDB\x8C\x20\x31\x38\x20\xD8\xB9\xDB\x8C\xD8\xA7\xD8\xB1 : '+gold_per_geram+'\n\xD9\xBE\xD9\x88\xD9\x86\xD8\xAF : '+pond
        bot.send_message(m.chat.id, text)

@bot.message_handler(commands=['spotify'])
def m(m):
        try:
            url = urllib.urlopen("https://api.spotify.com/v1/search?limit=1&type=track&q={}".format(m.text.replace('/spotify','')))
            data = url.read()
            js = json.loads(data)
            files = js['tracks']['items'][0]['preview_url']
            name = js['tracks']['items'][0]['name']
            pic = js['tracks']['items'][0]['album']['images'][1]['url']
            art = js['tracks']['items'][0]['artists'][0]['name']
            bot.send_message(m.chat.id, '<b>Name</b> : {}\n<b>Artist : </b>{}'.format(name,art),parse_mode='HTML')
            bot.send_chat_action(m.chat.id, 'record_audio')
            urllib.urlretrieve(files,'spotify.mp3')
            urllib.urlretrieve(pic,'spotify.png')
            bot.send_audio(m.chat.id, open('spotify.mp3'), title=name)
            bot.send_sticker(m.chat.id, open('spotify.png'))
            hash = 'spotify'
            os.remove('spotify.mp3')
            os.remove('spotify.png')
            print ' send /spotify'
        except KeyError:
            bot.send_message(m.chat.id, 'Error')
        except IndexError:
            bot.send_message(m.chat.id, 'Error')
        except IOError:
            bot.send_message(m.chat.id, 'Error')

@bot.message_handler(commands=['whois'])
def whois(m):
        try:
            cid = m.chat.id
            text = m.text
            input = text.split()[1]
            req = urllib2.Request("http://www.whoisxmlapi.com/whoisserver/WhoisService?domainName={}&outputFormat=JSON".format(input))
            opener = urllib2.build_opener()
            f = opener.open(req)
            parsed_json = json.loads(f.read())
            output = parsed_json['WhoisRecord']['rawText']
            bot.send_message(cid,output)
        except KeyError:
            bot.send_message(m.chat.id, 'Error')
        except IndexError:
            bot.send_message(m.chat.id, '/whois [Domain Name]')

@bot.message_handler(commands=['hola']) 
def command_hola(m): 
    cid = m.chat.id 
    bot.send_message( cid, 'Hola, Dadach 😀😀') 

@bot.message_handler(commands=['hello']) 
def command_hello(m): 
    cid = m.chat.id 
    bot.send_message( cid, 'Hello and welcome Dadach😀😀') 

@bot.message_handler(commands=['attack']) 
def command_attack(m): 
    cid = m.chat.id 
    bot.send_photo( cid, open( './imagenes/dictionary_attack.jpg', 'rb')) 


@bot.message_handler(commands=['roll']) 
def command_roll(m): 
    cid = m.chat.id 
    bot.send_message( cid, random.randint(1,6) )

@bot.message_handler(commands=['time'])
def command_time(m): 
    cid = m.chat.id 
    bot.send_message( cid, str(datetime.datetime.now())) 

@bot.message_handler(commands=['coding']) 
def command_coding(m): 
    cid = m.chat.id 
    bot.send_photo( cid, open( './imagenes/coding.jpg', 'rb')) 

@bot.message_handler(commands=['format'])
def command_format(m):
    cid = m.chat.id
    try:
        bot.send_message( cid, m.text.split(None,1)[1],parse_mode='markdown')
    except IndexError:
        bot.send_message( cid, "Argument missing" )
    except Exception:
        bot.send_message( cid, "Invalid argument" )

@bot.message_handler(commands=['fuckyou']) 
def command_fuckyou(m): 
    cid = m.chat.id 
    bot.send_document( cid, open( './imagenes/fuckyou.mp4', 'rb')) 

@bot.message_handler(func=lambda m: True)
def response(m):
    if(m.chat.type in ['group', 'supergroup']):
        trg = get_triggers(m.chat.id)
        if(trg):
            for t in trg.keys():
                if t.lower() in m.text.lower():
                    bot.reply_to(m, trg[t])

print('Functions loaded')
