from rest_framework import serializers

from .models import Medication, RefillRequest


class MedicationSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

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

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["added_by"] = user
        return super().create(validated_data)


class RefillRequestSerializer(serializers.ModelSerializer):
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
        read_only_fields = ["id", "user", "status", "requested_at", "updated_at"]

        def create(self, validated_data):
            user = self.context["request"].user
            validated_data["user"] = user
            return super().create(validated_data)


class RefillRequestDetailSerializer(serializers.ModelSerializer):
    medication = MedicationSerializer(read_only=True)

    class Meta:
        model = RefillRequest
        fields = [
            "id",
            "medication",
            "quantity",
            "status",
            "requested_at",
            "updated_at",
        ]
