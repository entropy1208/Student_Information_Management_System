from rest_framework import serializers


from .models import Student


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='students:student_detail')

    class Meta:
        model = Student
        fields = ('id', 'url',  'name', 'email',
                  'state', 'city', 'gender', 'ph_no')
