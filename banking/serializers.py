from rest_framework import serializers
from django.urls import reverse
from banking.models.customer import Customer

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['url', 'first_name', 'last_name', 'email', 'phone', 'customer_rank', 'links']

    def get_links(self, obj):
        request = self.context['request']
        links = {
            'self': request.build_absolute_uri(obj.get_absolute_url()),
            'accounts': request.build_absolute_uri(reverse('banking:customer/accounts', args=[obj.pk])),
            'loan_applications': request.build_absolute_uri(reverse('banking:customer/loan_applications', args=[obj.pk])),
            'loans': request.build_absolute_uri(reverse('banking:customer/loans', args=[obj.pk])),
        }
        return links