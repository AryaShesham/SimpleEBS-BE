import factory
from django.contrib.auth.models import User
from users.customer.models import Customer
from users.event_organiser.models import EventOrganiser


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating User instances.

    This factory generates User instances with unique usernames and a predefined password.
    """

    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")


class CustomerFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Customer instances.

    This factory generates Customer instances associated with User instances created using the UserFactory.
    """

    class Meta:
        model = Customer

    user = factory.SubFactory(UserFactory)


class EventOrganiserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating EventOrganiser instances.

    This factory generates EventOrganiser instances associated with User instances created using the UserFactory.
    """

    class Meta:
        model = EventOrganiser

    user = factory.SubFactory(UserFactory)
