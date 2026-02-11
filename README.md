# 🎬 SenpaiList - Anime Recommendation System

A modern Flask-based anime recommendation system using content-based filtering (TF-IDF + cosine similarity) and a responsive UI with Tailwind CSS v4.

## 📋 CV-Ready Description

**Full-stack anime recommendation web application** leveraging **machine learning** (scikit-learn's TF-IDF vectorization and cosine similarity) for content-based filtering on a 20,000+ anime dataset. Built with **Python/Flask backend**, **RESTful routing**, **Jinja2 templating**, and **Tailwind CSS v4** frontend featuring real-time search, personalized recommendations, and responsive UI. Implements **model persistence** with pickle serialization for optimized performance and **data preprocessing pipelines** using pandas/numpy for large-scale dataset processing.

## ✨ Features

- 🔍 **Smart Search**: Search anime by name, genre, or synopsis
- 🎯 **Content-Based Recommendations**: Personalized suggestions by genres, type, and synopsis
- 🎨 **Modern UI**: Responsive, animated, and mobile-friendly
- ⚡ **Fast**: Pre-computed similarity matrix for instant results
- 🖼️ **Fallback Images**: Automatic placeholder for missing covers

## 🛠️ Tech Stack

- **Backend**: Flask 3.0+, Python 3.13
- **ML/Data**: pandas, numpy, scikit-learn
- **Frontend**: Tailwind CSS v4, Jinja2, HTML5
- **Data**: CSV (Kaggle), Pickle (model cache)

## 🚀 Quickstart

1. **Clone & Setup**
   ```bash
   git clone https://github.com/Mujtaba-Kamran/SenpaiList.git
   cd SenpaiList
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   pip install -r requirements.txt
   ```
2. **Get Dataset**
   - Download `anime-dataset-2023.csv` from [Kaggle](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset) and place in `data/`
3. **Run**
   ```bash
   python app.py
   # Visit http://127.0.0.1:5000
   ```

## 📁 Structure

```
SenpaiList/
├── app.py                # Main Flask app
├── requirements.txt      # Dependencies
├── data/                 # Dataset CSV
├── models/               # Pickle model
├── static/               # Images & placeholder
└── templates/            # index.html, recommendations.html
```

## 🔄 How It Works

1. **Startup**: Loads/cleans dataset, builds or loads similarity matrix (TF-IDF + cosine similarity, cached as pickle)
2. **Homepage**: Shows top 20 anime by score
3. **Search**: Filters anime by name/synopsis
4. **Recommendations**: Finds top 10 similar anime using content-based filtering

## ⚙️ Customization

- **Change recommendations count**: In `app.py`, edit `get_recommendations(anime_title, n=10)`
- **Change top anime count**: In `app.py`, edit `df.nlargest(20, 'Score')`
- **Change port**: In `app.py`, edit `app.run(debug=True, port=5001)`

## 🐛 Troubleshooting

- **ModuleNotFoundError**: Activate venv, reinstall with `pip install -r requirements.txt`
- **Dataset Not Found**: Ensure `data/anime-dataset-2023.csv` exists
- **Port in Use**: Change port in `app.py`
- **DLL Load Failed (Windows)**: `pip uninstall numpy pandas scikit-learn && pip install --only-binary=:all: numpy pandas scikit-learn`
- **Images Not Loading**: Check `static/placeholder/placeholder.jpg` exists
- **Slow First Run**: Model builds on first run, then loads instantly
- **Memory Issues**: Limit dataset in `app.py` with `df = df.head(10000)`

## 📝 Dependencies

See `requirements.txt` for all dependencies. Main:

- Flask>=3.0.0
- pandas>=2.0.0
- numpy>=1.24.0
- scikit-learn>=1.3.0
- requests>=2.31.0

## 🚀 Deployment

- **Local**: `python app.py` (http://127.0.0.1:5000)
- **Production (Windows)**: `pip install waitress && waitress-serve --host=0.0.0.0 --port=8000 app:app`
- **Production (Linux/Mac)**: `pip install gunicorn && gunicorn -w 4 -b 0.0.0.0:8000 app:app`

## 🤝 Contributing

Contributions welcome! Fork, branch, PR. Please follow PEP 8, add docstrings, and test your changes.

## 📄 License

MIT License © 2025 Mujtaba Kamran | Shubair Hyder

## 👤 Authors

- [@Mujtaba-Kamran](https://github.com/Mujtaba-Kamran)
- [@SyedMuhammadShubairHyder](https://github.com/SyedMuhammadShubairHyder)

## 🙏 Acknowledgments

- [MyAnimeList Dataset 2023](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset)
- [Flask](https://flask.palletsprojects.com/), [Tailwind CSS v4](https://tailwindcss.com/), [scikit-learn](https://scikit-learn.org/)

## 🔮 Future Enhancements

- [ ] User authentication & watchlists
- [ ] Collaborative/hybrid recommendations
- [ ] Advanced filters, API integration, PWA, and more

---

**Built with ❤️ for the anime community | Last Updated: December 2025**