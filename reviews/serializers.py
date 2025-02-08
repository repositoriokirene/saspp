from rest_framework import serializers
from .models import Review, Response, Account

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'message', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    response = ResponseSerializer(read_only=True, many=True)
    user = serializers.StringRelatedField(read_only=True)
    company = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'company', 'stars', 'title', 'description', 'created_at', 'response']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user

        if request.user.is_company:
            raise serializers.ValidationError("Empresas não podem criar avaliações.")

        company_id = self.context['request'].data.get('company_id')
        if not company_id:
            raise serializers.ValidationError("É necessário informar a empresa a ser avaliada.")
        
        try:
            company = Account.objects.get(id=company_id, is_company=True)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Empresa inválida.")
        validated_data['company'] = company

        return super().create(validated_data)

class CreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'review', 'message']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request.user.is_company:
            raise serializers.ValidationError("Apenas empresas podem responder avaliações.")
        validated_data['company'] = request.user
        return super().create(validated_data)
