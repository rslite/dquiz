from django.db import models

class Word(models.Model):
	#The word that's defined
	word = models.CharField(max_length=200)  

	def __unicode__(self):
		return self.word

	class Meta:
		pass

class Definition(models.Model):
	# Defined word
	word = models.ForeignKey(Word)
	# The definition of the word
	definition = models.TextField(default='')
	# Number of views in a test
	views = models.IntegerField(default=0)
	# Number of correct answers
	correct = models.IntegerField(default=0)

	def __unicode__(self):
		return '%s (%d/%d)' % (self.definition[:100], self.correct, self.views)

	class Meta:
		pass
