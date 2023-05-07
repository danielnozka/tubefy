import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from .configuration.app_settings import AppSettings


root_path = os.path.dirname(os.path.abspath(__file__))


class ModuleInitializer(DeclarativeContainer):

    app_settings = Singleton(AppSettings,
                             root_path=root_path,
                             settings_file=os.path.join(root_path, 'app_settings.json'))
