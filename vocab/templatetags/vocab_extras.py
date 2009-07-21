from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

register = template.Library()

RG_BOLD = re.compile(r'\*(\w+)\*')
RG_ITALIC = re.compile(r'_(\w+)_')
RG_LTGT = re.compile(r'[<>]')
EXAMPLE = '*****' 

# Register a filter to process the simple markdown
@register.filter('markdown')
def markdown(value):
	""" Simple markdown for bolding and removing italic stuff (word in examples) """

	def ltgt_repl(match):
		""" Regex replacer of < and > with italics """
		print match.group(0)
		if match.group(0) == '<': return '&lt;<i>'
		else: return '</i>&gt;'

	newval = value

	# Fix < and >
	newval = RG_LTGT.sub(ltgt_repl, newval)

	# Bolding step
	newval = RG_BOLD.sub(r'<b>\1</b>', newval)

	# Remove italic (hide the word in examples)
	newval = RG_ITALIC.sub(EXAMPLE, newval)

	return mark_safe(newval)
markdown.is_safe = True
#markdown.needs_autoescape = True
