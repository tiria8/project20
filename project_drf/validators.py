from rest_framework import serializers


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'youtube.com' not in str(value):
            raise serializers.ValidationError('Ссылка может быть только на материалы с YouTube')



