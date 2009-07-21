from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from dquiz.vocab.models import Word, Definition
import math, random

def get_random_item(model, max_id=None):
	""" Get a random object of the specified model """
	if max_id is None:
		max_id = model.objects.aggregate(Max('id')).values()[0]
	min_id = math.ceil(max_id * random.random())
	return model.objects.filter(id__gte=min_id)[0]

def quiz(request, quiz_id, page):
	# Quiz ID will always be the random seed
	random.seed(quiz_id)

	# If no page specified start with first page
	if not page:
		page = 1
	else:
		page = int(page)

	# Get to the current page definition from the quiz
	for x in xrange(page):
		definition = get_random_item(Definition)
	words = [definition.word]
	while len(words) < 5:
		word = get_random_item(Word)
		if not word in words:
			words.append(word)

	# Render the page
	data = { 'def': definition, 'words': words, 'page': page}
	return render_to_response('vocab/quiz.htm', data)
