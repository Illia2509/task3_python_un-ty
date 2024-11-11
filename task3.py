import os
import googleapiclient.discovery
from collections import Counter
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud 


api_key = "AIzaSyBYBojb-KGeclJa4QAfr-VJ4D0l-NfLlSg"


video_id = "R-QJg1AbmKI"


def get_comments(api_key, video_id):
    comments = []
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100
    )

    while request:
        response = request.execute()
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        request = youtube.commentThreads().list_next(request, response)

    return comments


def preprocess_text(comments):
    all_words = []
    for comment in comments:
        words = re.findall(r'\w+', comment.lower()) 
        all_words.extend(words)
    return all_words


comments = get_comments(api_key, video_id)


words = preprocess_text(comments)


stop_words = set([
    "і", "та", "не", "за", "на", "в", "це", "з", "а", "але", "чи", "або", "що", "як", "коли", "бо", "також", "проте", "щоб", "хоча", "якщо", "тому що", "поки що", "навіть якщо", "наскільки", "хоч би", "для того щоб", "незважаючи на те що", "до того як", "після того як", "оскільки", "з огляду на те що", "в той час як", "з тих пір як", "заради того щоб", "як тільки", "так само як"
])

filtered_words = [word for word in words if word not in stop_words]


word_counts = Counter(filtered_words)


most_common_word, frequency = word_counts.most_common(1)[0]
print(f"Найвживаніше слово: '{most_common_word}' з частотою: {frequency}")


top_words = dict(word_counts.most_common(20))  
plt.figure(figsize=(10, 5))
plt.bar(top_words.keys(), top_words.values(), color='skyblue')
plt.xticks(rotation=45)
plt.xlabel("Слова")
plt.ylabel("Частота")
plt.title("Частота вживання слів у коментарях до відео")
plt.show()


wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()