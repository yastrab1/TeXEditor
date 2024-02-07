import keyboard

from Config.Config import Config


class KeyRemap:
    def __init__(self):
        self.blockedKeys = set()

    def start(self):
        key_mappings = Config().get("KeyRemapping")


        blocked_keys = set()

        def on_key_event(e):
            if e.event_type == keyboard.KEY_DOWN:
                source_key = e.name.lower()

                if source_key in key_mappings:
                    destination_key = key_mappings[source_key]

                    if destination_key not in blocked_keys:
                        blocked_keys.add(destination_key)
                        keyboard.press_and_release(destination_key)
                        blocked_keys.remove(destination_key)

        keyboard.hook(on_key_event)
