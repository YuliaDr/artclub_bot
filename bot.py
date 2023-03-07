import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from models import User
from msg_attach import get_attachment
from send_message import send_message, start_message
from keyboard import create_keyboard
from VKtoken import get_token
from msg_text import get_text

token = get_token()


def bot_start():
    vk_session = vk_api.VkApi(token=token)
    vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    # keyboard = start_keyboard()
    # send_message(vk_session, '257947680', ')', keyboard=keyboard)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me: # обработка сообщений
                msg = event.text.lower()
                user_id = event.user_id # получаем id пользователя, отправившего сообщение

                # получаем доп информацию о пользователе с помощью методов vkAPI
                user_info = vk_session.method("users.get", {"user_ids": user_id})[0]
                first_name = user_info['first_name']
                last_name = user_info['last_name']

                # добавляем пользователя в бд, если его там нет, иначе получаем объект пользователя
                user, created = User.get_or_create(
                    id=user_id,
                    defaults={'first_name': first_name,
                              "last_name": last_name})
                is_admin = user.is_admin # определение прав пользователя

                # !!! вынести в отдельную функцию и сделать конечный автомат. глобальная переменная state - один из параметров
                if msg == "создать рассылку" and is_admin:
                    keyboard = create_keyboard(msg, is_admin)
                    send_message(vk_session, user_id, get_text(msg), keyboard=keyboard)

                    flag = 0
                    for event in longpoll.listen(): # ждем следуещее сообщение с текстом рассылки
                        if event.type == VkEventType.MESSAGE_NEW:

                            if event.to_me:
                                msg_to_all = event.text # сохраняем исходный текст сообщения для рассылки
                                keyboard = create_keyboard("confirm", is_admin, one_time=True)
                                send_message(vk_session, user_id, "Подтвердите отправку рассылки", keyboard=keyboard)

                                for event in longpoll.listen(): # ждем сообщение с подтверждением рассылки
                                    if event.type == VkEventType.MESSAGE_NEW:
                                        msg = event.text.lower()

                                        if event.to_me:
                                            if msg == 'подтвердить':
                                                print(msg_to_all)
                                                keyboard_admin = create_keyboard('начать', True)
                                                keyboard_user = create_keyboard('начать', False)

                                                # разбиение пользователей на батчи по n с учетом прав доступа
                                                dict = []
                                                user_dict = []
                                                user_adm_dict = []
                                                n = 10

                                                # разбиение простых пользователей
                                                for iter_user in User.select().where(User.is_admin == False):
                                                    dict.append(str(iter_user.id))

                                                for i in range(0, len(dict), n):
                                                    user_dict.append(dict[i:i+n])

                                                dict.clear()
                                                # разбиение админов
                                                for iter_user in User.select().where(User.is_admin == True):
                                                    dict.append(str(iter_user.id))

                                                for i in range(0, len(dict), n):
                                                    user_adm_dict.append(dict[i:i+n])

                                                # рассылка пользователям
                                                for users in user_dict:
                                                    send_message(vk_session, ','.join(users), msg_to_all,
                                                                 keyboard=keyboard_user)

                                                # рассылка админам
                                                for users in user_adm_dict:
                                                    send_message(vk_session, ','.join(users), msg_to_all,
                                                                 keyboard=keyboard_admin)

                                                flag = 1
                                                break

                                            elif msg == 'отменить':
                                                keyboard = create_keyboard('начать', is_admin)
                                                send_message(vk_session, user_id, "Рассылка отменена",
                                                             keyboard=keyboard)
                                                flag = 1
                                                break

                                if flag == 1:
                                    break

                else:
                    # if send_to_all and is_admin:
                    #     send_to_all = False
                    #     msg_to_all = event.text
                    #     keyboard = create_keyboard("confirm", is_admin, one_time=True)
                    #     send_message(vk_session, user_id, "Подтвердите отправку рассылки", keyboard=keyboard)
                    #
                    # elif msg_to_all != '' and is_admin:
                    #     if msg == 'подтвердить':
                    #         print(msg_to_all)
                    #         keyboard_admin = create_keyboard('начать', True)
                    #         keyboard_user = create_keyboard('начать', False)
                    #         for iter_user in User.select():
                    #             if iter_user.is_admin:
                    #                 send_message(vk_session, iter_user.id, msg_to_all, keyboard=keyboard_admin)
                    #             else:
                    #                 send_message(vk_session, iter_user.id, msg_to_all, keyboard=keyboard_user)
                    #
                    #
                    #     elif msg == 'отменить':
                    #         keyboard = create_keyboard('начать', is_admin)
                    #         send_message(vk_session, user_id, "Рассылка отменена", keyboard=keyboard)

                    # else:
                    answ_msg = get_text(msg) # ответ на сообщение msg
                    if answ_msg is not None:
                        send_message(vk_session, user_id, answ_msg, attachment=get_attachment(msg))
                    else: # начальное сообщение
                        keyboard = create_keyboard('начать', is_admin)
                        start_message(vk_session, user_id, keyboard=keyboard)


