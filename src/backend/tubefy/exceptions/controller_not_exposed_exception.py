class ControllerNotExposedException(Exception):

    def __init__(self, controller_name: str):
        
        super().__init__(f'Controller {controller_name} was not exposed properly')
