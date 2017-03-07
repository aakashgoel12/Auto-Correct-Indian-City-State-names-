from __future__ import division
import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('cities.txt').read()))

def P(word, N=sum(WORDS.values())): 
	#"Probability of `word`."
	return WORDS[word] / N

def correction(word): 
	#"Most probable spelling correction for word."
	l=candidates(word)
	return max(candidates(word), key=P)

def candidates(word): 
	"Generate possible spelling corrections for word."
	if(known([word])):
		return known([word])
	else:
		result_edits1= edits1(word)
		
		known_result_edits1=known(result_edits1)
		
		if(known_result_edits1):
			return known_result_edits1
		else:
			result_edits2=edits2(result_edits1)
			
			# result_edits2 is generator, so once it is tracersed, can't be traversed next time..
			
			known_result_edits2=known(result_edits2)
			
			if(known_result_edits2):
				return known_result_edits2
			else:
				result_edits3=edits3(result_edits2)
				known_result_edits3=known(result_edits3)
				if(known_result_edits3):
					return known_result_edits3
				else:
					return [word]
	#return (known([word]) or known(edits1(word)) or known(edits2(word)) or known(edits3(word)) or [word])

def known(words): 
	"The subset of `words` that appear in the dictionary of WORDS."
	return set([w for w in words if w in WORDS])

def edits1(word):
	#"All edits that are one edit away from `word`."
	letters    = 'abcdefghijklmnopqrstuvwxyz'
	splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
	deletes    = [L + R[1:]               for L, R in splits if R]
	transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
	replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
	inserts    = [L + c + R               for L, R in splits for c in letters]
	final_added_list=deletes + transposes + replaces + inserts
	return set(final_added_list)

# def edits2(word): 
	# "All edits that are two edits away from `word`."
	# return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def edits2(result_edits1): 
	"All edits that are two edits away from `word`."
	return [e2 for e1 in result_edits1 for e2 in edits1(e1)]

def edits3(result_edits2):
	#print "Inside edit3"
	#print result_edits2
	print "System gone in deep to answer your query better. Please be Patient.  :) "
	return [e3 for e2 in result_edits2 for e3 in edits1(e2)]

if __name__ == '__main__':
	print "Please Enter the Indian City or State Name..."
	i_p=raw_input()
	print "Corrected City Name is: "+str(correction(i_p))