from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from dquiz.vocab.models import Word, Definition, Answer
import math, random, urllib2

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
	random.shuffle(words)

	# Get previous answer from session (and clear it)
	try:
		answer_data = request.session['answer_data']
		is_good = answer_data['is_good']
		old_def = answer_data['old_def']
		sel_answer = answer_data['answer']
		request.session['answer_data'] = None
	except:
		pass

	# Render the page
	return render_to_response('vocab/quiz.htm', locals())

def answer(request, quiz_id, page, def_id):
	print 'word_id', request.POST['word_id']
	try:
		sel_word = Word.objects.get(pk=request.POST['word_id'])
	except Exception as e:
		print 'Word not found', e
		return HttpResponseRedirect('/quiz/%s/%s' % (quiz_id, page))
	else:
		# Get the current definition
		definition = Definition.objects.get(pk=def_id)
		
		# Register the given answer
		answer = Answer(answer=sel_word, definition=definition)
		answer.save()

		# Update the definition counts
		definition.views += 1
		is_good = sel_word == definition.word
		if is_good:
			print 'Correct answer:', sel_word.word
			definition.correct += 1
		else:
			print 'Bad answer:', sel_word.word, ' correct:', definition.word.word
		definition.save()

		# Send information to the quiz view to display correct answer
		res = {}
		res['is_good'] = is_good
		res['old_def'] = definition
		res['answer'] = sel_word
		request.session['answer_data'] = res

		# Go to next question
		return HttpResponseRedirect('/quiz/%s/%d' % (quiz_id, int(page)+1))

def add(request, word):
	try:
		res = urllib2.urlopen('http://www.merriam-webster.com/dictionary/' + word)
	except Exception as e:
		print e
		return HttpResponse("Word '%s' not found" % word)
	data = res.read()
	res.close()
	return HttpResponse(data)
