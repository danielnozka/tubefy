import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from .configuration.app_settings import AppSettings


class ModuleInitializer(DeclarativeContainer):

    _root_path = os.path.dirname(os.path.abspath(__file__))

    app_settings = Singleton(AppSettings,
                             root_path=_root_path,
                             settings_file=os.path.join(_root_path, 'app_settings.json'))
