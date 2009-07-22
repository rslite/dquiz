from BeautifulSoup import BeautifulSoup
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from dquiz.vocab.models import Word, Definition, Answer
import math, random, re, unicodedata, urllib2

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
		return HttpResponseRedirect(reverse('vocab-quiz', args=(quiz_id, page)))
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
		url = reverse('vocab-quiz', args=(quiz_id, int(page)+1))
		return HttpResponseRedirect(url)

def add(request):
	# Check if we're posting back
	if 'w' in request.POST:
		sword = request.POST['w']
		index = request.POST['i']
	else:
		return render_to_response('vocab/add.htm', {})

	# Make the request
	try:
		url = 'http://www.merriam-webster.com/dictionary/' + sword
		if index:
			url += '[' + index + ']'
		res = urllib2.urlopen(url)
	except Exception as e:
		print e
		return HttpResponse("Word '%s' not found" % sword)
	data = unicodedata.normalize('NFKD', res.read().decode('utf8')).encode('ascii', 'ignore')
	res.close()

	# Prepare the regular expressions
	rgComments = re.compile(r'<!--.*?-->', re.S)
	rgSpan = re.compile(r'</?(span|div).*?>', re.S)
	rgLetters = re.compile(r'([a-z])<strong>:</strong>', re.S)
	rgStrong = re.compile(r'\s*<strong>:</strong>', re.S)
	rgSynonim = re.compile(r'<div class="synonym".*$', re.S)
	rgSpaces = re.compile(r'\s+', re.S)

	# Remove comments
	data = rgComments.sub('', data)

	# Initialize BS
	bs = BeautifulSoup(data)
	main = bs.findAll('div', attrs={'class':'defs'})
	if len(main) != 1:
		return HttpResponse("Word '%s' not found" % sword)
	else:
		main = main[0]
	
	print main
	print

	# Normalize spaces
	txt = rgSpaces.sub(' ', str(main).replace('\x0A', ' '))

	entries = txt.split('<span class=" sense_label start">')[1:]
	print entries
	print

	# Get/add the word
	if entries:
		word = Word.objects.filter(word=sword)
		if not word:
			word = Word(word=sword)
			word.save()
		else:
			word = word[0]
	else:
		return HttpResponse('No entries')

	texts = []

	# *** Prepare all entries
	for entry in entries:
		# Remove synonyms (in last entry)
		entry = rgSynonim.sub('', entry)
		# Get rid of spans, divs
		entry = rgSpan.sub('', entry)
		# Bold the subdef letters (a, b, ...)
		entry = rgLetters.sub(r'*\1*', entry)
		# Remove the digits of the definitions
		entry = re.sub(r'^\d\s*', '', entry)
		# Remove the strong colons
		entry = rgStrong.sub(':', entry)
		# Remove the colons at the beginning
		entry = re.sub(r'^:\s*', '', entry)
		# Change obsolete marker
		entry = re.sub(r'<em>(obsolete|also|especially)</em>', r'(\1)', entry)
		# Change word in examples
		entry = re.sub(r'</?em>', '_', entry)
		# Remove links
		entry = re.sub(r'</?a.*?>', '', entry)
		# Replace < and >
		entry = entry.replace('&lt;', '<').replace('&gt;', '>')

		print entry
		texts.append(entry)

		# Save the entry
		defi = Definition()
		defi.word = word
		defi.definition = entry
		defi.save()

	lword = Word.objects.filter(word=sword)
	if lword:
		word = lword[0]

	defs = word.definition_set.all()

	return render_to_response('vocab/add.htm', locals())
