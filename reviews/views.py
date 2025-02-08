from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Review, Response as ReviewResponse
from .serializers import ReviewSerializer, CreateResponseSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Permite: listar, criar, recuperar, atualizar e deletar avaliações.
    """
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # A criação já é tratada no serializer (definindo usuário e validando o tipo de usuário).
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def respond(self, request, pk=None):
        """
        Endpoint para que uma empresa responda a uma avaliação.
        URL: /reviews/{id}/respond/
        """
        review = self.get_object()

        # Apenas empresas podem responder, e somente às avaliações que pertencem à sua conta.
        if not request.user.is_company:
            return Response({"detail": "Apenas empresas podem responder avaliações."},
                            status=status.HTTP_403_FORBIDDEN)

        if review.company != request.user:
            return Response({"detail": "Você não pode responder avaliações de outra empresa."},
                            status=status.HTTP_403_FORBIDDEN)

        # Verifica se a avaliação já possui resposta (já que usamos OneToOneField)
        #if hasattr(review, 'response'):
        #    return Response({"detail": "Essa avaliação já possui uma resposta."},
        #                    status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateResponseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
