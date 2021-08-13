from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob_de import TextBlobDE

def sentiment_analysis_of_text(text_input):
    sid = SentimentIntensityAnalyzer()
    sentiment_matrix = sid.polarity_scores(text_input)
    sentiment_list = [str(k)+': '+str(v) for k, v in sentiment_matrix.items()]

    sentiment_list_out = str(sentiment_list).strip('[]')

    return sentiment_list_out




text = '''
"Ich hatte gerade einen wirklich schlechten Tag. Ich habe den Bus am Morgen verpasst. Ich war zu spät im Büro und der Chef war nicht glücklich über mich.

'''
"Chronisch-entzündliche Darmerkrankungen Noch ist nicht viel über die Ursachen chronisch-entzündlicher Darmerkrankungen bekannt. Chronisch-entzündliche Darmerkrankungen (CED)Unter den Oberbegriff chronisch-entzündliche Darmerkrankungen fallen 2 verschiedene Krankheitsbilder: Morbus Crohn Colitis Was sind die Symptome chronischer Darmerkrankungen?. Akute Darmerkrankungen chronischen Darmerkrankungen Welche chronischen Darmerkrankungen gibt es?. Wie werden Darmerkrankungen diagnostiziert?. Was kann man selbst gegen Darmerkrankungen tun?Ein gesunder Lebensstil schützt den Darm"

# Ich hatte gerade einen wirklich schlechten Tag. Ich habe den Bus am Morgen verpasst. Ich war zu spät im Büro und der Chef war nicht glücklich über mich.

def generate_sentiments(input_text):
    blob = TextBlobDE(input_text)

    sentiment_polarity = round((blob.sentiment.polarity), 2)
    sentiment_polarity = "{:.0%}".format(sentiment_polarity)

    subjectivity = blob.sentiment.subjectivity  # to make %
    subjectivity = "{:.0%}".format(subjectivity)

    objectivity = (1 - blob.sentiment.subjectivity)
    objectivity = "{:.0%}".format(objectivity)

    sentiment_results = {"Sentiment Polarity": sentiment_polarity, "objectivity": objectivity,
                         "subjectivity": subjectivity}
    '''
     The polarity score is a float within the range [-1.0, 1.0]. -1.0 is Negative and 1.0 Positive
     The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
    '''
    return sentiment_results


if __name__ == '__main__':
    input_text = "Chronisch-entzündliche Darmerkrankungen Noch ist nicht viel über die Ursachen chronisch-entzündlicher Darmerkrankungen bekannt. Chronisch-entzündliche Darmerkrankungen (CED)Unter den Oberbegriff chronisch-entzündliche Darmerkrankungen fallen 2 verschiedene Krankheitsbilder: Morbus Crohn Colitis Was sind die Symptome chronischer Darmerkrankungen?. Akute Darmerkrankungen chronischen Darmerkrankungen Welche chronischen Darmerkrankungen gibt es?. Wie werden Darmerkrankungen diagnostiziert?. Was kann man selbst gegen Darmerkrankungen tun?Ein gesunder Lebensstil schützt den Darm"
    sentiment = generate_sentiments(input_text)
    #print(sentiment)