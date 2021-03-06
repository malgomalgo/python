import string, os
import matplotlib.pyplot as plt
import json

print(r"""

                _   _                      _   
               | | (_)                    | |  
 ___  ___ _ __ | |_ _ _ __ ___   ___ _ __ | |_ 
/ __|/ _ \ '_ \| __| | '_ ` _ \ / _ \ '_ \| __|
\__ \  __/ | | | |_| | | | | | |  __/ | | | |_ 
|___/\___|_| |_|\__|_|_| |_| |_|\___|_| |_|\__|


                   _           _     
                  | |         (_)    
  __ _ _ __   __ _| |_   _ ___ _ ___ 
 / _` | '_ \ / _` | | | | / __| / __|
| (_| | | | | (_| | | |_| \__ \ \__ \
 \__,_|_| |_|\__,_|_|\__, |___/_|___/
                      __/ |          
                     |___/           """)
print("\n===================================================================")


def main():
    #WCZYTANIE JSONOW I PLIKU
    neg, pos = read_sentiments()
    print("Please provide path to the text file you wish to analyze: ")
    user_file_path = input()
    if not os.path.exists(user_file_path):
        raise FileNotFoundError
    f = open(user_file_path, 'r')
    #ANALIZA PLIKU UZYTKOWNIA
    clean_final_text = clean(f.read())
    f.close()
    result, present_positives, present_negatives = count_sentiments(clean_final_text, pos, neg)
    op = opinion(result)
    #WYNIKI
    print("===================================================================")
    print("Value of your text equals:", result, "and the opinion is:", op)
    stats(present_negatives, "negative")
    stats(present_positives, "positive")
    grids(present_positives, present_negatives)


def read_sentiments():
    f = open("negative.json",)
    neg = json.load(f)
    f.close()

    f = open("positive.json",)
    pos = json.load(f)
    f.close()

    return neg, pos


def clean(text):
    lower_case = text.lower()
    clean_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    tokenized_text = clean_text.split()
    stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves",
              "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
              "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
              "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
              "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about",
              "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up",
              "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when",
              "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor",
              "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    text = []
    for word in tokenized_text:
        if word not in stop_words:
            text.append(word)
    return text


def count_sentiments(text, pos, neg):
    result = 0
    p = []
    n = []
    for word in text:
        if word in pos:
            result = result + 1
            p.append(word)
        elif word in neg:
            result = result - 1
            n.append(word)
    return result, p, n


def opinion(result):
    opinion = None
    if result > 0:
        opinion = "positive"
    elif result < 0:
        opinion = "negative"
    else:
        opinion = "neutral"
    return opinion


def stats(presents, presents_type):
    print("===================================================================")
    print("The most common", presents_type, "word is:", max(set(presents), key=presents.count))
    print("The shortest", presents_type, "word is:", min(presents, key=len))
    print("The longest", presents_type, "word is:", max(presents, key=len))
    print("===================================================================")


def grids(present_positives, present_negatives):
    plt.subplot(121)
    plt.bar(["positives", "negatives"], [len(present_positives), len(present_negatives)], width=0.2, color=("green","red"))
    plt.title("amount of positive and negative words in a given text")
    plt.ylabel("amount")
    plt.minorticks_on
    plt.grid(True)

    plt.subplot(122)
    sizes = [len(present_positives), len(present_negatives)]
    explode = [0.1, 0]
    plt.pie(sizes, explode=explode, labels=["positives", "negatives"], autopct='%1.1f%%', shadow=True,colors=("green","red"))
    plt.title("percentage of positive and negative words in a given text")
    plt.savefig("graph_analysis.png")


main()
print("bye :)")



# (1 pkt) Powinien wczyta?? tekst do zanalizowania
# (2 pkt) Powinien wczyta?? tekst s????w pozytywnych i negatywnych dla danego j??zyka
# (3 pkt) Powinien dokona?? badania opinii metod?? statystyczn?? danego tekstu
# (3 pkt) Powinien mie?? mo??liwo???? ponownej analizy tekstu z u??yciem zb??dnych s????w (stoplisty)
# (5 pkt) Powinien wy??wietli?? statystyczne dane: najcz??stsze pozytywne/negatywne s??owa, procent pozytywnych/negatywnych s????w i inne w tek??cie poprzedzone odpowiednimi wykresami. Im czytelniejsze wykresy tym wi??ksza ilo???? punkt??w
# (4 pkt) Powinien dokona?? badania opinii w oparciu o s??owa kluczowe danego tekstu (imiona bohater??w, miejscowo??ci i inne)
# Pod ocen?? b??d?? brane nast??puj??ce elementy:
# (1 pkt) Poprawne uruchomienie programu.
# (18 pkt) Zastosowanie powy??szych wymaga??
# (1 pkt) ??adne i estetyczne menu programu :-)
# (1 pkt) Zastosowanie formatu JSON
# (1 pkt) Mo??liwo???? zapisu analizy tekstu dokonany w programie (liczba otrzymana w wyniku metody + wykresy najcz????ciej wyst??puj??cych pozytywnych/negatywnych s????w)
# (2 pkt) Mo??liwo???? por??wnania dw??ch tekst??w t?? sam?? metod??. Teksty powinny by?? odpowiednio du??e na przyk??ad wiersze/powie??ci.
# (4 pkt) Styl kodu (poprawno???? nazw, podzia?? kodu na funkcje)
# Dodatkowo b??d?? brane nast??puj??ce rzeczy:
# (1 pkt) Mo??liwo???? pobierania i analizowania tekst??w z sieci
# (1 pkt) Umieszczenie rozwi??zania w repozytorium github.com
# (1 pkt) Wykonanie test??w jednostkowych
# (max 2 pkt) U??ywanie rzeczy nie pokazywanych na zaj??ciach