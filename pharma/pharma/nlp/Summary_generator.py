import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

TOP_N = 5


# Data input
def read_article(text):
    sentences = []
    # text_in_unicode = csv_source_to_text_input(row, input_dataframe, column)
    text_in_unicode = u'Darmerkrankungen – Von harmlos bis lebensbedrohlich Fast jeder von uns leidet in seinem Leben einmal an einer Darmerkrankung. Bei den meisten von uns geht sie einfach vorüber, während andere ihr Leben lang damit zu kämpfen haben. Welche Darmerkrankungen es gibt, was die Symptome sind und wie ernst sie sein können, erfahren Sie hier. Es gibt viele verschiedene Formen von Darmerkrankungen. Einige verlaufen akut, andere chronisch, das heißt ein Leben lang. Akute Darmerkrankungen chronischen Darmerkrankungen Welche chronischen Darmerkrankungen gibt es?. Reizdarm Syndrom Dies ist eine recht häufige Funktionsstörung des Darms, ohne dass eine körperliche Ursache erkennbar ist. Frauen sind von dieser Darmerkrankung etwa doppelt so häufig betroffen wie Männer. Chronisch-entzündliche Darmerkrankungen (CED)Unter den Oberbegriff chronisch-entzündliche Darmerkrankungen fallen 2 verschiedene Krankheitsbilder: Morbus Crohn Colitis Was sind die Symptome chronischer Darmerkrankungen?. Die chronischen Darmerkrankungen haben auf den ersten Blick ähnliche Symptome, die aber unterschiedlich verlaufen und verschieden stark ausgeprägt sind. Reizdarmsyndrom Wiederkehrende Bauchschmerzen Durchfall Verstopfung Blähungen Völlegefühl Die Ursachen für das Reizdarmsyndrom sind bisher weitestgehend ungeklärt. Der Darm ist besonders empfindlich und die Darmbewegungen sind gestört. Bestimmte Nahrungsmittel, psychische Belastungen und Infektionen können deshalb leicht die typischen Symptome auslösen. Chronisch-entzündliche Darmerkrankungen Noch ist nicht viel über die Ursachen chronisch-entzündlicher Darmerkrankungen bekannt. Bei Morbus Crohn konnte eine genetische Veranlagung nachgewiesen werden. Sowohl hier als auch bei Colitis Ulcerosa wird außerdem eine Autoimmunreaktion vermutet, durch die sich das Abwehrsystem im Darm gegen körpereigene Substanzen richtet. Die weitere Erforschung der Ursachen ist eine wichtige Aufgabe der Wissenschaftler. Bauchschmerzen Durchfälle, teils blutig oder schleimig Ungewollter Gewichtsverlust Schwäche und Abgeschlagenheit Symptome außerhalb des Verdauungstraktes: Gelenkschmerzen und entzündliche Hautveränderungen Komplikationen: Verletzungen der Darmwand, Verengung oder Verschluss des Darms, erhöhtes Darmkrebsrisiko, Nährstoffmangel durch häufige Durchfälle Die Ursachen für chronisch-entzündliche Darmerkrankungen konnten bis heute nicht geklärt werden. “Die chronisch-entzündlichen Darmerkrankungen Morbus Crohn und Colitis ulcerosa sind von wiederkehrenden Krankheitsschüben geprägt. Die beschwerdefreien Zeiten zwischen den Schüben werden Remission genannt. Die Häufigkeit und Intensität dieser Schübe unterscheidet sich bei jedem Betroffenen. Wie werden Darmerkrankungen diagnostiziert?. Haben Sie länger als 3 Tage Durchfall oder kommt Fieber hinzu, sollten Sie einen Gastroenterologen aufsuchen. Dieser untersucht dann, ob und an welcher Darmerkrankung Sie leiden. Dafür hat er verschiedene Möglichkeiten: Befragung nach Symptomen Abtasten des Bauches auf Verhärtungen und Druckschmerz Ultraschall, Darmspiegelung, Magnetresonanztomographie (MRT), CT (Computertomographie): Anhand des Ortes der Entzündung lässt sich eventuell unterscheiden, ob es sich um Morbus Crohn oder Colitis ulcerosa handelt. Außerdem werden Komplikationen, wie eine Verletzung der Darmwand sichtbar Untersuchung von Blut und Stuhl auf Krankheitserreger Test auf Nahrungsmittelunverträglichkeiten oder – Allergien Wie können Darmerkrankungen behandelt werden?. Sowohl die chronisch-entzündlichen Darmerkrankungen, als auch das Reizdarmsyndrom sind bislang nicht heilbar. Durch die richtige Behandlung können aber die Beschwerden gelindert und damit die Lebensqualität deutlich erhöht werden. Dafür gibt es verschiedene Medikamente, die den Betroffen helfen: Schmerz- und krampflösende Medikamente Entzündungshemmung, häufig durch Kortison Immunsuppressiva, die das Immunsystem dämpfen und damit die Entzündung lindern Dauerbehandlung von CED, um die Remission zu verlängern: Bestimmte Medikamente, die das überaktive Immunsystem regulieren Bei bestimmten Komplikationen ist eine Operation erforderlich. Zum Beispiel können ein Darmverschluss oder eine starke Blutung des Darms tödlich enden, wenn sie nicht rechtzeitig operativ behandelt werden. In ausgeprägten Erkrankungsfällen kann auch die Entfernung des betroffenen Darmabschnitts notwendig sein. Was kann man selbst gegen Darmerkrankungen tun?Ein gesunder Lebensstil schützt den Darm. Er ist zwar kein Allheilmittel gegen chronische Darmerkrankungen, lindert jedoch die Symptome und beugt neuen Schüben vor. Eine gesunde, ausgewogene Ernährung Essen Sie regelmäßig kleinere Portionen, statt weniger großer. Trinken Sie ausreichend! Ein gesunder Mensch sollte etwa 2 Liter pro Tag trinken. Am gesündesten sind Wasser und ungesüßter Tee. Stilles Wasser belastet den Darm weniger als kohlensäurehaltiges. Verzichten Sie auf Nikotin und trinken Sie möglichst wenig Alkohol und Koffein. Bewegung regt den Stoffwechsel und die Darmtätigkeit an. Schon ein täglicher Spaziergang trägt dazu bei. Versuchen Sie psychische Belastungen und Stresssituationen zu vermeiden und finden Sie einen Ausgleich, wie z. B. autogenes Training. Quellenangaben Kompetenzcenter Darmerkrankungen (2017). Darmerkrankungen: Chronisch oder temporär?. Dr. med. Arne Schäffler, Dr. Bernadette Andre-Wallis (2016). Chronisch-entzündliche Darmerkrankungen Apothekenumschau (2014). Reizdarmsyndrom.'
    text = str(text)
    text_for_processing = [text]
    text_for_processing = text_for_processing[0].split(". ")

    for sentence in text_for_processing:
        # print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z0-9äöüÄÖÜß]", " ").split(" "))

    sentences.pop()
    return sentences


