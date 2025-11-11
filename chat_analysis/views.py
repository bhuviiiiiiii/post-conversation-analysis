from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, ConversationAnalysis
from .serializers import ConversationSerializer, ConversationAnalysisSerializer
from .services import ConversationAnalyzer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        messages = request.data.get('messages', [])
        serializer = self.get_serializer(data=request.data, context={'messages': messages})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Trigger analysis
        analyzer = ConversationAnalyzer()
        analysis = analyzer.analyze_conversation(serializer.instance)
        
        if analysis:
            analysis_serializer = ConversationAnalysisSerializer(analysis)
            return Response({
                'conversation': serializer.data,
                'analysis': analysis_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        conversation = self.get_object()
        analyzer = ConversationAnalyzer()
        analysis = analyzer.analyze_conversation(conversation)
        
        if analysis:
            serializer = ConversationAnalysisSerializer(analysis)
            return Response(serializer.data)
        return Response(
            {'error': 'Could not analyze conversation'},
            status=status.HTTP_400_BAD_REQUEST
        )

class AnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ConversationAnalysis.objects.all()
    serializer_class = ConversationAnalysisSerializer
