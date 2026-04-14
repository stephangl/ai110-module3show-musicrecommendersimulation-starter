# Reflection: Adversarial Profile Comparisons

## Original Weights (genre: 0.30, mood: 0.25, energy: 0.25)

### Profile 1 vs Profile 5: Conflicting energy+mood vs Acoustic boundary

The conflicting profile (energy 0.9, mood "melancholic") surfaces high-energy pop songs like *Gym Hero* (0.64) and *Sunrise City* (0.63), completely ignoring the melancholic mood signal. Meanwhile, the acoustic boundary profile (energy 0.3, mood "chill", acoustic) gets near-perfect matches in *Library Rain* (0.99) and *Midnight Coding* (0.97) because all three signals align. This shows the recommender works well when preferences are coherent but breaks down when they conflict — the heavier weights (genre, energy) simply overpower mood.

### Profile 2 vs Profile 3: Substring genre trick vs Substring mood trick

Both profiles exploit the loose substring matching. Profile 2 ("pop" genre) correctly gets *Sunrise City* at 0.92, but *Rooftop Lights* ("indie pop") scores 0.78 as a "similar genre" — a reasonable but unearned bonus. Profile 3 ("ill" mood) is worse: *Midnight Coding* and *Library Rain* (both "chill") score 0.33 and 0.31 as "similar mood" even though "ill" and "chill" have nothing to do with each other. The genre substring happens to produce semi-plausible results; the mood substring produces nonsense.

### Profile 4 vs Profile 1: Missing valence mood vs Conflicting energy+mood

Profile 4 ("angry" mood, rock, energy 0.8) places *Storm Runner* (rock, "intense", 0.62) above *Iron Ritual* (metal, "angry", 0.56) even though *Iron Ritual* is the only angry-mood song in the catalog. The reason: "angry" is not in the valence bonus list, so *Iron Ritual* silently loses up to 0.10 that a "chill" or "happy" user would receive. In contrast, Profile 1 at least gets mood-adjacent results because "melancholic" triggers the valence bonus. The system effectively penalizes users whose mood falls outside the hardcoded valence categories.

### Profile 6 vs Profile 5: Acoustic+genre conflict vs Acoustic boundary

Profile 6 (metal, intense, energy 0.9, likes acoustic) surfaces non-acoustic songs like *Iron Ritual* (acousticness 0.03, score 0.53) because genre and energy dominate the score. Profile 5 (lofi, chill, energy 0.3, likes acoustic) gets perfect acoustic matches because lofi songs are already acoustic. This reveals a structural bias: the recommender cannot reconcile a preference for acoustic sound with a genre that rarely features it. The acoustic weight (0.10) is simply too small to compete with genre (0.30) and energy (0.25).

### Profile 7 vs Profile 8: Energy extreme 0.0 vs Energy center 0.5

Profile 7 (energy 0.0) and Profile 8 (energy 0.5) produce top results that are remarkably similar despite very different energy targets. Both are dominated by genre and mood matches. Energy 0.0 slightly penalizes higher-energy lofi songs but not enough to change the ranking. Energy 0.5 provides almost no differentiation at all — songs with energy from 0.35 to 0.93 all get similar energy scores because the midpoint is equidistant from both extremes. This confirms that energy is a useful signal only at the edges; near 0.5 it becomes noise.

## Weight-Shift Experiment (genre: 0.15, mood: 0.25, energy: 0.50)

### Profile 4 after weight shift: Missing valence mood improves

With energy doubled, *Iron Ritual* (energy 0.97, angry mood) jumped from 0.56 to 0.77 and took the top spot away from *Storm Runner*. This is a more accurate result for a user who wants high-energy angry music. The genre weight reduction also helped — metal vs rock mattered less, letting the energy match dominate. This suggests the weight shift is beneficial for profiles where energy is the primary signal.

### Profile 6 after weight shift: Acoustic+genre conflict improves

*Storm Runner* (rock, intense, energy 0.91, score 0.74) overtook *Iron Ritual* (metal, angry, energy 0.97, score 0.61) — the energy match to the user's 0.9 target now outweighs the genre mismatch. However, both top songs still have acousticness below 0.10, meaning the user's acoustic preference is entirely ignored. The weight shift fixed the ordering between non-acoustic songs but did not solve the deeper problem that acoustic songs cannot compete in a high-energy ranking.

### Profile 1 after weight shift: Conflicting energy+mood gets worse

The conflicting profile now surfaces *Night Drive Loop* (score 0.62) in the top 5, pushing *Winter Strings* (the only melancholic song) further down. Doubling energy made the mood signal even more powerless — the recommender is now confidently recommending happy/intense songs to a user who said they feel melancholic. The weight shift amplified the existing bias rather than resolving the conflict.

### Profile 8 after weight shift: Energy center 0.5 unchanged

Scores shifted slightly upward (0.92 to 0.94 for *Sunrise City*) but the ranking is identical. Energy=0.5 still provides almost no differentiation — the doubled weight just uniformly inflated all energy scores without changing any relative ordering. This confirms that the problem with central energy targets is not the weight but the signal itself.