from students.models import Student
from .serializers import StudentSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from employees.models import Employee
from rest_framework.views import APIView
from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.renderers import JSONRenderer, AdminRenderer
from rest_framework.parsers import JSONParser
from students.filters import EmployeeFilter
from blogs.models import Blog, Comments
from blogs.serializers import BlogSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from .pagination import CustomPagination
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from .customauth import CustomAuthentication
from .custompermissions import MyPermission, OwnerPermission
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, routers
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from .throttle import AdminRateThrottle
from validator.serializers import CustomerSerializer


# function based serializer
@api_view(["GET", "POST"])
def studentView(request):
    if request.method == "GET":
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def studentDetailView(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""class Employees(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializers = EmployeeSerializer(employees, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeesDetail(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)"""


# Mixins
"""class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class EmployeesDetail(mixins.RetrieveModelMixin, generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)
    
    def put(self, request, pk):
        return self.update(request, pk)
    
    def delete(self, request, pk):
        return self.destroy(request, pk)"""


# Generics
"""class Employees(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'
"""


# Viewsets
"""
class EmployeeViewset(viewsets.ViewSet):
    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
"""


class EmployeeViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    # filterset_fields = ['designation']
    filterset_class = EmployeeFilter
    authentication_classes = [SessionAuthentication]
    permission_classes = [DjangoModelPermissions]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'viewemp'


class BlogsView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["^blog_title"]  # starts with
    ordering_fields = ["id", "blog_title"]
    authentication_classes = [TokenAuthentication]
    throttle_classes = [AdminRateThrottle]
    permission_classes = [IsAuthenticated]


class CommentsView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    # renderer_classes = [AdminRenderer]
    parser_classes = [JSONParser]
    authentication_classes = [SessionAuthentication]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [OwnerPermission]


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "pk"
    # renderer_classes = [JSONRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"
    authentication_classes = [SessionAuthentication]
    permission_classes = [OwnerPermission]


'''class CustomerView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
'''
