from rest_framework import serializers

from notes.models import NotesModel


class NotesSerializer(serializers.ModelSerializer):

    class Meta:

        model = NotesModel
        fields = "__all__"

    def create(self, validated_data):
        return NotesModel.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.title = validated_data.get("title",instance.title)
        instance.description = validated_data.get("description",instance.description)
        instance.user_id = validated_data.get("user_id",instance.user_id)
        instance.save()
        return instance
