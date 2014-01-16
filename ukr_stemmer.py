#!/usr/bin/python
# -*- coding: utf8 -*-py

"""
Russian stemming algorithm provided by Dr Martin Porter (snowball.tartarus.org):
http://snowball.tartarus.org/algorithms/russian/stemmer.html

Algorithm implementation in PHP provided by Dmitry Koterov (dklab.ru):
http://forum.dklab.ru/php/advises/HeuristicWithoutTheDictionaryExtractionOfARootFromRussianWord.html

Algorithm implementation adopted for Drupal by Algenon (4algenon@gmail.com):
https://drupal.org/project/ukstemmer

Algorithm implementation in Python by Zakharov Kyrylo
https://github.com/Amice13

"""


import re


class UkrainianStemmer():
     def __init__(self,word):
         self.word = word
         self.vowel = ur'аеиоуюяіїє'  # http://uk.wikipedia.org/wiki/Голосний_звук
         self.perfectiveground = ur'(ив|ивши|ившись|ыв|ывши|ывшись((?<=[ая])(в|вши|вшись)))$'
         self.reflexive = ur'(с[яьи])$'  # http://uk.wikipedia.org/wiki/Рефлексивне_дієслово
         self.adjective = ur'(ими|ій|ий|а|е|ова|ове|ів|є|їй|єє|еє|я|ім|ем|им|ім|их|іх|ою|йми|іми|у|ю|ого|ому|ої)$'  # http://uk.wikipedia.org/wiki/Прикметник + http://wapedia.mobi/uk/Прикметник
         self.participle = ur'(ий|ого|ому|им|ім|а|ій|у|ою|ій|і|их|йми|их)$'  # http://uk.wikipedia.org/wiki/Дієприкметник
         self.verb = ur'(сь|ся|ив|ать|ять|у|ю|ав|али|учи|ячи|вши|ши|е|ме|ати|яти|є)$'  # http://uk.wikipedia.org/wiki/Дієслово
         self.noun = ur'(а|ев|ов|е|ями|ами|еи|и|ей|ой|ий|й|иям|ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я|і|ові|ї|ею|єю|ою|є|еві|ем|єм|ів|їв|ю)$'  # http://uk.wikipedia.org/wiki/Іменник
         self.rvre = ur'[аеиоуюяіїє]'
         self.derivational = ur'[^аеиоуюяіїє][аеиоуюяіїє]+[^аеиоуюяіїє]+[аеиоуюяіїє].*(?<=о)сть?$'
         self.RV = ''

     def ukstemmer_search_preprocess(self,word):
         word = word.decode('utf-8').lower().encode('utf-8')
         word = word.replace("'","")
         word = word.replace("ё","е")
         word = word.replace("ъ","ї")
         return word

     def s(self,st, reg, to):
         orig = st
         self.RV = re.sub(reg, to, st)
	 return (orig != self.RV)

     def stem_word(self):
          word = self.ukstemmer_search_preprocess(self.word)
          p = re.search(self.rvre,word.decode('utf-8'))
          start = word.decode('utf-8')[0:p.span()[1]]
          self.RV = word.decode('utf-8')[p.span()[1]:len(word)]

          # Step 1
          if not self.s(self.RV,self.perfectiveground,''):
              
              self.s(self.RV,self.reflexive,'')
              if self.s(self.RV,self.adjective,''):
                  self.s(self.RV,self.participle,'')
              else:
                  if not self.s(self.RV,self.verb,''): self.s(self.RV,self.noun,'')
          # Step 2
          self.s(self.RV,u'и$','')

          # Step 3
          if re.search(self.derivational,self.RV):
               self.s(self.RV,u'ость$','')

          # Step 4
          if self.s(self.RV,'ь$',''):
               self.s(self.RV,'ейше?$','')
               self.s(self.RV,'нн$','н')

          stem = start + self.RV
          return stem

# Use of class

word = raw_input('Word for stemming:')
stemmed = UkrainianStemmer(word)
print stemmed.stem_word()
