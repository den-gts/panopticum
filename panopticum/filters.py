import rest_framework_filters as filters
from panopticum import models


class RequirementFilter(filters.FilterSet):
    """ allow to filter requirements at REST API side """

    class Meta:
        model = models.Requirement
        fields = '__all__'

class ComponentFilter(filters.FilterSet):
    name = filters.AutoFilter(lookups='__all__')

    class Meta:
        model = models.ComponentModel
        fields = '__all__'

class RequirementStatusTypeFilter(filters.FilterSet):

    class Meta:
        model = models.RequirementStatusType
        fields = '__all__'

class RequirementStatusFilter(filters.FilterSet):

    class Meta:
        model = models.RequirementStatus
        fields = '__all__'

class RequirementStatusEntryFilter(filters.FilterSet):
    requirement = filters.RelatedFilter(RequirementFilter,
                                        field_name='requirement',
                                        queryset=models.Requirement.objects.all(),
                                        lookups='__all__')
    component_version = filters.RelatedFilter('ComponentVersionFilter',
                                        field_name='component_version',
                                        queryset=models.ComponentVersionModel.objects.all(),
                                        lookups='__all__')
    status = filters.RelatedFilter(RequirementStatusFilter,
                                   field_name='status',
                                   queryset=models.RequirementStatus.objects.all(),
                                   lookups='__all__')

    class Meta:
        model = models.RequirementStatusEntry
        fields = '__all__'

class ComponentVersionFilter(filters.FilterSet):
    component = filters.RelatedFilter(ComponentFilter,
                                      field_name='component',
                                      queryset=models.ComponentModel.objects.all(),
                                      lookups='__all__')
    statuses = filters.RelatedFilter(RequirementStatusEntryFilter,
                                     field_name='statuses',
                                     queryset=models.RequirementStatusEntry.objects.all(),
                                     )
    class Meta:
        model = models.ComponentVersionModel
        fields = '__all__'
