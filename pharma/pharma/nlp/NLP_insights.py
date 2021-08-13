import pandas as pd
from .Summary_generator import generate_summary
from .Word_counter import genarate_word_count
from .Sentiment_analysis import generate_sentiments

class NLP_module():

    def __init__(self, input_text):
        # input data frame should be according to the CSV files in the data folder
        self.input_text = input_text
        self.summary = None
        self.word_count = None
        self.sentiments = None

    def get_summary(self):
        self.summary = generate_summary(self.input_text)
        return self.summary

    def get_word_count(self):
        self.word_count = genarate_word_count(self.input_text)
        return self.word_count

    def get_sentiments(self):
        self.sentiments = generate_sentiments(self.input_text)
        return self.sentiments


if __name__ == '__main__':

    text_input = u'Darmerkrankungen – Von harmlos bis lebensbedrohlich Fast jeder von uns leidet in seinem Leben einmal an einer Darmerkrankung. Bei den meisten von uns geht sie einfach vorüber, während andere ihr Leben lang damit zu kämpfen haben. Welche Darmerkrankungen es gibt, was die Symptome sind und wie ernst sie sein können, erfahren Sie hier. Es gibt viele verschiedene Formen von Darmerkrankungen. Einige verlaufen akut, andere chronisch, das heißt ein Leben lang. Akute Darmerkrankungen chronischen Darmerkrankungen Welche chronischen Darmerkrankungen gibt es?. Reizdarm Syndrom Dies ist eine recht häufige Funktionsstörung des Darms, ohne dass eine körperliche Ursache erkennbar ist. Frauen sind von dieser Darmerkrankung etwa doppelt so häufig betroffen wie Männer. Chronisch-entzündliche Darmerkrankungen (CED)Unter den Oberbegriff chronisch-entzündliche Darmerkrankungen fallen 2 verschiedene Krankheitsbilder: Morbus Crohn Colitis Was sind die Symptome chronischer Darmerkrankungen?. Die chronischen Darmerkrankungen haben auf den ersten Blick ähnliche Symptome, die aber unterschiedlich verlaufen und verschieden stark ausgeprägt sind. Reizdarmsyndrom Wiederkehrende Bauchschmerzen Durchfall Verstopfung Blähungen Völlegefühl Die Ursachen für das Reizdarmsyndrom sind bisher weitestgehend ungeklärt. Der Darm ist besonders empfindlich und die Darmbewegungen sind gestört. Bestimmte Nahrungsmittel, psychische Belastungen und Infektionen können deshalb leicht die typischen Symptome auslösen. Chronisch-entzündliche Darmerkrankungen Noch ist nicht viel über die Ursachen chronisch-entzündlicher Darmerkrankungen bekannt. Bei Morbus Crohn konnte eine genetische Veranlagung nachgewiesen werden. Sowohl hier als auch bei Colitis Ulcerosa wird außerdem eine Autoimmunreaktion vermutet, durch die sich das Abwehrsystem im Darm gegen körpereigene Substanzen richtet. Die weitere Erforschung der Ursachen ist eine wichtige Aufgabe der Wissenschaftler. Bauchschmerzen Durchfälle, teils blutig oder schleimig Ungewollter Gewichtsverlust Schwäche und Abgeschlagenheit Symptome außerhalb des Verdauungstraktes: Gelenkschmerzen und entzündliche Hautveränderungen Komplikationen: Verletzungen der Darmwand, Verengung oder Verschluss des Darms, erhöhtes Darmkrebsrisiko, Nährstoffmangel durch häufige Durchfälle Die Ursachen für chronisch-entzündliche Darmerkrankungen konnten bis heute nicht geklärt werden. “Die chronisch-entzündlichen Darmerkrankungen Morbus Crohn und Colitis ulcerosa sind von wiederkehrenden Krankheitsschüben geprägt. Die beschwerdefreien Zeiten zwischen den Schüben werden Remission genannt. Die Häufigkeit und Intensität dieser Schübe unterscheidet sich bei jedem Betroffenen. Wie werden Darmerkrankungen diagnostiziert?. Haben Sie länger als 3 Tage Durchfall oder kommt Fieber hinzu, sollten Sie einen Gastroenterologen aufsuchen. Dieser untersucht dann, ob und an welcher Darmerkrankung Sie leiden. Dafür hat er verschiedene Möglichkeiten: Befragung nach Symptomen Abtasten des Bauches auf Verhärtungen und Druckschmerz Ultraschall, Darmspiegelung, Magnetresonanztomographie (MRT), CT (Computertomographie): Anhand des Ortes der Entzündung lässt sich eventuell unterscheiden, ob es sich um Morbus Crohn oder Colitis ulcerosa handelt. Außerdem werden Komplikationen, wie eine Verletzung der Darmwand sichtbar Untersuchung von Blut und Stuhl auf Krankheitserreger Test auf Nahrungsmittelunverträglichkeiten oder – Allergien Wie können Darmerkrankungen behandelt werden?. Sowohl die chronisch-entzündlichen Darmerkrankungen, als auch das Reizdarmsyndrom sind bislang nicht heilbar. Durch die richtige Behandlung können aber die Beschwerden gelindert und damit die Lebensqualität deutlich erhöht werden. Dafür gibt es verschiedene Medikamente, die den Betroffen helfen: Schmerz- und krampflösende Medikamente Entzündungshemmung, häufig durch Kortison Immunsuppressiva, die das Immunsystem dämpfen und damit die Entzündung lindern Dauerbehandlung von CED, um die Remission zu verlängern: Bestimmte Medikamente, die das überaktive Immunsystem regulieren Bei bestimmten Komplikationen ist eine Operation erforderlich. Zum Beispiel können ein Darmverschluss oder eine starke Blutung des Darms tödlich enden, wenn sie nicht rechtzeitig operativ behandelt werden. In ausgeprägten Erkrankungsfällen kann auch die Entfernung des betroffenen Darmabschnitts notwendig sein. Was kann man selbst gegen Darmerkrankungen tun?Ein gesunder Lebensstil schützt den Darm. Er ist zwar kein Allheilmittel gegen chronische Darmerkrankungen, lindert jedoch die Symptome und beugt neuen Schüben vor. Eine gesunde, ausgewogene Ernährung Essen Sie regelmäßig kleinere Portionen, statt weniger großer. Trinken Sie ausreichend! Ein gesunder Mensch sollte etwa 2 Liter pro Tag trinken. Am gesündesten sind Wasser und ungesüßter Tee. Stilles Wasser belastet den Darm weniger als kohlensäurehaltiges. Verzichten Sie auf Nikotin und trinken Sie möglichst wenig Alkohol und Koffein. Bewegung regt den Stoffwechsel und die Darmtätigkeit an. Schon ein täglicher Spaziergang trägt dazu bei. Versuchen Sie psychische Belastungen und Stresssituationen zu vermeiden und finden Sie einen Ausgleich, wie z. B. autogenes Training. Quellenangaben Kompetenzcenter Darmerkrankungen (2017). Darmerkrankungen: Chronisch oder temporär?. Dr. med. Arne Schäffler, Dr. Bernadette Andre-Wallis (2016). Chronisch-entzündliche Darmerkrankungen Apothekenumschau (2014). Reizdarmsyndrom.'
    obj = NLP_module(text_input)
    summary = obj.get_summary()
    #print(summary)
    word_count = obj.get_word_count()
    #print(word_count)
    sentiments = obj.get_sentiments()
    #print(sentiments)
