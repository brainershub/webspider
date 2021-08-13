
# Installing required libraries
# sudo apt-get install python-pip
# sudo pip install -U nltk
# python
# >>> import nltk
# >>> nltk.download('stopwords')
# >>> nltk.download('punkt')
# >>> exit()

import sys
import codecs
import nltk
import pandas as pd
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords

NUM_MOST_COMMON_WORDS = 350


def get_frequency_distribution(input_text):
    # NLTK's default German stopwords
    # default_stopwords = set(nltk.corpus.stopwords.words('german'))

    # We're adding some on our own - could be done inline like this...
    # custom_stopwords = set((u'–', u'dass', u'mehr'))
    # ... but let's read them from a file instead (one stopword per line, UTF-8)
    # stopwords_file = './stopwords.txt'
    # custom_stopwords = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())

    # all_stopwords = default_stopwords | custom_stopwords
    german_stopwords = set(nltk.corpus.stopwords.words('german'))
    english_stopwords = set(nltk.corpus.stopwords.words('english'))
    all_stopwords = german_stopwords | english_stopwords

    #input_file = 'msft.txt'

    # fp = codecs.open(input_file, 'r', 'utf-8')

    # words = nltk.word_tokenize(fp.read())
    words = nltk.word_tokenize(input_text)

    # Remove single-character tokens (mostly punctuation)
    words = [word for word in words if len(word) > 1]

    # Remove numbers
    words = [word for word in words if not word.isnumeric()]

    # Lowercase all words (default_stopwords are lowercase too)
    words = [word.lower() for word in words]

    # Stemming words seems to make matters worse, disabled
    #stemmer = nltk.stem.snowball.SnowballStemmer('german')
    #words = [stemmer.stem(word) for word in words]

    # Remove stopwords
    words = [word for word in words if word not in all_stopwords]

    # Calculate frequency distribution
    frq_dist = nltk.FreqDist(words)
    #print("original word frequency distribution: ", len(frq_dist))


    if len(frq_dist) <= NUM_MOST_COMMON_WORDS:
        return frq_dist, len(frq_dist)
        #NUM_MOST_COMMON_WORDS = len(frq_dist)
        #print("NUM_MOST_COMMON_WORDS", NUM_MOST_COMMON_WORDS)

    else:
        return frq_dist, NUM_MOST_COMMON_WORDS


def get_word_frequency(frequency_distribution, num_of_words):
    # Output top 50 words
    word_list = []
    word_freqency_list = []

    for word, frequency in frequency_distribution.most_common(num_of_words):
        word_list.append(word)
        word_freqency_list.append(frequency)

    word_list_df = pd.DataFrame(word_list, columns=['words'])
    word_freqency_list_df = pd.DataFrame(word_freqency_list, columns=['word frequency'])

    word_df_combined = pd.concat([word_list_df, word_freqency_list_df], axis=1, sort=False)
    return word_df_combined


def word_frequency_dfs_to_json(word_freq_dfs_comb_df):
    word_freq_dfs_comb_df.to_json('results/word_frequency_results_json/word_frequency_result.json', orient='columns')
    word_freq_dfs_comb_df.to_csv('results/word_frequency_results_json/results_table_word_frequency.csv', encoding='utf-8', index=False)


def genarate_word_count(input_text):

    frequency_distribution_of_txt, num_of_words  = get_frequency_distribution(input_text=input_text)
    word_freq_df = get_word_frequency(frequency_distribution=frequency_distribution_of_txt, num_of_words=num_of_words)
    #print("num_of_words counted: ",num_of_words)
    word_freq_df.set_index('words')

    #print(word_freq_df.head())

    word_freq_df = word_freq_df.to_dict(orient='list')


    return word_freq_df


