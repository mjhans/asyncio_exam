import re
import reprlib
RE_WORD = re.compile('\w+')

###############################################################################
class Sentence:


    #==========================================================================
    @profile
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)


    #==========================================================================
    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)


    #==========================================================================
    @profile
    def __iter__(self):
        for word in self.words:
            yield word
        return


@profile
def print_word(s):
    for word in s:
        word
        #print("loop :{}".format(word))

###############################################################################
if __name__ == "__main__":
    text="""An object representing a stream of data. Repeated calls to the iterator’s next() method return successive items in the stream. When no more data are available a StopIteration exception is raised instead. At this point, the iterator object is exhausted and any further calls to its next() method just raise StopIteration again. Iterators are required to have an __iter__() method that returns the iterator object itself so every iterator is also iterable and may be used in most places where other iterables are accepted. One notable exception is code which attempts multiple iteration passes. A container object (such as a list) produces a fresh new iterator each time you pass it to the iter() function or use it in a for loop. Attempting this with an iterator will just return the same exhausted iterator object used in the previous iteration pass, making it appear like an empty container.
"""
    s = Sentence(text)
    print_word(s)

