from rest_framework import serializers

from ..entity import Category


class NullIntField(serializers.IntegerField):
    def to_internal_value(self, data):
        if data in ("", None, "null"):
            return None
        return super().to_internal_value(data)


class CategoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    icon = serializers.CharField(max_length=255, required=False, allow_blank=True, default="")
    parent_id = NullIntField(required=False, allow_null=True)
    status = serializers.BooleanField(required=False, default=True)
    created_by = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True
    )

    def validate(self, attrs):
        if "user_id" in self.initial_data:
            raise serializers.ValidationError(
                {"user_id": "Use X-User-Id header, not request body."}
            )
        return attrs


class CategoryUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    icon = serializers.CharField(max_length=255, required=False, allow_blank=True)
    parent_id = NullIntField(required=False, allow_null=True)
    status = serializers.BooleanField(required=False)
    updated_by = serializers.CharField(
        max_length=255, required=False, allow_blank=True, allow_null=True
    )

    def validate(self, attrs):
        if "user_id" in self.initial_data:
            raise serializers.ValidationError(
                {"user_id": "Use X-User-Id header, not request body."}
            )
        return attrs


class CategoryListSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "icon",
            "user_id",
            "parent_id",
            "parent_name",
            "status",
        ]

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None


class CategoryResponseSerializer(serializers.ModelSerializer):
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "icon",
            "user_id",
            "parent_id",
            "parent_name",
            "status",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
        ]

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None
