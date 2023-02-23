from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

keyboard = VkKeyboard(one_time=False, inline=False)
keyboard.add_button("Нажми, чтобы узнать что я умею \N{smiling face with sunglasses}", VkKeyboardColor.PRIMARY)
keyboard.add_button("Начать автоматический поиск", VkKeyboardColor.POSITIVE)
keyboard.add_button("Начать поиск по заданным параметрам", VkKeyboardColor.POSITIVE)
keyboard = keyboard.get_keyboard()

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

keyboard3 = VkKeyboard(one_time=False, inline=True)
keyboard3.add_button(
    label="Удалить историю",
    color=VkKeyboardColor.SECONDARY,
    payload={"type": "text", "text": "Удалить историю"})

keyboard = json.dumps(keyboard, ensure_ascii=False)

