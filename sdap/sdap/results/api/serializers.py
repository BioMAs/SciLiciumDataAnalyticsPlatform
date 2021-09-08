from rest_framework import serializers
from sdap.results.models import Results

from sdap.projects.api.serializers import ProjectSerializer

class ResultSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(many=False, read_only=True)
    class Meta:
        model = Results
        fields = "__all__"
