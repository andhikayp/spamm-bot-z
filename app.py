from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json

import errno
import os
#import datetime
import sys, random
import tempfile
import requests
import re

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('t5b5X0LHwCZQHy55X75+FZfjBWBDfvw+NWgDIruLX/EoslSALtJHPdaBsVRlkjFUeQRscNzXPtkTI8dYZH6I+ku1yyGazFjq8KShojdmcowVeXZYWNjkd7oT5nAxHZIK8q+lM/KR0DM+IwdyO5lyGQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('b38e05865272e44156c19da5d5191c83')

#===========[ NOTE SAVER ]=======================
notes = {}

#REQUEST DATA MHS
def carimhs(nmr):
    URLmhs = "http://www.aditmasih.tk/api_andhika/show.php?nmr=" + nmr
    r = requests.get(URLmhs)
    data = r.json()
    err = "data tidak ditemukan"
    
    flag = data['flag']
    if(flag == "1"):
        nmr = data['data_angkatan'][0]['nmr']
        sangar = data['data_angkatan'][0]['sangar']
    
        # munculin semua, ga rapi, ada 'u' nya
        # all_data = data['data_angkatan'][0]
        data= "Kesangaran ke-"+nmr+"\n"+sangar
        return data
        # return all_data

    elif(flag == "0"):
        return err

#INPUT DATA MHS
def inputmhs(nmr, sangar):
    r = requests.post("http://www.aditmasih.tk/api_andhika/insert.php", data={'nmr': nmr, 'sangar': sangar})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

def allmhs():
    r = requests.post("http://www.aditmasih.tk/api_andhika/all.php")
    data = r.json()
    flag = data['flag']
    if(flag == "1"):
        hasil = ""
        for i in range(0,len(data['data_angkatan'])):
            nmr = data['data_angkatan'][int(i)][0]
            sangar = data['data_angkatan'][int(i)][2]
            hasil=hasil+str(i+1)
            hasil=hasil+".\nKesangaran ke "
            hasil=hasil+nmr
            hasil=hasil+"\n"
            hasil=hasil+sangar
            hasil=hasil+"\n"
        return hasil

def bingung(x):
    return x[::-1]

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Halo bro salam kenal, wes siap tak spam?...' + event.source.type))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    teks = event.message.text
    text = teks.lower().strip()
    data=text.split('-')
    data2=text.split(' ')
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)

#MENAMPILKAN MENU
    #tiap ngetik ng grup opo room isok munculo terjemahan boso jowo\n\nawakmu bebas isok ngetik keyword nggawe huruf gede opo cilik"  
    menu1="'/spam-[kalimat]-[jumlah spam]' gawe nyepam wong sing mbok sayang"  
    menu2="'/spamkata [kalimat]' gawe nyepam tiap kata sebanyak kalimat sing diketik" 
    menu3="'/bye' gawe ngetokno bot teko grup opo room"
    menu4="'/rev-[kalimat]' gawe ngewalik tulisan"
    menu5="awali pertanyaan dengan kata 'apa' / 'opo' / 'apakah'"
    menu6="/jodoh-[namamu]-[nama pasangannmu] gawe ndelok prediksi hubunganmu, tapi ojok dipercoyo"
    menu7="'/spamsticker-[package_id]-[sticker_id]-[jumlah spam]' gawe nyepam sticker. list sticker isok didelok ng link iki https://developers.line.me/media/messaging-api/sticker_list.pdf"
    if text=="/spam":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu1))
    if text=="/spamkata":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu2))
    if text=="/bye":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu3))
    if text=="/rev":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu4))
    if text=="/ask":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu5))
    if text=="/jodoh":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu6))
    if text=="/spamsticker":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu7))
#MENU SANGAR
    elif(data[0]=='/sangar'):
        pro = "Wong suroboyo terkenal karo kesangarane. Sak piro sangarmu cak?\n1. lihat-[id]\n2. tambah-[id]-[kesangaran]\n3. hapus-[id]\n4. ganti-[id lama]-[id baru]-[kesangaran baru]\n5. kabeh"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=pro))

#SUB MENU SANGAR
    if(data[0]=='lihat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=carimhs(data[1])))
    elif(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputmhs(data[1],data[2])))
    #elif(data[0]=='hapus'):
     #   line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hapusmhs(data[1])))
    #elif(data[0]=='ganti'):
     #   line_bot_api.reply_message(event.reply_token, TextSendMessage(text=updatemhs(data[1],data[2],data[3],data[4])))
    #elif(data[0]=='kabeh'):
     #   line_bot_api.reply_message(event.reply_token, TextSendMessage(text=allsmhs()))

