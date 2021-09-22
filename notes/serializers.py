from rest_framework import serializers

from notes.models import NotesModel


class NotesSerializer(serializers.ModelSerializer):

    class Meta:

        model = NotesModel
        fields = "__all__"

    def create(self, validated_data):
        notes = NotesModel.objects.create(
            title=validated_data.get("title"),
            description=validated_data.get("description"),
            user_id = validated_data.get("user_id"),
            labels = validated_data.get("labels"),
            )
        notes.save()
        notes.contributers.set(validated_data.get("contributers"))
        return notes

    def update(self, instance, validated_data):

        instance.title = validated_data.get("title",instance.title)
        instance.description = validated_data.get("description",instance.description)
        instance.labels = validated_data.get("labels",instance.labels)
        instance.save()
        return instance
