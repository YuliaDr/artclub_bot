from vk_api.utils import get_random_id


def start_message(session, id, keyboard=None):
    session.method("messages.send", {"user_id": id, "message": "Привет, меня зовут ArtBot! \nЧто ты хочешь узнать?",
                                     "random_id": get_random_id(), "keyboard": keyboard})


def send_message(session, id, text, keyboard=None, attachment=None):
    session.method("messages.send", {"user_ids": id, "message": text, "random_id": get_random_id(),
                                     "attachment": attachment, "keyboard": keyboard})


# def send_keyboard(session, id):
#     with open("keyboard_test.json", "r") as keyboard:
#         keyboard = json.load(keyboard)
#         keyboard = json.dumps(keyboard)
#         session.method("messages.send",
#         {"user_id": id, "message": "Выбери действие", "keyboard": keyboard, "random_id": random.randint(1, 1000)})

