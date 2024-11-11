# 📜 Crime Section Recommender System

This **Crime Section Recommender** uses Python and NLP to suggest relevant legal sections based on crime descriptions. Enter a description, and it provides matching sections with details on offenses, punishments, bailability, cognizability, and court handling.

## ✨ Features
- **Quick Crime Lookup**: Enter a crime description to receive relevant legal sections.
- **Detailed Info**: Each result shows offense type, punishment, and other details.
- **NLP-Powered**: Uses tokenization, stemming, and cosine similarity for matching.
- **Easy-to-Use GUI**: User-friendly interface built with Tkinter.

## 📊 Dataset
The dataset `combined_data.csv` includes:
- **Description** - Crime description
- **Offense** - Type of offense
- **Punishment** - Punishment details
- **Cognizable/Bailable** - Offense classifications
- **Court** - Handling court type

## 🛠️ How It Works
1. **Text Preprocessing**: Removes stop words and stems descriptions.
2. **Embeddings & Similarity**: Embeds text using Sentence Transformers and calculates cosine similarity for best matches.

🙏 Acknowledgments
Built with the powerful Sentence Transformers library for efficient text matching and open-source NLP tools.