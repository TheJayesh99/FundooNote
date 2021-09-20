import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestNotes:

    def test_init(self):

        notes_obj = mixer.blend('notes.NotesModel')
        assert notes_obj.pk == 1 , 'should save an instance' 