import vk_api
import random
import scraper
import datetime
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

def tryScrape(date, chatlist, id):
    try:
        return scraper.Scraper(
            "http://www.osu.ru/pages/schedule/?who=1&what=1&filial=1&group="+str(chatlist[id][0])+"&mode=full",
            date)
    except Exception as e:
        print('error', e)

def main():
    vk_session=vk_api.VkApi(token="60f78a53491b23031c9b3defc31584255db9b51c1e3cd5b9cb655abb6e8dd462472f87d2fdc221c7b05d1")
    longpoll = VkBotLongPoll(vk_session, 187255690)
    vk = vk_session.get_api()
    groupList = {"18пинж(ба)рпис": 11852, "18ивт(ба)оп": 11853, "18кб(с)рзпо": 11848, "18иб(б)кзои": 11850, "18ист(ба)оп": 11849, "18мкн(ба)апкм": 11851}
                 #, "18КБ(с)РЗПО": 11848, "18КБ(с)РЗПО": 11848, "18КБ(с)РЗПО": 11848, "18КБ(с)РЗПО": 11848, "18КБ(с)РЗПО": 11848, "18КБ(с)РЗПО": 11848
                 #, "18КБ(с)РЗПО": 11848, "18КБ(с)РЗПО": 11848, "18КБ(с)РЗПО": 11848, "18КБ(с)РЗПО": 11848, "18КБ(с)РЗПО": 11848, "18КБ(с)РЗПО": 11848}
    chatList = dict()
    try:
        for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                    date = ''
                    if "#CONFIGURATION" in event.obj.text:
                        try:
                            groupID = 2000000000 + event.chat_id
                            groupNAME = event.obj.text.strip().lower().split()
                            chatList[event.chat_id] = (groupList[groupNAME[1]], groupID, )
                        except Exception as e:
                            print('error', e)
                            vk.messages.send(
                                # user_id=event.obj.from_id,
                                random_id=random.randint(0, 1024),
                                peer_id=2000000000 + event.chat_id,
                                message="Такая группа не найдена.")
                    if "расп" in event.obj.text.lower():
                        now = datetime.datetime.now()
                        date = str(now.day + 1) + '.' + str(now.month) + '.' + str(now.year)
                        if "сегодня" in event.obj.text.lower():
                            date = str(now.day) + '.' + str(now.month) + '.' + str(now.year)
                            scrape=tryScrape(date, chatList, event.chat_id)
                            #############################################
                        elif "расп" == event.obj.text.lower():
                            date = str(now.day+1) + '.' + str(now.month) + '.' + str(now.year)
                            scrape=tryScrape(date, chatList, event.chat_id)
                            #############################################
                        elif "завтра" in event.obj.text.lower():
                            date = str(now.day+1) + '.' + str(now.month) + '.' + str(now.year)
                            scrape=tryScrape(date, chatList, event.chat_id)
                            #############################################
                        else:
                            tmp=[]
                            tmp=event.obj.text.lower().split(" ")
                            for n in tmp:
                                if not n.isalpha():
                                    date=n
                            scrape=tryScrape(date, chatList, event.chat_id)
                            #############################################
                        try:
                            vk.messages.send(
                                #user_id=event.obj.from_id,
                                random_id=random.randint(0, 1024),
                                peer_id=chatList[event.chat_id][1],
                                message=scrape.scrape())
                        except Exception as e:
                            print('error', e)
    except Exception as e:
        print('error', e)
main()