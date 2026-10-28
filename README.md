# Harmonify

**Find people who share your music taste, and new songs to listen to.**

Harmonify is a music-based friend and song recommender. Pick your five favourite songs, your favourite genre and the song length you prefer, and Harmonify finds the most compatible listener in its dataset. It then shows the songs you have in common and recommends the songs they listen to that you haven't picked.

It was built as the final project for **CSC111 (Foundations of Computer Science II)** at the University of Toronto.

## How it works

Users and songs are stored as vertices in a graph, and an edge connects a user to each song they listen to. When you enter your choices, you are added to the graph as a new user. Harmonify then compares you with every other user using this score:

```
similarity = 3 × (songs in common)
           + 2 × (songs in common that match your favourite genre)
           + 1 × (songs in common that match your preferred duration)
```

The user with the highest score is your match. Song durations are grouped like this:

| Duration | Song length |
| --- | --- |
| Short | under 2 minutes |
| Medium | 2 to 8 minutes |
| Long | over 8 minutes |

The song data comes from the [Spotify Tracks Genre dataset](https://www.kaggle.com/datasets/thedevastator/spotify-tracks-genre-dataset) on Kaggle, cut down to the 200 most popular tracks.

## Getting started

### Requirements

- Python 3.10 or newer, with Tkinter (included with most Python installs)

### Install

```bash
git clone https://github.com/mertrassa/Harmonify-CSC111.git
cd Harmonify-CSC111
pip install -r requirements.txt
```

### Run

Run it from the project folder so it can find the CSV files:

```bash
python main.py
```

## Using the app

1. Click **Song List** to open a PDF of the 200 songs and their IDs.
2. Enter a username and the IDs (1 to 200) of five different songs you like.
3. Enter your favourite genre. **Info → Genre** lists the genres you can choose from.
4. Choose a preferred song duration: **Short**, **Medium** or **Long**.
5. Click **Launch** to see your match: their name, username, age, province, match score, the songs you share, and their other songs as recommendations.

Other options:

- **Visualize Program** draws the whole user–song graph.
- **Options → Switch Color** switches between light and dark mode.

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Tkinter interface and entry point |
| `graph_functions.py` | Graph and vertex classes, similarity scoring, recommendations and loading data from CSV |
| `graph_visualization.py` | Graph visualization with NetworkX and Plotly |
| `data.py` | Script that produced `songs_by_popularity.csv` from the raw dataset |
| `all_user_data_200_songs.csv` | User data the app uses |
| `songs_by_popularity.csv` | The 200 songs the app uses |
| `pre_processed_all_songs.csv` | Raw Spotify dataset |
| `Datas.zip` | Archive of the data files |
| `mypdf.pdf` | Song list opened by the **Song List** button |
| `project_report.pdf` / `.tex` | Project report |

## Report

The full write-up, covering the data, the algorithms and the design decisions, is in [project_report.pdf](project_report.pdf).

## Authors

- Mert Rassa
- Salih Atamert Cam
- Ece Avşar
