from nltk.stem import PorterStemmer

#define vocabulary to build a simple text classifier
words_book = ['book', 'reserv', 'schedul']
words_cancel = ['cancel', 'remov','repeal']
words_webcheckin = ['webcheckin','web','check','checkin']

def stem_word(word):
    """
    Function to stem a given word
    :param word: string word
    :return: string stemmed_word
    """
    ps = PorterStemmer()
    return ps.stem(word)

def classify_text(text):
    """
    classify given text as book,cancel,webcheckin,feedback
    :param text:
    :return:
    """

    words = text.split()
    stemmed_words = []
    for word in words:
        stemmed_words.append(stem_word(word=word))

    for stemmed_word in stemmed_words:
        if stemmed_word in words_book:
            return 'book'
        elif stemmed_word in words_cancel:
            return 'cancel'
        elif stemmed_word in words_webcheckin:
            return 'webcheckin'

    return 'feedback'