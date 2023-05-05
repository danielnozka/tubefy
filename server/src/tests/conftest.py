from youtube_music_manager_server.module_initializer import ModuleInitializer


module_initializer = ModuleInitializer()
module_initializer.wire(modules=['.unit.conftest'])
