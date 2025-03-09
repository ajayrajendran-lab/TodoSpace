from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import UserCreationSerializer,TodoSerializer
from rest_framework import authentication,permissions,serializers
from myapp.models import Todo
from api.permissions import IsOwnerPermissionRequired
from django.db.models import Count

# Create your views here.
class UserCreateView(APIView):

    def post(self,request,*args,**kwargs):
        serializer_instance=UserCreationSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)


class TodoListCreateView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        all_todos=Todo.objects.filter(owner=request.user)
        serializer_instance=TodoSerializer(all_todos,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request,*args,**kwargs):
        serializer_instance=TodoSerializer(data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save(owner=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class TodoRetrieveUpdateDestroyView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[IsOwnerPermissionRequired]

    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_instance=get_object_or_404(Todo,id=id)
        self.check_object_permissions(request,todo_instance)

        # if todo_instance.owner != request.user:
        #     raise serializers.ValidationError("You do not have the permission to access this data")
        
        serializer_instance = TodoSerializer(todo_instance)
        return Response(data=serializer_instance.data)

    def put(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_instance=get_object_or_404(Todo,id=id)
        self.check_object_permissions(request,todo_instance)
        # if todo_instance.owner != request.user:
        #     raise serializers.ValidationError("You do not have the permission to access this data")
        serializer_instance=TodoSerializer(data=request.data,instance=todo_instance)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        todo_instance=get_object_or_404(Todo,id=id)
        self.check_object_permissions(request,todo_instance)

        # if todo_instance.owner != request.user:
        #     raise serializers.ValidationError("You do not have the permission to access this data")
        
        todo_instance.delete()
        return Response({"message":"Deleted"})

class TodoSummaryView(APIView):
    def get(self,request,*args,**kwargs):
        category_summary=Todo.objects.filter(owner=request.user).values("category").annotate(count=Count("category"))
        priority_summary=Todo.objects.filter(owner=request.user).values("priority").annotate(count=Count("priority"))
        status_summary=Todo.objects.filter(owner=request.user).values("priority").annotate(count=Count("priority"))

        context={
            "category_summary":category_summary,
            "priority_summary":priority_summary,
            "status_summary":status_summary
        }

        return Response(data=context)