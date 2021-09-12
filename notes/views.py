import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from notes.models import NotesModel
from notes.serializers import NotesSerializer
from notes.utility import EncodeDecodeToken

logging.basicConfig(filename="fundooNotes.log", filemode="a")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create your views here.
class Notes(APIView):

    """
    Notes api to manage all the curd operations regarding to notes
    """

    def get(self, request):
        
        try:
            decode_token = EncodeDecodeToken.decode_token(request.META.get('HTTP_TOKEN'))
            user_id = decode_token.get("user_id")   
            serializer = NotesSerializer(
                NotesModel.objects.filter(user_id=user_id), many=True
            )
            logger.info("Get all notes of user id = "+str(user_id))
            return Response(
                {
                    "message": "Welcome to our notes",
                    "data": {"notelist": serializer.data},
                },
                status=status.HTTP_200_OK,
            )
        except TypeError:
            return Response("token not found")
        except Exception as e:
            logger.error(f"internal server error while viewing all notes due to {str(e)}")
            return Response(
                {
                    "message": "internal server error",
                    "data": {"error":str(e)},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):

        try:
            decode_token = EncodeDecodeToken.decode_token(request.META.get('HTTP_TOKEN'))
            notes_data = request.data
            notes_data["user_id"] = decode_token.get("user_id")
            serializer = NotesSerializer(data=notes_data)
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
            logger.warning("invalid data while adding a note "+str(serializer.errors))
            return Response(
                {
                    "message": "invalid data or login in before you add notes",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
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
            logger.error("error while adding notes")
            return Response(
                {
                    "message": "error while adding notes",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

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
            logger.warning("Invalid data while updating notes "+str(serializer.errors))
            return Response(
                {
                    "message": "Error while updating notes",
                    "data": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
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
            logger.error("data not found for updation")
            return Response(
                {
                    "message": "no such note found",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

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
