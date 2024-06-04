from rest_framework import serializers
from core.models import Recipe, Tag, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes',
                  'price', 'link', 'tags', 'ingredients')
        read_only_fields = ('id',)

    def _get_or_create_tag(self, tags, recipe):
        """Handle getting and creating tags as needed."""
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=self.context['request'].user, **tag,)
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredient(self, ingredients, recipe):
        """Handle getting and creating ingredients as needed."""
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=self.context['request'].user, **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tag(tags, recipe)
        self._get_or_create_ingredient(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.ingredients.clear()
        self._get_or_create_tag(tags, instance)
        self._get_or_create_ingredient(ingredients, instance)
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail."""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description', 'image',)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipe."""

    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
        extra_kwargs = {'image': {'required': True}}
