from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    createdAt = serializers.DateTimeField(read_only=True, source='created_at')
    updatedAt = serializers.DateTimeField(read_only=True, source='updated_at')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    color = serializers.CharField(max_length=20, required=False)
    createdAt = serializers.DateTimeField(read_only=True, source='created_at')


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    color = serializers.CharField(max_length=20, required=False)
    createdAt = serializers.DateTimeField(read_only=True, source='created_at')


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=500)
    description = serializers.CharField(required=False, allow_null=True)
    priority = serializers.ChoiceField(choices=['HIGH', 'MEDIUM', 'LOW'], default='MEDIUM')
    dueDate = serializers.DateTimeField(required=False, allow_null=True, source='due_date')
    completed = serializers.BooleanField(default=False)
    completedAt = serializers.DateTimeField(required=False, allow_null=True, source='completed_at')
    createdAt = serializers.DateTimeField(read_only=True, source='created_at')
    updatedAt = serializers.DateTimeField(read_only=True, source='updated_at')
    categoryId = serializers.IntegerField(required=False, allow_null=True, source='category_id')
    category = CategorySerializer(read_only=True, required=False)
    tags = TagSerializer(many=True, read_only=True, required=False)
    tagIds = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        source='tag_ids'
    )
