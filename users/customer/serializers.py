from rest_framework.serializers import ModelSerializer
from users.customer.models import Customer
from users.serliazers import UserSerializer


class CustomerSerializers(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"
