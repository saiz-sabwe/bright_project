from rest_framework import serializers
from .models import Agent, Presence

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class PresenceSerializer(serializers.ModelSerializer):
    agent = AgentSerializer()  # nested pour avoir nom/prenom

    class Meta:
        model = Presence
        fields = '__all__'

    def get_photo(self, obj):
        request = self.context.get('request')
        if obj.photo and hasattr(obj.photo, 'url'):
            return request.build_absolute_uri(obj.photo.url) if request else obj.photo.url
        return None