from pathlib import Path
from types import ModuleType
from . import adapters, communications, controllers, persistence, services, use_cases


APP_COMPONENTS: list[ModuleType] = [adapters, communications, controllers, persistence, services, use_cases]
APP_ROOT_PATH: Path = Path(__file__).parent
