from rest_framework import serializers

from .models import DirectorProfile, ParentProfile, TeacherProfile, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'full_name',
            'email',
            'phone',
            'password',
            'role',
            'school',
            'school_name',
            'is_active',
        )
        read_only_fields = ('id',)
        extra_kwargs = {
            'username': {'required': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not validated_data.get('username'):
            validated_data['username'] = validated_data.get('email', '')
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user


class DirectorProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = DirectorProfile
        fields = ('id', 'user', 'user_name', 'user_email', 'school', 'school_name')


class TeacherProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = TeacherProfile
        fields = (
            'id',
            'user',
            'user_name',
            'user_email',
            'school',
            'school_name',
            'employee_code',
        )


class ParentProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = ParentProfile
        fields = (
            'id',
            'user',
            'user_name',
            'user_email',
            'school',
            'school_name',
            'address',
        )
