from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import json


def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}",
    }


keyboard = {
    "one_time": False,
    "inline": False,
    "buttons": [
        [get_button('Нажми, чтобы узнать что я умею \N{smiling face with sunglasses}', 'primary')],
        [get_button('Начать автоматический поиск', 'positive', )],
        [get_button('Начать поиск по заданным параметрам', 'positive')],
    ]
}

keyboard1 = VkKeyboard(one_time=False, inline=True)
keyboard1.add_button(
    label="Еще варианты",
    color=VkKeyboardColor.SECONDARY,
    payload={"type": "text", "text": "Еще варианты"},
)

keyboard2 = VkKeyboard(one_time=False, inline=True)
keyboard2.add_button(
    label="Закончить просмотр",
    color=VkKeyboardColor.SECONDARY,
    payload={"type": "text", "text": "Закончить просмотр"})

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
