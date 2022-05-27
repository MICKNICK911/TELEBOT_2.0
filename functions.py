import config
import random
from database import db as session
import models
from telebot import types


def familiar(point, table: [], fam_state: []):
    statement = session.query(models.Users).all()
    box = []
    for u in statement:
        box.append(u.__dict__)

    if box:
        for itm in box:
            if itm['chat_id'] == point:
                print('success')
                table.clear()
                table.append(itm['chat_id'])

                fam_state.clear()
                fam_state.append(1)

                requesting = session.query(models.Users).filter(models.Users.chat_id == point).first()
                requesting.trust = itm['trust'] = int(itm['trust']) + 1
                session.commit()

                requested = session.query(models.Users).filter(models.Users.chat_id == point).first()
                mox = [requested.__dict__]
                break
    else:
        new_posts = models.Users(chat_id=config.my_chat_id, trust=1)
        session.add(new_posts)
        session.commit()
        session.refresh(new_posts)

    if not fam_state:
        new_posts = models.Users(chat_id=point, trust=1)
        session.add(new_posts)
        session.commit()
        session.refresh(new_posts)


def confirm(label, chatID, bot):
    mark = types.ReplyKeyboardMarkup(row_width=1)
    bta = types.KeyboardButton("YES")
    btb = types.KeyboardButton("NO")
    mark.add(bta, btb)
    bot.send_message(chat_id=chatID,
                     text=label,
                     parse_mode='markdown', reply_markup=mark)


def cancel(label, chatID, bot):
    marks = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id=chatID, text=label,
                     parse_mode="markdown", reply_markup=marks)


def invalid(label, chatID, bot, say):
    bot.send_sticker(chat_id=chatID,
                     data="CAACAgIAAxkBAAPrYZgpuCc1LHLrxcN4T5mBMzKjXIQAAggNAAKmPTlIx6LTQyGewQciBA")
    bot.reply_to(say, label, parse_mode="markdown")


def ask(no_idea, source):
    requesting = session.query(models.Memory).filter(models.Memory.reply == no_idea).all()
    box = []
    for u in requesting:
        box.append(u.__dict__)

    def opt():
        co = 0
        for items in box:
            co += 1
            requested = session.query(models.Memory).filter(models.Memory.listen == items['listen'],
                                                            models.Memory.Author == source).all()
            box1 = []
            for ui in requested:
                box1.append(ui.__dict__)

            if box1:
                for itm in box1:
                    if itm['reply'] != 'no idea':
                        if items in box:
                            num = box.index(items)

                            box.remove(box[num])

    for tins in range(len(box)):
        opt()
    return box


def store(asking: [], identifying: [], reply, listen: [], author, try_correct: [], try_listen: [], try_reply: [],
          keyword: [],
          key_reply: []):
    try:
        if asking:
            if identifying[0] == author:
                requesting = session.query(models.Memory).filter(models.Memory.listen == asking[0]).first()
                requesting.reply = reply
                session.commit()
            else:
                new_posts = models.Memory(reply=reply, listen=listen[0], Author=author)
                session.add(new_posts)
                session.commit()
                session.refresh(new_posts)

            asking.clear()
            identifying.clear()

        elif try_correct:
            new_posts = models.Memory(reply=try_listen[0], listen=try_reply[0], Author=author)
            session.add(new_posts)
            session.commit()
            session.refresh(new_posts)

            try_correct.clear()
            try_listen.clear()
            try_reply.clear()

        else:
            new_posts = models.Memory(reply=key_reply[0], listen=keyword[0], Author=author)
            session.add(new_posts)
            session.commit()
            session.refresh(new_posts)

        return

    except:
        pass


def public(label, point):
    post = session.query(models.Memory).filter(models.Memory.reply == label, models.Memory.listen == point).all()

    box = []
    for row in post:
        box.append(row.__dict__)

    if len(box) >= 3:
        for items in box:
            requesting = session.query(models.Memory).filter(models.Memory.id == items['id']).first()
            requesting.published = True
            session.commit()


def think(no_idea: [], try_idea: [], chatID, point):
    if no_idea:
        post = session.query(models.Memory).filter(models.Memory.published == 'true').all()

        no_idea.clear()

    elif try_idea:
        post = session.query(models.Memory).filter(models.Memory.published == 'false').all()

        try_idea.clear()

    else:
        post = session.query(models.Memory).filter(models.Memory.Author == chatID).all()

    box = []
    for row in post:
        box.append(row.__dict__)

    for itm in box:
        single = itm['listen'].split(" or ")
        for tins in single:
            if point == tins:
                grab = itm['listen']
                post = session.query(models.Memory).filter(models.Memory.listen == grab).all()

                box1 = []
                for row in post:
                    box1.append(row.__dict__)

                if len(box1) > 1:
                    ans = []
                    for item in box1:
                        ans.append(item['reply'])

                    final_output = random.choice(ans)
                    final = final_output.split(" or ")
                    final_say = random.choice(final)

                else:
                    final = box1[0]['reply'].split(" or ")
                    final_say = random.choice(final)
                try:
                    public(final_say, point)
                except:
                    pass

                return final_say


def keep(reply, listen, Author):
    new_posts = models.Memory(reply=reply, listen=listen, Author=Author)
    session.add(new_posts)
    session.commit()
    session.refresh(new_posts)


def delete_excess(grab, source):
    post = session.query(models.Memory).filter(models.Memory.listen == grab, models.Memory.Author == source).all()

    box1 = []
    for row in post:
        box1.append(row.__dict__)

    post1 = session.query(models.Memory).filter(models.Memory.listen == grab).all()

    box = []
    for row in post1:
        box.append(row.__dict__)

    prof = []
    guarantee = []
    sieve = []
    bases = []
    for items in box1:
        prof.append(items['listen'])
        for itm in box:
            if itm['listen'] == prof[0]:
                if itm['reply'] in sieve and itm['reply'] not in bases:
                    bases.append(itm['reply'])
                if itm['reply'] in sieve:
                    sieve.insert(int(sieve.index(itm['reply'])), itm['reply'])
                else:
                    sieve.append(itm['reply'])
        for tin in bases:
            num = sieve.count(tin)
            if num >= 3:
                guarantee.append(tin)
        prof.clear()
        sieve.clear()
        bases.clear()
    if guarantee:
        post = session.query(models.Memory).filter(models.Memory.listen == grab, models.Memory.Author == source).delete(
            synchronize_session=False)
        session.commit()
