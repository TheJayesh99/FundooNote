import logging

from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.models import NotesModel
from notes.serializers import NotesSerializer
from notes.utility import verify_token

logging.basicConfig(filename="fundooNotes.log", filemode="a")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create your views here.
class Notes(APIView):

    """
    Notes api to manage all the curd operations regarding to notes
    """
    @verify_token
    def get(self, request):
        
        try:
            owner = Q(user_id=request.data.get("user_id"))
            contributer = Q(contributers=request.data.get("user_id"))
            notes = NotesModel.objects.filter(owner | contributer)
            serializer = NotesSerializer(
               notes, many=True
            )
            logger.info("Get all notes of user id = "+str(request.data.get("user_id")))
            return Response(
                {
                    "message": "Welcome to our notes",
                    "data": {"notelist": serializer.data},
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"internal server error while viewing all notes due to {str(e)}")
            return Response(
                {
                    "message": "internal server error",
                    "data": {"error":str(e)},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    @verify_token
    def post(self, request):

        try:
            serializer = NotesSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info("Added notes by user id "+str(serializer.data["user_id"])+"and note id = "+str(serializer.data["id"]))
                return Response(
                    {
                        "message": "notes added successfully",
                        "data": {"note": serializer.data},
                    },
                    status=status.HTTP_201_CREATED,
                )
            
        except ValidationError:
            logger.error("validation failed while adding notes")
            return Response(
                {
                    "message":"Validation failed",
                    "data":serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"error while adding notes {str(e)}")
            return Response(
                {
                    "message": "error while adding notes",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @verify_token
    def put(self, request):

        try:
            note = NotesModel.objects.get(id=request.data["id"]) 
            serializer = NotesSerializer(note, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info("note updated successfully of note id = "+str(serializer.data["id"]))
                return Response(
                    {
                        "message": "note updated successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
        except ValidationError:
            logger.error("validation failed while updating notes")
            return Response(
                {
                    "message":"Validation failed",
                    "data":serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"data not found for updation {str(e)}")
            return Response(
                {
                    "message": "no such note found",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    @verify_token
    def delete(self, request):

        try:
            note = NotesModel.objects.get(id=request.data["id"])
            note.delete()
            logger.info("note deleted suceessfully having note id "+ str(request.data["id"]))
            return Response(
                {
                    "message": "notes deleted successfully",
                    "data": {},
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            logger.error("error occured while deleting a note")
            return Response(
                {
                    "message": "no such note",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

class Label(APIView):

    @verify_token
    def get(self, request):

        try:
            label = Q(labels__contains=request.data.get("labels"))
            owner = Q(user_id = request.data.get("user_id"))
            contributer = Q(contributers=request.data.get("user_id"))
            notes = NotesModel.objects.filter( label & (owner | contributer)) 
            serializer = NotesSerializer(notes, many=True)
            return Response({
                "message" : "The notes retrived sucessfully",
                "data" : {
                    "notelist":serializer.data
                    }
                },
                status=status.HTTP_202_ACCEPTED
                )
        except Exception as e:
            logger.error(f"internal server error while viewing all notes due to {str(e)}")
            return Response(
                {
                    "message": "internal server error",
                    "data": {"error":str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
