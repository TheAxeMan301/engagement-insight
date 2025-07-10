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
    all_comments_array = parse_csv("./engagements.csv")
    print("For all posts")
    print(f"{len(all_comments_array)} comments")
    process_array(all_comments_array)
    print("\n\n")

    # Break down by post
    posts_dict = {}
    for entry in all_comments_array:
        media_id = entry["media_id"]
        media_caption = entry["media_caption"]
        post_entry = posts_dict.setdefault(media_id, {
            "media_caption": media_caption,
            "count": 0,
        })
        post_entry["count"] += 1

    # List of each media_id
    posts_list = list(posts_dict.keys())
    posts_list = sorted(posts_list, key=lambda media_id: -posts_dict[media_id]["count"])

    for media_id in posts_list:
        media_comments = [entry for entry in all_comments_array if entry["media_id"] == media_id]
        print("Post text")
        print(posts_dict[media_id]["media_caption"])
        if (len(media_comments) > 0):
            print(f"{len(media_comments)} comments")
            process_array(media_comments)
        else:
            print("No comments on this post")
        print("\n\n")


main()
