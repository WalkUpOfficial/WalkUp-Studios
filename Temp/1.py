import wordcloud
import matplotlib.pyplot as plt

wordcloud = wordcloud.WordCloud(width=800, height=400, background_color='white').generate("Hello World! This is a sample text for generating a word cloud.")
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("on")
plt.show()