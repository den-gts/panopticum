from django.contrib import admin
from django.forms.widgets import SelectMultiple, NumberInput, TextInput, Select

import datetime

# Register your models here.
from panopticum.models import *


class ComponentDependencyAdmin(admin.TabularInline):
    model = ComponentVersionModel.depends_on.through


class ComponentVersionAdmin(admin.ModelAdmin):
    formfield_overrides = {models.ForeignKey: {'widget': Select(attrs={'width': '300px', 'style': 'width:300px'})},
                           models.ManyToManyField: {'widget': SelectMultiple(attrs={'size': '7', 'width': '300px', 'style': 'width:300px'})},
                           models.IntegerField: {'widget': NumberInput(attrs={'width': '300px', 'style': 'width:300px'})},
                           models.CharField: {'widget': TextInput(attrs={'width': '300px', 'style': 'width:300px'})},
                           models.URLField: {'widget': TextInput(attrs={'width': '300px', 'style': 'width:300px'})}
                           }

    inlines = (ComponentDependencyAdmin,)

    fieldsets = (
        (None, {'fields': ('component', 'version', 'comments')}),
        ('Ownership', {'classes': ('collapse',),
                       'fields': (
                                  ('owner_maintainer', 'owner_responsible_qa'),
                                  ('owner_product_manager', 'owner_program_manager'),
                                  ('owner_expert', 'owner_escalation_list'), 'owner_architect')}),
        ('Development', {'classes': ('collapse',),
                          'fields': ('dev_language', 'dev_framework', 'dev_database', 'dev_orm', 'dev_logging',
                                     ('dev_raml', 'dev_jira_component'),
                                     ('dev_repo', 'dev_public_repo'),
                                     ('dev_docs', 'dev_public_docs'),
                                     ('dev_build_jenkins_job', 'dev_api_is_public'))}),
        ('Compliance', {'classes': ('collapse',),
                          'fields': (
                                     ('compliance_fips_status', 'compliance_fips_notes'),
                                     ('compliance_gdpr_status', 'compliance_gdpr_notes'),
                                     ('compliance_api_status', 'compliance_api_notes'))}),
        ('Operations capabilities', {'classes': ('collapse',),
                          'fields': (
                                     ('op_guide_status', 'op_guide_notes'),
                                     ('op_failover_status', 'op_failover_notes'),
                                     ('op_horizontal_scalability_status', 'op_horizontal_scalability_notes'),
                                     ('op_scaling_guide_status', 'op_scaling_guide_notes'),
                                     ('op_sla_guide_status', 'op_sla_guide_notes'),
                                     ('op_metrics_status', 'op_metrics_notes'),
                                     ('op_alerts_status', 'op_alerts_notes'),
                                     ('op_zero_downtime_status', 'op_zero_downtime_notes'),
                                     ('op_backup_status', 'op_backup_notes'),
                                      'op_safe_restart')}),
        ('Maintenance capabilities', {'classes': ('collapse',),
                          'fields': (('mt_http_tracing_status', 'mt_http_tracing_notes'),
                                     ('mt_logging_sufficiency_status', 'mt_logging_sufficiency_notes'),
                                     ('mt_logging_format_status', 'mt_logging_format_notes'),
                                     ('mt_logging_storage_status', 'mt_logging_storage_notes'),
                                     ('mt_anonymisation_status', 'mt_anonymisation_notes'))}),
        ('Quality Assurance', {'classes': ('collapse',),
                          'fields': (('qa_manual_tests_quality', 'qa_manual_tests_notes'),
                                     ('qa_unit_tests_quality', 'qa_unit_tests_notes'),
                                     ('qa_e2e_tests_quality', 'qa_e2e_tests_notes'),
                                     ('qa_perf_tests_quality', 'qa_perf_tests_notes'),
                                     ('qa_security_tests_quality', 'qa_security_tests_notes'),
                                     ('qa_longhaul_tests_quality', 'qa_longhaul_tests_notes'),
                                     ('qa_api_tests_quality', 'qa_api_tests_notes'))}),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # standard django method
        if db_field.name in ("owner_product_manager", "owner_program_manager", "owner_expert",
                             "owner_escalation_list", "owner_architect"):
            kwargs["queryset"] = PersonModel.objects.filter(hidden=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # standard django method
        if db_field.name in ("owner_maintainer", "owner_responsible_qa"):
            kwargs["queryset"] = PersonModel.objects.filter(hidden=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # standard django method
        if obj.pk:
            orig_obj = ComponentVersionModel.objects.get(id=obj.id)
            if orig_obj.version != obj.version:
                obj.id = None
        obj.meta_update_date = datetime.datetime.now()
        obj.meta_deleted = False
        super().save_model(request, obj, form, change)


admin.site.register(CountryModel)
admin.site.register(OrganizationModel)
admin.site.register(OrgDepartmentModel)
admin.site.register(PersonRoleModel)
admin.site.register(PersonModel)

admin.site.register(SoftwareVendorModel)
admin.site.register(DatabaseVendorModel)
admin.site.register(ProductFamilyModel)
admin.site.register(ProductModel)
admin.site.register(ProgrammingLanguageModel)
admin.site.register(FrameworkModel)
admin.site.register(ORMModel)
admin.site.register(LoggerModel)
admin.site.register(ComponentRuntimeTypeModel)
admin.site.register(ComponentDataPrivacyClassModel)
admin.site.register(ComponentCategoryModel)
admin.site.register(ComponentSubcategoryModel)
admin.site.register(ComponentModel)
admin.site.register(ComponentVersionModel, ComponentVersionAdmin)
