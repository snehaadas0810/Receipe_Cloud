from rest_framework import serializers
from .models import Post, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'media', 'media_type', 'description', 'ingredients']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        user = self.context['request'].user

        post = Post.objects.create(user=user, **validated_data)

        for item in ingredients_data:
            Ingredient.objects.create(post=post, **item)

        return post