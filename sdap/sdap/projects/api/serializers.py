from rest_framework import serializers
from sdap.projects.models import Project
from sdap.results.models import Results


class ProjectSerializer(serializers.ModelSerializer):
    rel_results = serializers.SerializerMethodField('get_results')
    
    def get_results(self, project):
        results = []
        prj_results = Results.objects.filter(project=project.id)
        for result in prj_results :
            results.append({'title':result.title,'id':result.id})
        return results
    class Meta:
        model = Project
        fields = "__all__"