if __name__ == '__main__':
    #input_text = "Chronisch-entzündliche Darmerkrankungen Noch ist nicht viel über die Ursachen chronisch-entzündlicher Darmerkrankungen bekannt. Chronisch-entzündliche Darmerkrankungen (CED)Unter den Oberbegriff chronisch-entzündliche Darmerkrankungen fallen 2 verschiedene Krankheitsbilder: Morbus Crohn Colitis Was sind die Symptome chronischer Darmerkrankungen?. Akute Darmerkrankungen chronischen Darmerkrankungen Welche chronischen Darmerkrankungen gibt es?. Wie werden Darmerkrankungen diagnostiziert?. Was kann man selbst gegen Darmerkrankungen tun?Ein gesunder Lebensstil schützt den Darm"
    input_text = "As we mark the 1-year anniversary of the declaration by the World Health Organization (WHO) of COVID-19 as a global pandemic, the world has suffered a staggering and tragic human toll. During this dark time, the scientific community has been called to rise to the occasion in unprecedented ways. The intensity of the work and the sense of urgency have been unremitting and exhausting. As we sort out the triumphs and frustrations, we can begin to reflect on what we have learned. The rapid development of vaccines has been breathtaking. Moving at least five times faster than ever before, the design, development, rigorous testing, and manufacture of multiple vaccines using different platforms have been astoundingly successful. This was only possible because of decades of investment in the long arc of technology development\u2014working out the details of a messenger RNA strategy, for instance, was a 25-year journey. To prepare for future pandemics, we must extrapolate this lesson to the most likely pathogens lurking in the future. We should also learn from the experience of vaccine trial recruitment, where special efforts like the U.S. National Institutes of Health (NIH) Community Engagement Alliance (CEAL) were needed to reach out to communities of color, where the disease has taken its highest toll in the United States. Diversity in clinical trial enrollment is not just a nice idea\u2014it is essential if the results are going to be meaningful to all groups. Therapeutics that have proven beneficial for COVID-19 include an antiviral (remdesivir), immunosuppressives (dexamethasone, baracitinib), several outpatient monoclonal antibodies, and anticoagulants. Important contributions were made by the Randomised Evaluation of COVID-19 Therapy (RECOVERY) trial in the United Kingdom and the Solidarity Trial sponsored by WHO. In the United States, a public-private partnership, Accelerating COVID-19 Therapeutic Interventions and Vaccines (ACTIV), brought together government agencies, academics, and 20 pharmaceutical companies, ably managed by the Foundation for the NIH. With a priority on therapeutic agents, ACTIV designed master protocols and coordinated rigorous, well-powered randomized controlled trials. Operation Warp Speed, a public-private partnership initiated by the U.S. government, provided billions of dollars for trial operation and at-risk manufacturing. One lesson learned, however, was that many clinical trials in the United States were not initially well suited to a public health emergency. Far too many small and poorly designed trials (many focused on hydroxychloroquine, which turned out to be a dead end) were initiated in the early days of the pandemic\u2014all with good intentions but contributing relatively little in terms of new knowledge. Another lesson is that the necessary short-term dependence on repurposing existing drugs will not often produce true successful outcomes. For the future, we should begin to work on potent oral antivirals against all major classes of potential pathogens, with the goal of having drugs ready for phase 2/3 efficacy trials when the next threat emerges. Another major challenge was the need for fast, widely accessible, and highly accurate virus testing. For all their merits, the first-arriving nucleic acid tests, which generally had to be conducted in central labs, took too long to produce the rapid results urgently needed to prevent spread. This inspired an innovative response\u2014the NIH Rapid Acceleration of Diagnostics (RADx) program in which test developers drew on a \u201cshark tank\u201d of engineering, business, and manufacturing experts. From over 700 applications, 137 went through an intense evaluation, and those judged most promising were provided with additional resources. As a result, today there are 28 novel diagnostic platforms collectively contributing an additional 2.5 million tests daily. An analysis of the potential benefits of widespread home testing is about to get under way. This approach, whereby NIH took on the role of venture capitalist, should be considered in the future when rapid development of new technologies is the goal. In the past, the world has rallied to confront new pandemics, only to lapse into complacency as the risk faded. Having now experienced the worst pandemic in 103 years, we must not make that mistake again."
    word_frq = genarate_word_count(input_text)
    print(word_frq)
    # {'words': ['darmerkrankungen', 'chronisch-entzündliche'], 'word frequency': [10, 3]}
