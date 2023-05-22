from ..typing import JsonType


class ServerJsonAdapter:

    @classmethod
    def adapt(cls, obj: object | list[object]) -> JsonType:

        if cls._object_is_list(obj):

            result = cls._adapt_list_of_objects(obj)

        elif cls._object_has_attributes(obj):

            result = cls._adapt_object_with_attributes(obj)

        else:

            result = obj

        return result

    @staticmethod
    def _object_is_list(obj: object) -> bool:

        return isinstance(obj, list)

    @staticmethod
    def _object_has_attributes(obj: object) -> bool:

        return hasattr(obj, '__dict__')

    @classmethod
    def _adapt_list_of_objects(cls, objects: list[object]) -> JsonType:

        result = []

        for obj in objects:

            result.append(cls.adapt(obj))

        return result

    @classmethod
    def _adapt_object_with_attributes(cls, obj: object) -> JsonType:

        result = {}

        for attribute, value in obj.__dict__.items():

            result[cls._snake_case_to_lower_camel_case(attribute)] = value

        return result

    @classmethod
    def _snake_case_to_lower_camel_case(cls, snake_case_string: str) -> str:

        camel_case_string = cls._snake_case_to_camel_case(snake_case_string)

        return snake_case_string[0].lower() + camel_case_string[1:]

    @staticmethod
    def _snake_case_to_camel_case(snake_case_string: str) -> str:

        return ''.join(x.capitalize() for x in snake_case_string.lower().split('_'))
