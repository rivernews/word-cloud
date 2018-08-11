from wordcloud import WordCloud
'''
Customize Doc: https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html
'''

import csv
import matplotlib.pyplot as plt

import datetime

def get_freq_dict_from_csv(filename, row_amount=None):
    print('get frequency dictionary from csv...')
    with open(filename, 'r') as file:
        sample = file.read(1024)
        dialect = csv.Sniffer().sniff(sample)
        
        file.seek(0)
        if not row_amount or row_amount < 0:
            reader = csv.reader(file.readlines()[1:], dialect)
        else:
            reader = csv.reader(file.readlines()[1:row_amount], dialect)

        d = {}
        err = []
        line_pointer = 0
        
        for index, x in enumerate(reader):
            try:
                line_pointer = index + 2
                if len(x) != 2:
                    err.append({
                        'context': 'in function get_freq_dict_from_csv, file {}'.format(filename),
                        'line': line_pointer,
                        'context': x,
                        'err_msg': 'csv parsed more than 2 values in a line'
                    })
                    continue
                    # raise Exception
                v, k = x
                d.update( { k:int(v) } )
            except Exception as e:
                print('get freq dict from csv failed at line {} in file {}. Line is {}'.format(line_pointer, filename, x))
                print(repr(e))
                err.append({
                    'context': 'in function get_freq_dict_from_csv, file {}'.format(filename),
                    'line': line_pointer,
                    'context': x,
                    'err_msg': repr(e),
                })
        
        return [d, err]

def write_csv_file(d):
    print('writing to csv...')
    with open("output", "w") as file:
        for k, v in d.items():
            file.write("{} {}\n".format( v,k ))

def generate_word_cloud(d=None):
    wordcloud = None

    print("generating word cloud image...")
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

def pre_processing_file(filename):
    print('preprocessing file {} into csv...'.format(filename))
    with open(filename, "r") as input_file, open('processed_' + filename, 'w') as output_file:
        output_file.write('Count,Word\n')
        for index, line in enumerate(input_file.readlines()[1:]):
            line_number = index + 2 # base 0 index && csv 1st line is field header
            try:
                tokens = line.replace('\n', '').split(maxsplit=1)
                if len(tokens) < 2:
                    count, word = [0, '']
                else:
                    count, word = tokens
                output_file.write('{},{}\n'.format(count, word) )
            except Exception as e:
                print('error while preprocessing for line {} in file {} '.format(line_number, filename) , repr(e))
                return False
    return True

def err_end():
    print('some error. end program')    

if __name__ == "__main__":
    all_err = []
    if pre_processing_file('eng_pairs'):
        d, err = get_freq_dict_from_csv('processed_eng_pairs', row_amount=-1)
        all_err += err
        if d:
            print(d)
            # generate_word_cloud(d)
        else:
            err_end()
    else:
        err_end()
    
    # print('errors summary....')