#SPAM
    elif (data[0]=='/spam'):
        i = 0
        if(int(data[2])>1000):
            if isinstance(event.source, SourceGroup):
                line_bot_api.push_message(event.source.group_id,TextSendMessage(text="kakean woi, nggarakno server lemot ae"))
            elif isinstance(event.source, SourceRoom):
                line_bot_api.push_message(event.source.room_id,TextSendMessage(text="kakean woi, nggarakno server lemot ae"))
        else:
            while i < int(data[2]):
                if isinstance(event.source, SourceGroup):
                    line_bot_api.push_message(event.source.group_id,TextSendMessage(text=data[1]))
                elif isinstance(event.source, SourceRoom):
                    line_bot_api.push_message(event.source.room_id,TextSendMessage(text=data[1]))
                else:
                   line_bot_api.push_message(event.source.user_id,TextSendMessage(text=data[1]))
                i =i+1

#SPAM
    elif (data[0]=='/spamsticker'):
        i = 0
        event.message.package_id=data[1]
        event.message.sticker_id=data[2]
        if(int(data[3])>1000):
            if isinstance(event.source, SourceGroup):
                line_bot_api.push_message(event.source.group_id,StickerSendMessage(package_id=event.message.package_id,sticker_id=event.message.sticker_id))
            elif isinstance(event.source, SourceRoom):
                line_bot_api.push_message(event.source.room_id,StickerSendMessage(package_id=event.message.package_id,sticker_id=event.message.sticker_id))
        else:
            while i < int(data[3]):
                if isinstance(event.source, SourceGroup):
                    line_bot_api.push_message(event.source.group_id,StickerSendMessage(package_id=event.message.package_id,sticker_id=event.message.sticker_id))
                elif isinstance(event.source, SourceRoom):
                    line_bot_api.push_message(event.source.room_id,StickerSendMessage(package_id=event.message.package_id,sticker_id=event.message.sticker_id))
                else:
                   line_bot_api.push_message(event.source.user_id,StickerSendMessage(package_id=event.message.package_id,sticker_id=event.message.sticker_id))
                i =i+1

    elif(data[0]=='/jodoh'):
        a=random.randint(1,100)
        wes="tingkat hubungan kalian "+str(a)
        if a<=20:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wes+"%\nkalian berdua cocok dadi musuh"))
        elif a<=35:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wes+"%\nwoy "+data[1]+", koyoke cintamu bertepuk sebelah tangan"))
        elif a<=50:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wes+"%\nwes ketok "+data[2]+" gaonok rasa nang awakmu"))
        elif a<=65:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wes+"%\nlanjutno usahamu gawe ngejar dee, ojok nyerah"))
        elif a<=80:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wes+"%\nwaduh ternyata "+data[2]+" onok rasa nang awakmu"))
        elif a<=90:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wes+"%\nakeh sing nyenengi "+data[2]+" cepetan ndang ditembak daripada kena tikung"))
        elif a<=100:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=wes+"%\n"+data[1]+" & "+data[2]+" pasangan yang sempurna"))
    
    elif text =="/menu":
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://andhikay24.000webhostapp.com/a.jpg', title='Menu 1', text='Geser kanan', 
                    actions=[
                        PostbackAction(label='/sangar', text='/sangar', data='action=buy&itemid=1'),
                        MessageAction(label='SAK PIRO SANGARMU?',text='/sangar'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://andhikay24.000webhostapp.com/b.jpg', title='Menu 2', text='Penasaran?', 
                    actions=[
                        PostbackAction(label='/spam', text='/spam', data='action=buy&itemid=1'),
                        MessageAction(label='GAWE NYEPAM',text='/spam'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://andhikay24.000webhostapp.com/c.jpg', title='Menu 3', text='Geser terus!', 
                    actions=[
                        PostbackAction(label='/spamkata', text='/spamkata', data='action=buy&itemid=1'),
                        MessageAction(label='POKOKE NYEPAM',text='/spamkata'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://andhikay24.000webhostapp.com/i.jpg', title='Menu 4', text='Geser terus!', 
                    actions=[
                        PostbackAction(label='/spamsticker', text='/spamsticker', data='action=buy&itemid=1'),
                        MessageAction(label='NYEPAM STICKER',text='/spamsticker'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://andhikay24.000webhostapp.com/d.jpg', title='Menu 5', text='Penasaran?', 
                    actions=[
                        PostbackAction(label='/bye', text='/bye', data='action=buy&itemid=1'),
                        MessageAction(label='GAWE LEFT',text='/bye'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://andhikay24.000webhostapp.com/e.jpg', title='Menu 6', text='Akeh kan?', 
                    actions=[
                        PostbackAction(label='/rev', text='/rev', data='action=buy&itemid=1'),
                        MessageAction(label='NGEWALIK TULISAN',text='/rev'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://andhikay24.000webhostapp.com/g.jpg', title='Menu 7', text='Penasaran?', 
                    actions=[
                        PostbackAction(label='/ask', text='/ask', data='action=buy&itemid=1'),
                        MessageAction(label='TANYA BOT',text='/ask'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://andhikay24.000webhostapp.com/h.jpg', title='Menu 8', text='Akeh kan?', 
                    actions=[
                        PostbackAction(label='/jodoh', text='/jodoh', data='action=buy&itemid=1'),
                        MessageAction(label='PREDIKSI PASANGAN',text='/jodoh'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')]),
                CarouselColumn(
                    thumbnail_image_url='https://andhikay24.000webhostapp.com/f.jpg',title='Menu 9',text='Geser kiri',
                    actions=[
                        PostbackAction(label='/dev',text='/dev',data='action=buy&itemid=2'),
                        MessageAction(label='NDELOK PENGEMBANG',text='/dev'),
                        URIAction(label='Add line bot',uri='https://line.me/R/ti/p/%40gne0915s')])
                    ]
                )
            )
        )
    elif text =="/dev":
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://andhikay24.000webhostapp.com/IMG_20180805_103128.jpg',
            title='PENGEMBANG',
            text='Andhika Yoga Perdana, Mahasiswa Informatika ITS',
            actions=[
                PostbackAction(
                    label='Submenu saat ini',
                    text='/menu',
                    data='action=buy&itemid=1'
                ),
                MessageAction(
                    label='Kembali ke menu',
                    text='/menu'
                ),
                URIAction(
                    label='My Personal Website',
                    uri='http://andhikay24.000webhostapp.com/'
                )
            ]
        )
    ))

    #TINGGALKAN GROUP/ROOM
    elif text=="/bye":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Pingin ngekick aku?:(\nketik "/start" gawe ngekick!'))
    elif text=="/start":
        if isinstance(event.source, SourceGroup):
            line_bot_api.push_message(event.source.group_id, TextSendMessage(text='Woy '+profile.display_name+', kurang ajar banget kon wani ngekick aku teko grup iki!'))
            line_bot_api.push_message(event.source.group_id, TextSendMessage(text='Sepurane rek aku tinggal disek, aku bosen ng kene! GAK MENARIK blass cuk'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.push_message(event.source.room_id, TextSendMessage(text='Woy '+profile.display_name+', kurang ajar banget kon wani ngekick aku teko grup iki!'))
            line_bot_api.push_message(event.source.room_id, TextSendMessage(text='Sepurane rek aku tinggal disek, aku bosen ng kene! GAK MENARIK blass cuk'))
            line_bot_api.leave_room(event.source.room_id)
        else: 
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Mending blokiren aku daripada ngekick aku"))
    
#CHAT 1:1
    elif not(isinstance(event.source, SourceGroup) or isinstance(event.source, SourceRoom)):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Hai,' +profile.display_name+'. Bahasa opo iki?\n"'+event.message.text+'"\nKok gak jelas banget'))
    
    #line_bot_api.multicast(['U8d343d76a1c15caad6dba2d2b5dab241'], TextSendMessage(text='Selamat Siang!'))
    elif (data2[0]=='/spamkata'):
        x=1
        while  x <= len(data2):
            if isinstance(event.source, SourceRoom):
                line_bot_api.push_message(event.source.room_id,TextSendMessage(text=data2[x]))
            elif isinstance(event.source, SourceGroup):
                line_bot_api.push_message(event.source.group_id,TextSendMessage(text=data2[x]))
            else:
                line_bot_api.push_message(event.source.user_id,TextSendMessage(text=data2[x]))
            x=x+1 
    
    elif (data[0]=='/rev'):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=bingung(data[1])))
    elif (text=='test' or text=='tes'):
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="masok pak eko"))
    if(data2[0]=='apa' or data2[0]=='apakah' or data2[0]=='opo'):
        a=random.randint(0, 18)
        hasil=["iya", "mungkin", "bisa jadi", "wajib", "terserah", "bebas", "sembarang", "sunnah", "jangan", "sak karepmu", "tanya admin","kakean takok cuk", "apa urusan anda menanyakan hal itu kepada saya","silakan bertanya pada rumput yang bergoyang", "oh yo jelas", "pasti","mboh","lho yo iyo seh","entahlah"]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=hasil[a]))


#kicker.kickoutFromGroup(msg.to,[target])
import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

