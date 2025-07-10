import re, regex
import pandas

"""
Parse the csv file into a simple array of dictionaries that we can process.
"""
def parse_csv(filename):
    data_frame = pandas.read_csv(filename)
    return data_frame.to_dict(orient='records')

"""
Get a set of words in the text. Emojis count as a word.
"""
def get_word_set(text):
    # Some comments aren't processed by this, just fail with empty set
    try:
        word_set = set(regex.findall(r'\p{Emoji}|\w+', text))
        word_set = set(word.lower() for word in word_set)
        # Trying to get rid of empty entries, may actually be some non-print char?
        word_set.discard("")
    except Exception as e:
        return set()

    return word_set

"""
Get a count of each word in the given dataset
"""
def word_count(comment_array):
    count_data = {}
    for comment_data in comment_array:
        comment_text = comment_data["comment_text"]
        word_set = get_word_set(comment_text)
        for word in word_set:
            word_count_data = count_data.setdefault(word, {"count": 0})
            word_count_data["count"] += 1
    return count_data

"""
Print out a report with data on the top 100 words in each dataset
"""
def process_array(comment_array):
    results = word_count(comment_array)
    word_list = list(results.keys())
    sorted_words = sorted(word_list, key=lambda word: -results[word]["count"])
    print(sorted_words[:100])
    #for word in sorted_words[:100]:
        #print(f"{word} - {results[word]["count"]}")


def main():
    comment_array = parse_csv("./engagements.csv")
    print("For all posts")
    process_array(comment_array)

main()
