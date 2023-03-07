from vk_api.keyboard import VkKeyboard, VkKeyboardColor


# def start_keyboard():
#     keyboard = VkKeyboard()
#     keyboard.add_button("Начать", color=VkKeyboardColor.POSITIVE)
#     keyboard = keyboard.get_keyboard()
#     return keyboard


def create_keyboard(msg, is_admin, one_time=False):
    keyboard = VkKeyboard(one_time=one_time)

    if msg == "начать" and is_admin is False:
        keyboard.add_button('Что такое ЦКИ?', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Как вас найти?', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()

        keyboard.add_button('Чем занимается Art Club BMSTU?', color=VkKeyboardColor.SECONDARY)

        keyboard.add_line()

        keyboard.add_button('Что такое Art Club Academy?', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()

        keyboard.add_button('Расскажи о коллективах ЦКИ', color=VkKeyboardColor.SECONDARY)

    elif msg == "начать" and is_admin:
        keyboard.add_button('Что такое ЦКИ?', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Как вас найти?', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()

        keyboard.add_button('Чем занимается Art Club BMSTU?', color=VkKeyboardColor.SECONDARY)

        keyboard.add_line()

        keyboard.add_button('Что такое Art Club Academy?', color=VkKeyboardColor.PRIMARY)

        keyboard.add_line()

        keyboard.add_button('Расскажи о коллективах ЦКИ', color=VkKeyboardColor.SECONDARY)

        keyboard.add_line()
        keyboard.add_button("Создать рассылку", color=VkKeyboardColor.POSITIVE)

    elif msg == "confirm" and is_admin:
        keyboard.add_button("Подтвердить", color=VkKeyboardColor.POSITIVE)
        keyboard.add_button("Отменить", color=VkKeyboardColor.NEGATIVE)

    elif msg == "создать рассылку":
        return keyboard.get_empty_keyboard()

    keyboard = keyboard.get_keyboard()
    return keyboard
