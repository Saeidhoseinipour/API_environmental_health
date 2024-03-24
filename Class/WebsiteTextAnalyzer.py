import requests
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import csv

class WebsiteTextAnalyzer:
    def __init__(self, urls, remove_words=None, num_words_plot=None):
        self.urls = self.filter_urls(urls)
        self.text_data = []
        self.remove_words = remove_words
        self.num_words_plot = num_words_plot
        self.corpus = ''
        self.vocab = {}
        self.tfidf_matrix = None

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

    def clean_text_data(self):
        self.corpus = ' '.join(self.text_data)
        if self.remove_words:
            for word in self.remove_words:
                self.corpus = self.corpus.replace(word, '')
        self.corpus = re.sub(r'\s+', ' ', self.corpus)

    def plot_word_frequencies(self):
        all_words = self.corpus.split()

        word_count = Counter(all_words)
        common_words = [word for word, _ in word_count.most_common(self.num_words_plot)]
        counts = [word_count[word] for word in common_words]

        plt.figure(figsize=(3, 5))
        plt.barh(common_words[::-1], counts[::-1], color='black')
        plt.xlabel('Frequency')
        plt.ylabel('Words')
        plt.title(f'Top {self.num_words_plot} Most Common Words')
        plt.tight_layout()
        plt.show()

    def generate_tfidf_matrix(self):
        tfidf = TfidfVectorizer()
        self.tfidf_matrix = tfidf.fit_transform(self.text_data)
        self.vocab = tfidf.vocabulary_

    def save_outputs(self, corpus_file_path='corpus.txt', text_data_file_path='text_data.txt', vocabulary_file_path='vocabulary.csv'):
        # Save combined corpus
        with open(corpus_file_path, 'w', encoding='utf-8') as file:
            file.write(self.corpus)
        print(f"Combined corpus saved to {corpus_file_path}")

        # Save scraped text data to a .txt file
        with open(text_data_file_path, 'w', encoding='utf-8') as file:
            for item in self.text_data:
                file.write("%s\n" % item)
        print(f"Text data saved to {text_data_file_path}")

        # Save vocabulary to a CSV file
        vocabulary_list = [(word, index) for word, index in self.vocab.items()]
        with open(vocabulary_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Word', 'Index'])  # Write header
            csv_writer.writerows(vocabulary_list)
        print(f'Vocabulary saved to {vocabulary_file_path}')

# Example usage
urls = [
    "http://www.climatecentral.org/",
    "http://skepticalscience.com/",
    "http://www.climatechangenews.com/",
    "http://www.npr.org/sections/climate/",
    "http://public.wmo.int/en/media/news",
    "http://www.climatechangenews.com/",
    "http://www.theclimategroup.org/",
    "http://www.climaterealityproject.org/",
    "http://www.worldwildlife.org/initiatives/climate",
    "http://climate.nasa.gov/",
    "http://www.climate.gov/",
    "http://unfccc.int/",
    "http://www.ipcc.ch/",
    "http://www.worldbank.org/en/topic/climatechange",
    "http://www.nationalgeographic.com/environment/climate-change/",
    "http://www.climaterealityproject.org/",
    "http://www.ucsusa.org/climate",
    "http://www.climatecentral.org/",
    "http://www.climateworks.org/",
    "http://skepticalscience.com/",
    "http://climaticoanalysis.org/",
    "http://www.climatechangenews.com/",
    "http://www.npr.org/sections/climate/",
    "http://public.wmo.int/en/media/news",
    "http://www.climatechangenews.com/",
    "http://www.theclimategroup.org/",
    "http://www.climaterealityproject.org/",
    "http://www.worldwildlife.org/initiatives/climate",
    "http://www.airnow.gov/",
    "http://waqi.info/",
    "http://www.edf.org/airquality",
    "http://www.eea.europa.eu/themes/air",
    "http://www.iqair.com/",
    "http://www.nationalgeographic.com/environment/article/air-pollution",
    "http://www.eea.europa.eu/themes/air",
]
remove_words = ['the', 'of', 'and','to','a','in','is'
                ,'on','for','The','re','tht','by',',',
                'with','ir','from','or','bout','chnge','climte','s',
               'mo','A','t','th','&','we','be','n','hs','se','hve','e',
               'h','i','.','d','oe','o','l','m','p','c','r',
               'g','y','ew','our','chge','u','w','V']
num_words_plot = 20

analyzer = WebsiteTextAnalyzer(urls, remove_words=remove_words, num_words_plot=num_words_plot)
analyzer.fetch_text_from_urls()
analyzer.clean_text_data()
analyzer.plot_word_frequencies()
analyzer.generate_tfidf_matrix()
analyzer.save_outputs()
