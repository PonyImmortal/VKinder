from vk_api.keyboard import VkKeyboard, VkKeyboardColor

main_keyboard = VkKeyboard(one_time=False, inline=False)
main_keyboard.add_button("Нажми, чтобы узнать что я умею \N{smiling face with sunglasses}", color=VkKeyboardColor.PRIMARY)
main_keyboard.add_button("Начать автоматический поиск", color=VkKeyboardColor.POSITIVE)
main_keyboard.add_button("Начать поиск по заданным параметрам", color=VkKeyboardColor.POSITIVE)

keyboard1 = VkKeyboard(one_time=False, inline=True)
keyboard1.add_button(label="Еще варианты", color=VkKeyboardColor.SECONDARY, payload={"type": "text", "text": "Еще варианты"})

keyboard2 = VkKeyboard(one_time=False, inline=True)
keyboard2.add_button(label="Закончить просмотр", color=VkKeyboardColor.SECONDARY, payload={"type": "text", "text": "Закончить просмотр"})

keyboard3 = VkKeyboard(one_time=False, inline=True)
keyboard3.add_button(label="Удалить историю", color=VkKeyboardColor.SECONDARY, payload={"type": "text", "text": "Удалить историю"})

main_keyboard = main_keyboard.get_keyboard()
keyboard1 = keyboard1.get_keyboard()
keyboard2 = keyboard2.get_keyboard()
keyboard3 = keyboard3.get_keyboard()

