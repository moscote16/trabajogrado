from django.contrib import admin
from .models import Pruebas, Canino

@admin.register(Pruebas)
class PruebaAdmin(admin.ModelAdmin):
    list_display = ('tipo_prueba', 'get_diagnostico_display',  'archivo')

    def get_diagnostico_display(self, obj):
        return obj.get_diagnostico_display()
    get_diagnostico_display.short_description = 'Diagnóstico'

class CaninoAdmin(admin.ModelAdmin):
    list_display = ('imagen','id_canino', 'nombre_canino', 'nombre_dueño', 'dictamen', 'cedula', 'telefono', 'años_canino')
    search_fields = ('nombre_canino', 'nombre_dueño', 'cedula')
admin.site.register(Canino, CaninoAdmin)