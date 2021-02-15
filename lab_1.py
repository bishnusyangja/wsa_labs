# Author: Bishnu Bhattarai 078-08

import json
import os
from collections import Counter

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
             'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
             'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
             'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were',
             'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
             'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
             'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
             'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
             'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
             'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
             'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain',
             'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn',
             "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
             "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't",
             'wouldn', "wouldn't"]

trimming_words = ("'", "\"", "(", ")", "/", "\\", ".", ",")

path = os.path.dirname(__file__)
file_path = os.path.join(path, 'cran.all')
json_file = os.path.join(path, 'content.json')


def read_file_content():
    with open(file_path, 'r') as fp:
        content = fp.read()
    return content


def get_main_content(content):
    try:
        content = content.split('\n.W\n')
        title = content[0].split('\n')[0]
        content = content[1]
        title = f"doc_{title}"
    except Exception as exc:
        print(content)
        return None
    else:
        return {title: content}


def get_parsed_content(from_file=False):
    if from_file:
        with open(json_file, "r") as load_file:
            return json.load(load_file)

    content = read_file_content()
    content_list = content.split('\n.I ')
    content_list[0] = content_list[0].strip('.I ')

    item_list = []
    for content in content_list:
        item_dict = get_main_content(content)
        if item_dict is not None:
            item_list.append(item_dict)

    with open(json_file, "w") as dump_file:
        json.dump(item_list, dump_file)

    return item_list


def remove_stop_words(words):
    final_word = []
    for word in words:
        if word not in stopwords:
            final_word.append(word)
    return final_word


def remove_punctuation_character(tokens):
    after_trimming = []
    for item in tokens:
        for t in trimming_words:
            item = item.strip(t)
        after_trimming.append(item)
    return list(set(after_trimming))


def tokenize_content(content):
    all_words = []
    for docs in content:
        for k, v in docs.items():
            doc_content = v.split()
            after_removing_punctuation = remove_punctuation_character(doc_content)
            all_words.extend(after_removing_punctuation)
    return [item for item in all_words if item]


def print_top_ten_words(tokens):
    count_dict = Counter(tokens)
    total_tokens = len(tokens)
    count = 1
    sorted_dict = sorted(count_dict.items(), key=lambda i: i[1], reverse=True)
    print("Top ten words in ranking")
    count_sum = 0
    half_sum_accounting_words = 0

    for k, v in sorted_dict:
        if count_sum <= total_tokens / 2:
            count_sum += v
            half_sum_accounting_words = count

        if count <= 10:
            print(count, "\t", k, "\t\t", v)
        count += 1
        
        if count > 10 and count_sum >= total_tokens / 2:
            break
    print("Number of half word accounting sum : ", half_sum_accounting_words)


def main():
    json_content = get_parsed_content(from_file=True)
    tokens = tokenize_content(json_content)
    total_tokens = len(tokens)

    print("Total Tokens", total_tokens)
    distinct_tokens = list(set(tokens))

    print("******** After Tokenization *********\n")
    print("Distinct tokens : ", len(distinct_tokens))
    print_top_ten_words(tokens)

    after_stopwords = remove_stop_words(tokens)
    distinct_tokens = list(set(after_stopwords))
    print("\n\n******* After removal of stopwords ********")
    print("Distinct words", len(distinct_tokens))
    print_top_ten_words(after_stopwords)
