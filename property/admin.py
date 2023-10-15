from django.contrib import admin
from .models import Flat, Complaint


class RoomsNumberFilter(admin.SimpleListFilter):
    title = 'Количество комнат'
    parameter_name = 'rooms_number'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Однокомнатные'),
            ('2', 'Двухкомнатные'),
            ('3', 'Трехкомнатные'),
            ('4', 'Четырехкомнатные'),
            ('5', 'Пятикомнатные'),
        )

    def queryset(self, request, queryset):
        rooms = self.value()
        if rooms == '1':
            return queryset.filter(rooms_number=1)
        if rooms == '2':
            return queryset.filter(rooms_number=2)
        if rooms == '3':
            return queryset.filter(rooms_number=3)
        if rooms == '4':
            return queryset.filter(rooms_number=4)
        if rooms == '5':
            return queryset.filter(rooms_number=5)


class HasBalconyFilter(admin.SimpleListFilter):
    title = 'Наличие балкона'
    parameter_name = 'has_balcony'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        values = self.value()
        if values is not None:
            if values == 'yes':
                return queryset.filter(has_balcony=True)
            elif values == 'no':
                return queryset.filter(has_balcony=False)


class PriceCategoryFilter(admin.SimpleListFilter):
    title = 'Стоимость квартиры'
    parameter_name = 'price_category'

    def lookups(self, request, model_admin):
        return (
            ('cheap', 'От 350 000'),
            ('expensive', 'От 3 100 000'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'cheap':
            return queryset.filter(price__gte=350000).order_by('price')
        if self.value() == 'expensive':
            return queryset.filter(price__gte=3100000).order_by('price')


class FlatAdmin(admin.ModelAdmin):
    search_fields = ['town', 'owner', 'address', ]
    readonly_fields = ['created_at', ]
    list_display = ('address', 'price', 'new_building', 'construction_year', 'town')
    list_editable = ('new_building',)
    list_filter = ('new_building', PriceCategoryFilter, RoomsNumberFilter, HasBalconyFilter,)


class ComplaintAdmin(admin.ModelAdmin):
    raw_id_fields = ('flat',)


admin.site.register(Flat, FlatAdmin)
admin.site.register(Complaint, ComplaintAdmin)
