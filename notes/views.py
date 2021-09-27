import logging

from django.db.models import Q
from drf_yasg import openapi
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from user_api.models import User
from user_api.serializers import UserSerializer

from notes.models import Labels, NotesModel
from notes.serializers import LabelSerializer, NotesSerializer
from notes.utility import verify_token, notes_converter, user_details 
from drf_yasg.utils import swagger_auto_schema

logging.basicConfig(filename="fundooNotes.log", filemode="a")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

header = openapi.Parameter('token',in_=openapi.IN_HEADER,type=openapi.TYPE_STRING)
# Create your views here.
class Notes(APIView):

    """
    Notes api to manage all the curd operations regarding to notes
    """
    @swagger_auto_schema(
        operation_summary="fetch notes",
        manual_parameters=[header])
    @verify_token
    def get(self, request):
        
        try:
            owner = Q(user_id=request.data.get("user_id"))
            collaborators = Q(collaborators=request.data.get("user_id"))
            notes = NotesModel.objects.filter(owner | collaborators)
            serializer = NotesSerializer(
               notes, many=True
            )
            notes_converter(serializer.data)
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
    
    @swagger_auto_schema(
        operation_summary="Add notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title' : openapi.Schema(type=openapi.TYPE_STRING,description="title"),
                'description' : openapi.Schema(type=openapi.TYPE_STRING,description="description"),
            }
        ),
        manual_parameters=[header])
    @verify_token
    def post(self, request):

        try:
            serializer = NotesSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info("Added notes by user id "+str(serializer.data["user_id"])+"and note id = "+str(serializer.data["id"]))
                note = notes_converter([serializer.data])
                return Response(
                    {
                        "message": "notes added successfully",
                        "data": {"note": note},
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

    @swagger_auto_schema(
        operation_summary="update notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title' : openapi.Schema(type=openapi.TYPE_STRING,description="title"),
                'description' : openapi.Schema(type=openapi.TYPE_STRING,description="description"),
                'id' : openapi.Schema(type=openapi.TYPE_INTEGER,description="note id"),
            }
        ),
        manual_parameters=[header])
    @verify_token
    def put(self, request):

        try:
            note = NotesModel.objects.get(id=request.data["id"]) 
            serializer = NotesSerializer(note, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info("note updated successfully of note id = "+str(serializer.data["id"]))
                note = notes_converter([serializer.data])
                return Response(
                    {
                        "message": "note updated successfully",
                        "data": note,
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

    @swagger_auto_schema(
        operation_summary="Delete notes",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id' : openapi.Schema(type=openapi.TYPE_INTEGER,description="note id"),
            }
        ),
        manual_parameters=[header])
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

    """
    Labels api to manage all the labels on the notes 
    """
    @swagger_auto_schema(
        operation_summary="get label",
        manual_parameters=[header])
    @verify_token
    def get(self, request):

        try:
            label = Labels.objects.filter(id=request.data.get("id")) 
            serializer = LabelSerializer(label, many=True)
            return Response({
                "message" : "The label retrived sucessfully",
                "data" : {
                    "label":serializer.data
                    }
                },
                status=status.HTTP_202_ACCEPTED
                )
        except Exception as e:
            logger.error(f"internal server error while viewing all label due to {str(e)}")
            return Response(
                {
                    "message": "internal server error",
                    "data": {"error":str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="add label",
        request_body=LabelSerializer,
        manual_parameters=[header])
    @verify_token
    def post(self, request):

        try:
            serializer = LabelSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({
                "message":"label created sucessfully",
                "data":serializer.data
                },
                status=status.HTTP_201_CREATED
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

    @swagger_auto_schema(
        operation_summary="update label",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'label' : openapi.Schema(type=openapi.TYPE_STRING,description="title"),
                'color' : openapi.Schema(type=openapi.TYPE_STRING,description="description"),
                'id' : openapi.Schema(type=openapi.TYPE_INTEGER,description="label id"),
            }
        ),
        manual_parameters=[header])
    @verify_token
    def put(self, request):

        try:
            label = Labels.objects.get(id=request.data.get("id"))
            serializer = LabelSerializer(label,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info("label updated successfully of label id = "+str(serializer.data["id"]))
                return Response(
                    {
                        "message": "label updated successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
        except Exception as e:
            logger.error(f"data not found for updation {str(e)}")
            return Response(
                {
                    "message": "no such label found",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    @swagger_auto_schema(
        operation_summary="Delete label",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id' : openapi.Schema(type=openapi.TYPE_INTEGER,description="label id"),
            }
        ),
        manual_parameters=[header])
    @verify_token   
    def delete(self, request):

        try:
            label = Labels.objects.get(id=request.data["id"])
            label.delete()
            logger.info("label deleted suceessfully having label id "+ str(request.data["id"]))
            return Response(
                {
                    "message": "label deleted successfully",
                    "data": {},
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            logger.error(f"error occured while deleting a label {str(e)}")
            return Response(
                {
                    "message": "no such label",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

class Collaborators(APIView):

    """
    Api to manage all the Collaborators on the notes
    """
    @verify_token
    def get(self, request):

        try:
            note = NotesModel.objects.get(id=request.data.get("id"))
            collaboraters = note.collaborators.all()
            serializer = UserSerializer(collaboraters, many=True)
            collaboraters_usernames = user_details(serializer.data)
            return Response({
                "message" : "The notes retrived sucessfully",
                "data" : {
                    "collaboraters":collaboraters_usernames
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

    @swagger_auto_schema(
        operation_summary="add collaborators",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id' : openapi.Schema(type=openapi.TYPE_INTEGER,description="note id"),
                'collaborators': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                    description="username of collaborators")
            }
        ),
        manual_parameters=[header])
    @verify_token
    def put(self, request):
        
        try:
            note = NotesModel.objects.get(id=request.data.get("id"))
            serializer = NotesSerializer(note)
            if request.data.get("collaborators"):
                user_id_list = []
                for user in request.data.get("collaborators"):
                    user_id = User.objects.get(username= user)
                    user_id_list.append(user_id.id)
                note.collaborators.set(user_id_list)
                logger.info("Added collaborators by user id "+str(serializer.data["user_id"])+"and note id = "+str(serializer.data["id"]))
                note = notes_converter([serializer.data])
                return Response(
                    {
                        "message": "collaborators added successfully",
                        "data": {"note": note},
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {
                    "message": "failed to add collaborators",
                    "data": {"note": serializer.data},
                },
                status=status.HTTP_304_NOT_MODIFIED,
            )

        except Exception as e:
            logger.error(f"error while adding collaborators {str(e)}")
            return Response(
                {
                    "message": "error while adding collaborators",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        operation_summary="Delete collaborators",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id' : openapi.Schema(type=openapi.TYPE_INTEGER,description="note id"),
                'user' : openapi.Schema(type=openapi.TYPE_STRING,description="username"),
            }
        ),
        manual_parameters=[header])
    @verify_token
    def delete(self, request):

        try:
            user = User.objects.get(username=request.data.get("user"))
            note = NotesModel.objects.get(id=request.data.get("id"))
            note.collaborators.remove(user)
            logger.info("collaborators removed suceessfully having collaborators id "+ str(request.data["id"]))
            return Response(
                {
                    "message": "collaborators removed successfully",
                    "data": {},
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            logger.error("error occured while deleting a collaborators")
            return Response(
                {
                    "message": "no such collaborators",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

class LabelNote(APIView):

    """
    Api to set label on notes 
    """
    @verify_token
    def get(self, request):

        try:
            label = Q(label=request.data.get("id"))
            owner = Q(user_id = request.data.get("user_id"))
            collaborators = Q(collaborators=request.data.get("user_id"))
            notes = NotesModel.objects.filter( label & (owner | collaborators)) 
            serializer = NotesSerializer(notes, many=True)
            notes_converter(serializer.data)
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

    @swagger_auto_schema(
        operation_summary="add label to note",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id' : openapi.Schema(type=openapi.TYPE_INTEGER,description="note id"),
                'label': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="id of label")
            }
        ),
        manual_parameters=[header])
    @verify_token
    def put(self, request):

        try:
            note = NotesModel.objects.get(id=request.data.get("id"))
            serializer = NotesSerializer(note)
            if request.data.get("label"):
                note.label.set(request.data.get("label"))
                logger.info("Added label by user id "+str(serializer.data["user_id"])+"and note id = "+str(serializer.data["id"]))
                note = notes_converter([serializer.data])
                return Response(
                    {
                        "message": "label added successfully",
                        "data": {"note": note},
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {
                    "message": "failed to add label",
                    "data": {"note": serializer.data},
                },
                status=status.HTTP_304_NOT_MODIFIED,
            )
        except Exception as e:
            logger.error(f"error while adding label {str(e)}")
            return Response(
                {
                    "message": "error while adding label",
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        operation_summary="remove labels",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id' : openapi.Schema(type=openapi.TYPE_INTEGER,description="note id"),
                'label_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="id of label")
            }
        ),
        manual_parameters=[header])
    @verify_token
    def delete(self, request):
        try:
            label = Labels.objects.get(id=request.data.get("label_id"))
            note = NotesModel.objects.get(id=request.data.get("id"))
            note.label.remove(label)
            logger.info("label removed suceessfully having note id "+ str(request.data["id"]))
            return Response(
                {
                    "message": "label removed successfully",
                    "data": {},
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            logger.error("error occured while deleting a label")
            return Response(
                {
                    "message": "no such label",
                    "data": {},
                },
                status=status.HTTP_404_NOT_FOUND,
            )

