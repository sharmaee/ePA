# from django.contrib import admin

# from portal.models.auth import User, ClientCompany


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = (
#         'email',
#         'first_name',
#         'last_name',
#         'is_staff',
#         'is_active',
#         'submission_date',
#     )
#     list_filter = (
#         'is_staff',
#         'is_active',
#     )
#     search_fields = (
#         'email',
#         'first_name',
#         'last_name',
#     )


# @admin.register(ClientCompany)
# class ClientCompanyAdmin(admin.ModelAdmin):
#     list_display = (
#         'company_name',
#         'email_domain',
#         'is_active',
#         'number_of_seats',
#     )
#     list_filter = (
#         'is_active',
#     )
#     search_fields = (
#         'company_name',
#         'email_domain',
#     )
