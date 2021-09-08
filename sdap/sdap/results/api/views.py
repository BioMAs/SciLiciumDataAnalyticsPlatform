from rest_framework import viewsets, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from sdap.results.models import Results
from sdap.results.api.serializers import ResultSerializer


class ResultViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
        Additionally we also provide an extra `public` action to allow anyone to acces to public studies.
    """
    serializer_class = ResultSerializer
    queryset = Results.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)
    
    @action(detail=False,url_path='last', url_name='last')
    def last(self, request, *args, **kwargs): 
        last = self.queryset.filter(created_by=self.request.user).order_by('-id')[:5]
        serializer = ResultSerializer(last, many=True)
        return Response(serializer.data)
