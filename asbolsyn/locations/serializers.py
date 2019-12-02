from rest_framework import serializers

from locations.models import Country, Town, Address


class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):
        country = Country(**validated_data)
        country.save()
        return country

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class TownSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    country = CountrySerializer(read_only=True)
    country_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        town = Town(**validated_data)
        town.save()
        return town

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.hint = validated_data.get('hint', instance.hint)
        instance.lat = validated_data.get('lat', instance.lat)
        instance.long = validated_data.get('long', instance.long)
        instance.save()
        return instance
