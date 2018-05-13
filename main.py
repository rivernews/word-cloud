from wordcloud import WordCloud
'''
Customize Doc: https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html
'''

import csv
import matplotlib.pyplot as plt

import datetime

def get_freq_dict_from_csv(filename, row_amount=None):
    if row_amount:
        reader = csv.reader(open(filename, 'r',newline='\n').readlines()[1:row_amount])
    else:
        reader = csv.reader(open(filename, 'r',newline='\n').readlines()[1:])
    d = {}
    for v, k in reader:
        d.update( { k:int(v) } )
    return d

def write_csv_file(d):
    with open("output", "w") as file:
        for k, v in d.items():
            file.write("{} {}\n".format( v,k ))

def generate_word_cloud(d=None):
    wordcloud = None

    if d:
        wordcloud = WordCloud(
            font_path='/Library/Fonts/Arial Unicode.ttf',
            background_color='white',
            scale=5,
            relative_scaling=0.5,
            width=1270,height=900, max_words=1628,normalize_plurals=False).generate_from_frequencies(d)
    
    if wordcloud:
        plt.figure( figsize=(20,10), dpi=400)
        plt.tight_layout(pad=0)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig("wordcloud - {}.png".format(datetime.datetime.now()), bbox_inches='tight')
        # plt.show()

if __name__ == "__main__":
    d = get_freq_dict_from_csv('cleaned_csv')
    generate_word_cloud(d)
