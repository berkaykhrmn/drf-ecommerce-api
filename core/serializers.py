from rest_framework import serializers

class EmptySerializer(serializers.Serializer):
    pass

class APIRootSerializer(serializers.Serializer):
    products = serializers.CharField()
    categories = serializers.CharField()
    comments = serializers.CharField()
    cart = serializers.DictField()
    orders = serializers.DictField()
    user = serializers.DictField()