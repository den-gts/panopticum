from django.contrib import admin
from django.forms.widgets import SelectMultiple, NumberInput, TextInput, Textarea, Select

import datetime

# Register your models here.
from panopticum.models import *

formfield_overrides = {models.ForeignKey: {'widget': Select(attrs={'width': '300px', 'style': 'width:300px'})},
                       models.ManyToManyField: {'widget': SelectMultiple(attrs={'size': '7', 'width': '300px', 'style': 'width:300px'})},
                       models.IntegerField: {'widget': NumberInput(attrs={'width': '300px', 'style': 'width:300px'})},
                       models.CharField: {'widget': TextInput(attrs={'width': '300px', 'style': 'width:300px'})},
                       models.URLField: {'widget': TextInput(attrs={'width': '300px', 'style': 'width:300px'})},
                       models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 60})},
                       }


class ComponentDependencyAdmin(admin.TabularInline):
    formfield_overrides = formfield_overrides
    model = ComponentVersion.depends_on.through


class ComponentVersionAdmin(admin.ModelAdmin):
    formfield_overrides = formfield_overrides

    inlines = (ComponentDependencyAdmin,)

    fieldsets = (
        (None, {'fields': ('component', 'version', 'comments', 'locations')}),
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
        ('Compliance', {'classes': ('collapse', 'show_hide_applicable'),
                          'fields': ('compliance_applicable',
                                     ('compliance_fips_status', 'compliance_fips_notes'),
                                     ('compliance_gdpr_status', 'compliance_gdpr_notes'),
                                     ('compliance_api_status', 'compliance_api_notes'))}),
        ('Operations capabilities', {'classes': ('collapse', 'show_hide_applicable'),
                          'fields': ('op_applicable',
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
        ('Maintenance capabilities', {'classes': ('collapse', 'show_hide_applicable'),
                          'fields': ('mt_applicable',
                                     ('mt_http_tracing_status', 'mt_http_tracing_notes'),
                                     ('mt_logging_completeness_status', 'mt_logging_completeness_notes'),
                                     ('mt_logging_format_status', 'mt_logging_format_notes'),
                                     ('mt_logging_storage_status', 'mt_logging_storage_notes'),
                                     ('mt_logging_sanitization_status', 'mt_logging_sanitization_notes'),
                                     ('mt_db_anonymisation_status', 'mt_db_anonymisation_notes'))}),
        ('Quality Assurance', {'classes': ('collapse', 'show_hide_applicable'),
                          'fields': ('qa_applicable',
                                     ('qa_manual_tests_status', 'qa_manual_tests_notes'),
                                     ('qa_unit_tests_status', 'qa_unit_tests_notes'),
                                     ('qa_e2e_tests_status', 'qa_e2e_tests_notes'),
                                     ('qa_perf_tests_status', 'qa_perf_tests_notes'),
                                     ('qa_security_tests_status', 'qa_security_tests_notes'),
                                     ('qa_longhaul_tests_status', 'qa_longhaul_tests_notes'),
                                     ('qa_api_tests_status', 'qa_api_tests_notes'),
                                     ('qa_anonymisation_tests_status', 'qa_anonymisation_tests_notes'),
                                     ('qa_upgrade_tests_status', 'qa_upgrade_tests_notes'))}),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # standard django method
        if db_field.name in ("owner_product_manager", "owner_program_manager", "owner_expert",
                             "owner_escalation_list", "owner_architect"):
            kwargs["queryset"] = Person.objects.filter(hidden=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # standard django method
        if db_field.name in ("owner_maintainer", "owner_responsible_qa"):
            kwargs["queryset"] = Person.objects.filter(hidden=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # standard django method
        if obj.pk:
            orig_obj = ComponentVersion.objects.get(id=obj.id)
            if orig_obj.version != obj.version:
                obj.id = None
        obj.meta_update_date = datetime.datetime.now()
        obj.meta_deleted = False
        super().save_model(request, obj, form, change)

    class Media:
        js = ('/static/js/admin.js',)
        css = {
                  'all': ('/static/css/admin.css',)
              }


admin.site.register(Country)
admin.site.register(Organization)
admin.site.register(Department)
admin.site.register(PersonRole)
admin.site.register(Person)

admin.site.register(SoftwareVendor)
admin.site.register(DatabaseVendor)
admin.site.register(ProductFamily)
admin.site.register(Product)
admin.site.register(ProgrammingLanguage)
admin.site.register(Framework)
admin.site.register(ORM)
admin.site.register(Logger)
admin.site.register(ComponentRuntimeType)
admin.site.register(ComponentDataPrivacyClass)
admin.site.register(ComponentCategory)
admin.site.register(ComponentSubcategory)
admin.site.register(Component)
admin.site.register(ComponentVersion, ComponentVersionAdmin)
admin.site.register(DeploymentLocationClass)
