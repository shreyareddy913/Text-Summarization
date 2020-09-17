#!/usr/bin/env python
# coding: utf-8

# In[21]:


from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize

text=''' Muhammad Ali (/ɑːˈliː/;[3] born Cassius Marcellus Clay Jr.;[4] January 17, 1942 – June 3, 2016) was an American professional boxer, activist, and philanthropist. Nicknamed "The Greatest", he is widely regarded as one of the most significant and celebrated figures of the 20th century and as one of the greatest boxers of all time.
Ali was born and raised in Louisville, Kentucky, and began training as an amateur boxer at age 12. At 18, he won a gold medal in the light heavyweight division at the 1960 Summer Olympics, and turned professional later that year. He converted to Islam and became a Muslim after 1961, and eventually took the name Muhammad Ali. He won the world heavyweight championship from Sonny Liston in a major upset at age 22 in 1964. In 1966, Ali refused to be drafted into the military, citing his religious beliefs and opposition to the Vietnam War.[5][6] He was arrested, found guilty of draft evasion, and stripped of his boxing titles. He appealed the decision to the Supreme Court, which overturned his conviction in 1971, but he had not fought for nearly four years and lost a period of peak performance as an athlete. His actions as a conscientious objector to the war made him an icon for the larger counterculture generation,[7][8] and he was a high-profile figure of racial pride for African Americans during the civil rights movement.[5][9] As a Muslim, Ali was initially affiliated with Elijah Muhammad's Nation of Islam (NOI). He later disavowed the NOI, adhering to Sunni Islam, and supporting racial integration like his former mentor Malcolm X.
Ali was a leading heavyweight boxer of the 20th century, and he remains the only three-time lineal champion of that division. His joint records of beating 21 boxers for the world heavyweight title and winning 14 unified title bouts stood for 35 years.[10][11][note 1] Ali is the only boxer to be named the Ring magazine Fighter of the Year six times. He has been ranked the greatest heavyweight boxer of all time,[12] and as the greatest athlete of the 20th century by Sports Illustrated, the Sports Personality of the Century by the BBC, and the third greatest athlete of the 20th century by ESPN SportsCentury.[13][14] He was involved in several historic boxing matches and feuds, most notably his fights with Joe Frazier, such as the Thrilla in Manila, and his fight with George Foreman known as The Rumble in the Jungle which has been called "arguably the greatest sporting event of the 20th century"[15][16] and was watched by a record estimated television audience of 1 billion viewers worldwide,[17][18] becoming the world's most-watched live television broadcast at the time. Ali thrived in the spotlight at a time when many fighters let their managers do the talking, and he was often provocative and outlandish.[19][20][21] He was famous for trash-talking, and often free-styled with rhyme schemes and spoken word poetry, anticipating elements of hip hop.[22][23][24]
Ali was arguably the most famous and documented human of the 20th century. Ali was known to be a very generous person who loved attention, as well as making other people happy. He never rejected an autograph, as he remembered how he'd felt as a youth when he was denied an autograph from his boxing idol, Sugar Ray Robinson; he would sometimes spend hours meeting people and signing autographs.[25] Ali also attained success as a musician, receiving two Grammy award nominations.[24] He was an ocassional actor, and a writer who released two autobiographies. Ali retired from boxing in 1981, and focused on religion, helping people by donating millions to charities and marching for people's rights to raise awareness for issues, in the U.S. and elsewhere. In 1984, he made public his diagnosis of Parkinson's disease, which some reports attribute to boxing-related injuries,[26] though he and his specialist physicians disputed this.[27] He remained an active public figure globally, but in his later years made increasingly limited public appearances as his condition worsened, and he was cared for by his family.
'''


def create_freq(text_string) -> dict:
   
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable


def _score_sentences(sentences, freqTable) -> dict:
   
    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        word_count_in_sentence_except_stop_words = 0
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                word_count_in_sentence_except_stop_words += 1
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        if sentence[:10] in sentenceValue:
            sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] / word_count_in_sentence_except_stop_words

        

    return sentenceValue


def _find_average_score(sentenceValue) -> int:
    
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = (sumValues / len(sentenceValue))

    return average


def _generate_summary(sentences, sentenceValue, threshold):
    count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
            summary += " " + sentence
            count += 1

    return summary


def run_summarization(text):
    # 1 Create the word frequency table
    freq_table = create_freq(text)

    # 2 Tokenize the sentences
    sentences = sent_tokenize(text)

    # 3 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(sentences, freq_table)

    # 4 Find the threshold
    threshold = _find_average_score(sentence_scores)

    # 5 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1.3 * threshold)

    return summary


if __name__ == '__main__':
    result = run_summarization(text)
    print(result)

text_file = open("summary.txt", "w")
n = text_file.write(result)
text_file.close()


# In[ ]:




