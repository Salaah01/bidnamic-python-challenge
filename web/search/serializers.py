from rest_framework.serializers import ModelSerializer
from . import models as search_models


class SearchTermSerializer(ModelSerializer):
    class Meta:
        model = search_models.SearchTerm
        fields = '__all__'
        depth = 3
