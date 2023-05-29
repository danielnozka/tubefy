class DatabaseQueryException(Exception):

    def __init__(self, exception: Exception):

        super().__init__(f'{exception.__class__.__name__} - {str(exception)}')
