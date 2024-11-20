from ninja import Schema


class ResponseItem[T](Schema):
    value: T
