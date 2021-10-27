from rest_framework import serializers

from notes.models import Labels, NotesModel


class NotesSerializer(serializers.ModelSerializer):

    class Meta:

        model = NotesModel
        fields = "__all__"

    def create(self, validated_data):
        notes = NotesModel.objects.create(
            title=validated_data.get("title"),
            description=validated_data.get("description"),
            user_id = validated_data.get("user_id"),
            )
        if validated_data.get("collaborators"):
            notes.collaborators.set(validated_data.get("collaborators"))
        if validated_data.get("label"):
            notes.label.set(validated_data.get("label"))
        return notes

    def update(self, instance, validated_data):

        instance.title = validated_data.get("title",instance.title)
        instance.description = validated_data.get("description",instance.description)
        instance.is_binned = validated_data.get("is_binned",instance.is_binned)
        instance.is_archive = validated_data.get("is_archive",instance.is_archive)
        if validated_data.get("label"):
            instance.label.set(validated_data.get("label"))
        instance.save()
        return instance

class LabelSerializer(serializers.ModelSerializer):

    class Meta:

        model = Labels
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)
