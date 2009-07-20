from dquiz.vocab.models import Word, Definition
from django.contrib import admin

class DefinitionInline(admin.TabularInline):
	# Only show the definition fields (at least for now)
	fields = ('definition',)
	model = Definition
	extra = 3

class WordAdmin(admin.ModelAdmin):
	inlines = [DefinitionInline,]

admin.site.register(Word, WordAdmin)
