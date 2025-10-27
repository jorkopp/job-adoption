from messaging.secrets import Secrets
from twilio.rest import Client
import time

class Messenger:
    CLIENT = Client(Secrets.TWILIO_SID, Secrets.TWILIO_AUTH)

    @staticmethod
    def send_notifications(adoptable_dogs):
        for adoptable_dog in adoptable_dogs:
            Messenger.send_notification(adoptable_dog)
            time.sleep(1)

    @staticmethod
    def send_notification(adoptable_dog):
        body = f"New dog match at {adoptable_dog.shelter}!\nName: {adoptable_dog.name}\nBreed: {adoptable_dog.breed}\nLink: {adoptable_dog.url}"
        try:
            kwargs = {"body": body, "from_": Secrets.TWILIO_FROM, "to": Secrets.MY_PHONE}
            if adoptable_dog.image:
                # include image as MMS media. Twilio accepts a list of URLs.
                kwargs["media_url"] = [adoptable_dog.image]
            Messenger.CLIENT.messages.create(**kwargs)
        except Exception:
            pass