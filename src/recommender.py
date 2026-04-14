from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a list of songs."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs matching the user's preferences."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        scored = []
        for song in self.songs:
            song_dict = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
                "tempo_bpm": song.tempo_bpm,
            }
            score, _ = score_song(prefs, song_dict)
            scored.append((score, song))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
            "tempo_bpm": song.tempo_bpm,
        }
        _, reasons = score_song(prefs, song_dict)
        return "Matches your preference for " + ", ".join(reasons) + "."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in float_fields:
                row[field] = float(row[field])
            row["id"] = int(row["id"])
            songs.append(dict(row))

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a song against user preferences.

    Returns (score, reasons) where score is 0.0–1.0 and reasons
    is a list of short strings explaining what matched.
    """
    score = 0.0
    reasons = []

    # Genre match (weight 0.30)
    if user_prefs.get("genre") and song.get("genre"):
        if user_prefs["genre"] == song["genre"]:
            score += 0.30
            reasons.append(f"genre ({song['genre']})")
        elif user_prefs["genre"] in song["genre"] or song["genre"] in user_prefs["genre"]:
            score += 0.15
            reasons.append(f"similar genre ({song['genre']})")

    # Mood match (weight 0.25)
    if user_prefs.get("mood") and song.get("mood"):
        if user_prefs["mood"] == song["mood"]:
            score += 0.25
            reasons.append(f"mood ({song['mood']})")
        elif user_prefs["mood"] in song["mood"] or song["mood"] in user_prefs["mood"]:
            score += 0.10
            reasons.append(f"similar mood ({song['mood']})")

    # Energy closeness (weight 0.25) — closer to target = higher score
    if user_prefs.get("energy") is not None and song.get("energy") is not None:
        energy_diff = abs(user_prefs["energy"] - song["energy"])
        energy_score = max(0.0, 0.25 * (1 - energy_diff))
        score += energy_score
        if energy_diff <= 0.15:
            reasons.append(f"energy ({song['energy']:.2f})")

    # Acoustic preference (weight 0.10)
    if user_prefs.get("likes_acoustic") is not None and song.get("acousticness") is not None:
        acoustic_match = (user_prefs["likes_acoustic"] and song["acousticness"] > 0.5) or \
                         (not user_prefs["likes_acoustic"] and song["acousticness"] <= 0.5)
        if acoustic_match:
            score += 0.10
            reasons.append(f"acousticness ({song['acousticness']:.2f})")

    # Valence bonus (weight 0.10) — positive moods prefer high valence, etc.
    if song.get("valence") is not None:
        if user_prefs.get("mood") in ("happy", "confident", "romantic") and song["valence"] > 0.6:
            score += 0.10
            reasons.append(f"positive valence ({song['valence']:.2f})")
        elif user_prefs.get("mood") in ("chill", "melancholic", "nostalgic") and song["valence"] <= 0.6:
            score += 0.10
            reasons.append(f"lower valence ({song['valence']:.2f})")

    return (score, reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, score, "Matches your preference for " + ", ".join(reasons) + ".")
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
