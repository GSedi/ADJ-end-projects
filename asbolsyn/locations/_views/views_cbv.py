from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from locations.models import Town, Address
from locations.serializers import TownSerializer, AddressSerializer


class TownListAPIView(APIView):
    def get(self, request):
        towns = Town.objects.all()
        serializer = TownSerializer(towns, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TownSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TownDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Town.objects.get(id=pk)
        except Town.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        town = self.get_object(pk)
        serializer = TownSerializer(town)
        return Response(serializer.data)

    def put(self, request, pk):
        town = self.get_object(pk)
        serializer = TownSerializer(instance=town, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        town = self.get_object(pk)
        town.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddressListAPIView(APIView):
    def get(self, request):
        towns = Address.objects.all()
        serializer = AddressSerializer(towns, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddressDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Address.objects.get(id=pk)
        except Address.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        address = self.get_object(pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    def put(self, request, pk):
        address = self.get_object(pk)
        serializer = AddressSerializer(instance=address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        address = self.get_object(pk)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)