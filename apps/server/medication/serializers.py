from rest_framework import serializers

from .models import Medication, RefillRequest


class MedicationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Medication
        fields = [
            "id",
            "name",
            "dosage",
            "quantity",
            "instructions",
            "image",
            "added_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "added_by", "created_at", "updated_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["added_by"] = user
        return super().create(validated_data)


class RefillRequestSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    medication = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all())

    class Meta:
        model = RefillRequest
        fields = [
            "id",
            "user",
            "medication",
            "quantity",
            "status",
            "requested_at",
            "updated_at",
        ]
        read_only_fields = ["status", "requested_at", "updated_at"]


class RefillRequestDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    medication = MedicationSerializer(read_only=True)

    class Meta:
        model = RefillRequest
        fields = [
            "id",
            "user",
            "medication",
            "quantity",
            "status",
            "requested_at",
            "updated_at",
        ]
