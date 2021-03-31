from config import group_id, api_token
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from urls import Urls
from stankin_classes_alias import Classes
import time
import sports_url
 
class Bot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = VkApi(token=token)
        self.api = self.vk.get_api()
        self.long_poller = VkBotLongPoll(self.vk, group_id=self.group_id)
        self.time_stamp = time.time()

    def _send(self, url, event):
        try:
            self.api.messages.send(message="ща скину...",
                                   random_id=event.object.random_id,
                                   peer_id=event.object.peer_id)
            self.api.messages.send(message=url,
                                   random_id=event.object.random_id,
                                   peer_id=event.object.peer_id)
        except Exception:
            self.api.messages.send(message="чёт ссылку не нашел...",
                                   random_id=event.object.random_id,
                                   peer_id=event.object.peer_id)

    def _update_sports_url(self):
        if (time.time() - self.time_stamp) / 1800 >= 1:
            Urls.sports_url = sports_url.get_url()
            print(f"sports link had been updated: {Urls.sports_url.value}")
            

    def send_sports_url(self, event):
        self._send(Urls.sports_url, event)

    def send_physics_url(self, event):
        self._send(Urls.physics_url, event)

    def send_probability_theory_url(self, event):
        self._send(Urls.probability_theory_url, event)

    def send_oop_url(self, event):
        self._send(Urls.oop_url, event)

    def send_elteh_url(self, event):
        self._send(Urls.elteh_url, event)

    def send_calc_math_url(self, event):
        self._send(Urls.calc_math_url, event)
        
    def send_hmi_url(self, event):
        self._send(Urls.hmi_url, event)
        
    def send_mo_url(self, event):
        self._send(Urls.mo_url, event)

    def _on_event(self, event):
        cmd = event.object.text.lower()
        if event.type == VkBotEventType.MESSAGE_NEW:
            if Classes.sports.value in cmd:
                self.send_sports_url(event)
            if Classes.physics.value in cmd:
                self.send_physics_url(event)
            if Classes.probability_theory.value in cmd:
                self.send_probability_theory_url(event)
            if Classes.elteh.value in cmd:
                self.send_elteh_url(event)
            if Classes.oop.value in cmd:
                self.send_oop_url(event)
            if Classes.calc_math.value in cmd:
                self.send_calc_math_url(event)
            if Classes.hmi.value in cmd:
                self.send_hmi_url(event)
            if Classes.mo.value in cmd:
                self.send_mo_url(event)
        else:
            print(f'can not proceed {event.type}')

    def run(self):
        try:
            for event in self.long_poller.listen():
                try:
                    self._update_sports_url()
                    self._on_event(event)
                except Exception as err:
                    print(err)
        except Exception as err:
            print(err)
            print(self.long_poller.listen())


if __name__ == '__main__':
    bot = Bot(group_id, api_token)
    bot.run()
