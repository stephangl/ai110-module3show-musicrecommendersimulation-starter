# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Intended Use

VibeMatch suggests songs based on a user's genre, mood, and energy preferences. It assumes users have simple, consistent tastes — one favorite genre, one mood, one energy level. This is a classroom project for exploring how scoring-based recommenders work, not a production music app. Don't use it to make real playlist decisions or assume it understands nuanced musical taste.

---

## 3. How the Model Works

Each song gets a score from 0 to 1 based on how well it matches what the user wants. Genre is the biggest factor (0.30 points for an exact match), followed by mood (0.25) and energy closeness (0.25). There are smaller bonuses for matching the user's acoustic preference (0.10) and for valence aligning with mood (0.10) — happy users get a boost from high-valence songs, sad users from low-valence ones. The top 5 scoring songs are returned as recommendations.

---

## 4. Data

The catalog has 15 songs across 9 genres (pop, rock, lofi, metal, classical, ambient, r&b, hip-hop, synthwave) and 8 moods (happy, chill, intense, melancholic, focused, romantic, angry, confident). Pop, lofi, and rock each have 2-3 songs while most other genres have just one. There are no jazz, country, or electronic dance tracks, and no instrumental-only or world music songs.

---

## 5. Strengths

The system works well when a user's preferences all point in the same direction — a chill lofi listener who likes acoustic music gets near-perfect recommendations. Genre and mood matches are intuitive and easy to explain. The energy scoring correctly rewards songs that are close to the user's target, which feels natural for high-energy or low-energy listeners.

---

## 6. Limitations and Bias

The 15-song catalog is too small and too skewed toward pop/lofi/rock — users who prefer jazz or country will always see the same single song. Substring matching causes false positives: "ill" matches "chill" and "pop" matches "indie pop," giving unearned score boosts. Moods like "angry" and "excited" are excluded from the valence bonus, silently penalizing those users. Conflicting preferences (high energy + sad mood) get resolved in favor of the heaviest weight, meaning mood often loses to genre or energy.

---

## 7. Evaluation

Tested 8 adversarial profiles: conflicting energy+mood, substring genre trick, substring mood trick, missing valence mood, acoustic boundary, acoustic+genre conflict, energy extreme (0.0), and energy center (0.5). Biggest surprise: the substring mood trick actually worked — "ill" matched "chill" songs, proving the comparison is too loose. Also surprising: energy=0.5 barely changed any rankings because it's equidistant from both extremes. Ran a weight-shift experiment (genre halved, energy doubled) which helped the angry profile but worsened the conflicting profile — the change made results different, not clearly better.

---

## 8. Intended Use and Non-Intended Use

**Intended:** Classroom exploration of how scoring-based recommenders work, testing edge cases, and understanding filter bubbles.

**Non-intended:** Making real playlist or music curation decisions, profiling actual user behavior, or deploying as a production recommendation service. The catalog and scoring logic are too simple for real-world use.

---

## 9. Future Work

1. Replace substring matching with exact or set-based genre/mood comparisons to eliminate false positives.
2. Expand the catalog to 50+ songs with better genre coverage so niche users get real variety.
3. Add a diversity penalty so the top 5 results don't all come from the same genre or energy range.

---

## 10. Personal Reflection

My biggest learning moment was realizing that a 70-line scoring function can already produce recommendations that *feel* smart even when they're mathematically simple. The substring trick was a wake-up call — the code looked correct, but "ill" matching "chill" proved I needed to test edge cases I wouldn't have thought of on my own. AI tools were great for generating adversarial profiles and running experiments quickly, but I had to double-check the weight-shift results myself because the agent couldn't tell me whether "different" meant "better." What surprised me most is how weight tuning is a tradeoff, not a fix — making one profile better made another worse. If I kept going, I'd want to try collaborative filtering instead of pure scoring, to see whether user-to-user similarity beats feature-to-feature matching.