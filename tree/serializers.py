from rest_framework import serializers
from .models import Family, FamilyMember, FamilyImage


class FamilySerializer(serializers.ModelSerializer):
    subfamilies = serializers.SerializerMethodField()

    class Meta:
        model = Family
        fields = '__all__'

    def get_subfamilies(self, obj):
        if obj.subfamilies.exists():
            return FamilySerializer(obj.subfamilies.all(), many=True).data
        return []


class FamilyRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ('members', 'parent', 'name',)


class FamilyListSerializer(FamilySerializer):
    class Meta:
        model = Family
        fields = ('id', 'name')


class FamilyDetailSerializer(FamilySerializer):
    class Meta:
        model = Family
        fields = ('name', 'members', 'parent', 'preview', )


class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = '__all__'


class FamilyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyImage
        fields = '__all__'


class RecursiveFamilySerializer(FamilySerializer):
    class Meta:
        model = Family
        fields = ('id', 'name', 'description', 'members', 'parent', 'subfamilies', )
