from django.contrib import admin
from tracker.models import Issue, Status, Issue_type

# Register your models here.


class IssueAdmin(admin.ModelAdmin):
    list_display = ["id", "summary", "description", "status", "issue_type", "created_at", "updated_at"]
    list_filter = ["id", "summary", "status", "issue_type"]
    search_fields = ["description", "created_at", "updated_at"]
    fields = ["id", "summary", "description", "status", "issue_type", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at", "id"]

admin.site.register(Issue, IssueAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = ["id", "status_code"]
    list_filter = ["id", "status_code"]
    list_search = ["status_code"]
    fields = ["id", "status_code"]
    readonly_fields = ["id"]

admin.site.register(Status, StatusAdmin)

class Issue_typeAdmin(admin.ModelAdmin):
    list_display = ["id", "issue_type_code"]
    list_filter = ["id", "issue_type_code"]
    list_search = ["issue_type_code"]
    fields = ["id", "issue_type_code"]
    readonly_fields = ["id"]

admin.site.register(Issue_type, Issue_typeAdmin)