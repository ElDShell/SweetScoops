from django.contrib import admin
from taggit.models import Tag
from .models import IceCream, NewTag, UUIDTaggedItem

# # Register the NewTag model to appear in the admin
# class IceCreamAdmin(admin.ModelAdmin):
#     list_display = ('name', 'flavor_display')  # Custom method to display the flavors

#     # # Custom method to display the tags as a comma-separated string
#     # def flavor_display(self, obj):
#     #     return ", ".join([tag.name for tag in obj.flavor.all()])
#     # flavor_display.short_description = 'Flavors'  # Customize column header name
#     def flavor_display(self, obj):
#         if obj.flavor.exists():  # Ensure there are flavors before trying to access them
#             return ", ".join([tag.name for tag in obj.flavor.all()])
#         return "No flavors assigned"  # Return a fallback message if no flavors exist
#     # Optional: Custom form to display flavors (if needed)
#     # form = IceCreamForm  # Uncomment this if you have a custom form

from django.contrib import admin
from .models import IceCream

class IceCreamAdmin(admin.ModelAdmin):
    search_fields = ['flavor__name']  # Allows searching by tag na
    list_filter = ['flavor']  # Adds a filter sidebar for tags
    
admin.site.register(IceCream,IceCreamAdmin)
    

# Register IceCream with the custom admin class
# Register your other models (NewTag, UUIDTaggedItem) if needed
@admin.register(NewTag)
class NewTagAdmin(admin.ModelAdmin):
    pass

@admin.register(UUIDTaggedItem)
class UUIDTaggedItemAdmin(admin.ModelAdmin):
    pass
