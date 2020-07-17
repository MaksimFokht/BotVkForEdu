import bot_config
import vk_api

vk_session = vk_api.VkApi(token=bot_config.token)
vk = vk_session.get_api()
