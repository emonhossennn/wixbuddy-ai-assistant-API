from django.apps import AppConfig

class WixbuddyConfig(AppConfig):
    name = 'wixbuddy'

    def ready(self):
        import wixbuddy.signals 