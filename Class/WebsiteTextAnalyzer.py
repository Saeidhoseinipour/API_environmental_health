import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from collections import Counter

class WebsiteTextAnalyzer:
    def __init__(self, urls):
        self.urls = self.filter_urls(urls)
        self.text_data = []

    def filter_urls(self, urls):
        valid_urls = []

        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                valid_urls.append(url)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url}: {e}")

        return valid_urls

    def fetch_text_from_urls(self):
        for url in self.urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text()

                # Remove extra spaces, newlines, "/", and "..."
                cleaned_text = re.sub(r'\s+', ' ', text)
                cleaned_text = cleaned_text.replace("/", "").replace("...", "")
                cleaned_text = re.sub(r'\d', '', cleaned_text)
                cleaned_text = cleaned_text.replace("Twitter", "").replace("Instagram", "").replace("Telegram", "")

                self.text_data.append(cleaned_text)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching {url}: {e}")

    def plot_word_frequencies(self):
        all_words = []
        for text in self.text_data:
            all_words.extend(text.split())

        word_count = Counter(all_words)
        common_words = [word for word, _ in word_count.most_common(10)]
        counts = [word_count[word] for word in common_words]

        plt.figure(figsize=(8, 6))
        plt.barh(common_words[::-1], counts[::-1], color='skyblue')
        plt.xlabel('Frequency')
        plt.ylabel('Words')
        plt.title('Top 10 Most Common Words')
        plt.tight_layout()
        plt.show()

    def save_combined_corpus(self, file_path):
        combined_corpus = ' '.join(self.text_data)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(combined_corpus)
        print(f"Combined corpus saved to {file_path}")

    def save_text_data(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            for item in self.text_data:
                file.write("%s\n" % item)
        print(f"Text data saved to {file_path}")

# Example usage
urls = [
    "http://www.example.com",
    "http://www.anotherexample.com"
]

analyzer = WebsiteTextAnalyzer(urls)
analyzer.fetch_text_from_urls()
analyzer.plot_word_frequencies()

# Save combined corpus and text data
analyzer.save_combined_corpus('Corpus_API_climate.txt')
analyzer.save_text_data('text_data_API_climate.txt')