def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []

    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1

    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1

    return 1 - cosine_distance(vector1, vector2)


def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:  # ignore if both are same sentences
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix


def generate_summary(text_input):
    stop_words = stopwords.words('german')
    summarize_text = []

    # Step 1 - Read text anc split it
    sentences = read_article(text=text_input)

    # Step 2 - Generate Similary Martix across sentences
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)

    # Step 3 - Rank sentences in similarity martix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph, max_iter=600)

    # Step 4 - Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    # print("Indexes of top ranked_sentence order are ", ranked_sentence[TOP_N][1])
    # OUT OF RANGE
    # print("Lengt of top ranked_sentence: ", len(ranked_sentence))
    if len(ranked_sentence) > 5:
        counter_over_ranked_sentence = TOP_N
    else:
        counter_over_ranked_sentence = len(ranked_sentence)

    for i in range(counter_over_ranked_sentence):
        summarize_text.append(" ".join(ranked_sentence[i][1]))

    summarize_text = '. '.join(summarize_text)

    return summarize_text


if __name__ == '__main__':
    text_input = u'Darmerkrankungen – Von harmlos bis lebensbedrohlich Fast jeder von uns leidet in seinem Leben einmal an einer Darmerkrankung. Bei den meisten von uns geht sie einfach vorüber, während andere ihr Leben lang damit zu kämpfen haben. Welche Darmerkrankungen es gibt, was die Symptome sind und wie ernst sie sein können, erfahren Sie hier. Es gibt viele verschiedene Formen von Darmerkrankungen. Einige verlaufen akut, andere chronisch, das heißt ein Leben lang. Akute Darmerkrankungen chronischen Darmerkrankungen Welche chronischen Darmerkrankungen gibt es?. Reizdarm Syndrom Dies ist eine recht häufige Funktionsstörung des Darms, ohne dass eine körperliche Ursache erkennbar ist. Frauen sind von dieser Darmerkrankung etwa doppelt so häufig betroffen wie Männer. Chronisch-entzündliche Darmerkrankungen (CED)Unter den Oberbegriff chronisch-entzündliche Darmerkrankungen fallen 2 verschiedene Krankheitsbilder: Morbus Crohn Colitis Was sind die Symptome chronischer Darmerkrankungen?. Die chronischen Darmerkrankungen haben auf den ersten Blick ähnliche Symptome, die aber unterschiedlich verlaufen und verschieden stark ausgeprägt sind. Reizdarmsyndrom Wiederkehrende Bauchschmerzen Durchfall Verstopfung Blähungen Völlegefühl Die Ursachen für das Reizdarmsyndrom sind bisher weitestgehend ungeklärt. Der Darm ist besonders empfindlich und die Darmbewegungen sind gestört. Bestimmte Nahrungsmittel, psychische Belastungen und Infektionen können deshalb leicht die typischen Symptome auslösen. Chronisch-entzündliche Darmerkrankungen Noch ist nicht viel über die Ursachen chronisch-entzündlicher Darmerkrankungen bekannt. Bei Morbus Crohn konnte eine genetische Veranlagung nachgewiesen werden. Sowohl hier als auch bei Colitis Ulcerosa wird außerdem eine Autoimmunreaktion vermutet, durch die sich das Abwehrsystem im Darm gegen körpereigene Substanzen richtet. Die weitere Erforschung der Ursachen ist eine wichtige Aufgabe der Wissenschaftler. Bauchschmerzen Durchfälle, teils blutig oder schleimig Ungewollter Gewichtsverlust Schwäche und Abgeschlagenheit Symptome außerhalb des Verdauungstraktes: Gelenkschmerzen und entzündliche Hautveränderungen Komplikationen: Verletzungen der Darmwand, Verengung oder Verschluss des Darms, erhöhtes Darmkrebsrisiko, Nährstoffmangel durch häufige Durchfälle Die Ursachen für chronisch-entzündliche Darmerkrankungen konnten bis heute nicht geklärt werden. “Die chronisch-entzündlichen Darmerkrankungen Morbus Crohn und Colitis ulcerosa sind von wiederkehrenden Krankheitsschüben geprägt. Die beschwerdefreien Zeiten zwischen den Schüben werden Remission genannt. Die Häufigkeit und Intensität dieser Schübe unterscheidet sich bei jedem Betroffenen. Wie werden Darmerkrankungen diagnostiziert?. Haben Sie länger als 3 Tage Durchfall oder kommt Fieber hinzu, sollten Sie einen Gastroenterologen aufsuchen. Dieser untersucht dann, ob und an welcher Darmerkrankung Sie leiden. Dafür hat er verschiedene Möglichkeiten: Befragung nach Symptomen Abtasten des Bauches auf Verhärtungen und Druckschmerz Ultraschall, Darmspiegelung, Magnetresonanztomographie (MRT), CT (Computertomographie): Anhand des Ortes der Entzündung lässt sich eventuell unterscheiden, ob es sich um Morbus Crohn oder Colitis ulcerosa handelt. Außerdem werden Komplikationen, wie eine Verletzung der Darmwand sichtbar Untersuchung von Blut und Stuhl auf Krankheitserreger Test auf Nahrungsmittelunverträglichkeiten oder – Allergien Wie können Darmerkrankungen behandelt werden?. Sowohl die chronisch-entzündlichen Darmerkrankungen, als auch das Reizdarmsyndrom sind bislang nicht heilbar. Durch die richtige Behandlung können aber die Beschwerden gelindert und damit die Lebensqualität deutlich erhöht werden. Dafür gibt es verschiedene Medikamente, die den Betroffen helfen: Schmerz- und krampflösende Medikamente Entzündungshemmung, häufig durch Kortison Immunsuppressiva, die das Immunsystem dämpfen und damit die Entzündung lindern Dauerbehandlung von CED, um die Remission zu verlängern: Bestimmte Medikamente, die das überaktive Immunsystem regulieren Bei bestimmten Komplikationen ist eine Operation erforderlich. Zum Beispiel können ein Darmverschluss oder eine starke Blutung des Darms tödlich enden, wenn sie nicht rechtzeitig operativ behandelt werden. In ausgeprägten Erkrankungsfällen kann auch die Entfernung des betroffenen Darmabschnitts notwendig sein. Was kann man selbst gegen Darmerkrankungen tun?Ein gesunder Lebensstil schützt den Darm. Er ist zwar kein Allheilmittel gegen chronische Darmerkrankungen, lindert jedoch die Symptome und beugt neuen Schüben vor. Eine gesunde, ausgewogene Ernährung Essen Sie regelmäßig kleinere Portionen, statt weniger großer. Trinken Sie ausreichend! Ein gesunder Mensch sollte etwa 2 Liter pro Tag trinken. Am gesündesten sind Wasser und ungesüßter Tee. Stilles Wasser belastet den Darm weniger als kohlensäurehaltiges. Verzichten Sie auf Nikotin und trinken Sie möglichst wenig Alkohol und Koffein. Bewegung regt den Stoffwechsel und die Darmtätigkeit an. Schon ein täglicher Spaziergang trägt dazu bei. Versuchen Sie psychische Belastungen und Stresssituationen zu vermeiden und finden Sie einen Ausgleich, wie z. B. autogenes Training. Quellenangaben Kompetenzcenter Darmerkrankungen (2017). Darmerkrankungen: Chronisch oder temporär?. Dr. med. Arne Schäffler, Dr. Bernadette Andre-Wallis (2016). Chronisch-entzündliche Darmerkrankungen Apothekenumschau (2014). Reizdarmsyndrom.'
    summary_out = generate_summary(text_input)
    print(summary_out)
