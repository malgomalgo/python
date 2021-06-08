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



# (1 pkt) Powinien wczytać tekst do zanalizowania
# (2 pkt) Powinien wczytać tekst słów pozytywnych i negatywnych dla danego języka
# (3 pkt) Powinien dokonać badania opinii metodą statystyczną danego tekstu
# (3 pkt) Powinien mieć możliwość ponownej analizy tekstu z użyciem zbędnych słów (stoplisty)
# (5 pkt) Powinien wyświetlić statystyczne dane: najczęstsze pozytywne/negatywne słowa, procent pozytywnych/negatywnych słów i inne w tekście poprzedzone odpowiednimi wykresami. Im czytelniejsze wykresy tym większa ilość punktów
# (4 pkt) Powinien dokonać badania opinii w oparciu o słowa kluczowe danego tekstu (imiona bohaterów, miejscowości i inne)
# Pod ocenę będą brane następujące elementy:
# (1 pkt) Poprawne uruchomienie programu.
# (18 pkt) Zastosowanie powyższych wymagań
# (1 pkt) Ładne i estetyczne menu programu :-)
# (1 pkt) Zastosowanie formatu JSON
# (1 pkt) Możliwość zapisu analizy tekstu dokonany w programie (liczba otrzymana w wyniku metody + wykresy najczęściej występujących pozytywnych/negatywnych słów)
# (2 pkt) Możliwość porównania dwóch tekstów tą samą metodą. Teksty powinny być odpowiednio duże na przykład wiersze/powieści.
# (4 pkt) Styl kodu (poprawność nazw, podział kodu na funkcje)
# Dodatkowo będą brane następujące rzeczy:
# (1 pkt) Możliwość pobierania i analizowania tekstów z sieci
# (1 pkt) Umieszczenie rozwiązania w repozytorium github.com
# (1 pkt) Wykonanie testów jednostkowych
# (max 2 pkt) Używanie rzeczy nie pokazywanych na zajęciach