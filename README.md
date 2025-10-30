# Belief-Networks-Hidden-Markov-Models
Fall 2025 CS 362/562


# Part 1
**P(MaryCalls | JohnCalls='yes')**

| MaryCalls      | φ(MaryCalls) |
|----------------|---------------|
| MaryCalls(yes) | 0.0400        |
| MaryCalls(no)  | 0.9600        |

P(MaryCalls='yes' | JohnCalls='yes') = 0.0400  

---

**P(JohnCalls, MaryCalls | Alarm='yes')**

| JohnCalls      | MaryCalls      | φ(JohnCalls, MaryCalls) |
|----------------|----------------|--------------------------|
| JohnCalls(yes) | MaryCalls(yes) | 0.6300                   |
| JohnCalls(yes) | MaryCalls(no)  | 0.2700                   |
| JohnCalls(no)  | MaryCalls(yes) | 0.0700                   |
| JohnCalls(no)  | MaryCalls(no)  | 0.0300                   |

P(JohnCalls='yes', MaryCalls='yes' | Alarm='yes') = 0.6300 

---

**P(Alarm | MaryCalls='yes')**

| Alarm      | φ(Alarm) |
|-------------|-----------|
| Alarm(yes)  | 0.1501    |
| Alarm(no)   | 0.8499    |

P(Alarm='yes' | MaryCalls='yes') = 0.1501


# Part 2
## Step 2
**P(Battery | Moves='no')**

| Battery               | φ(Battery) |
|------------------------|-------------|
| Battery(Works)         | 0.6410      |
| Battery(Doesn't work)  | 0.3590      |

**[Q1]** Ans: P(Battery='Doesn't work' | Moves='no') = 0.3590  

---

**P(Starts | Radio='Doesn't turn on')**

| Starts      | φ(Starts) |
|--------------|-----------|
| Starts(yes)  | 0.1313    |
| Starts(no)   | 0.8687    |

**[Q2]** Ans: P(Starts='no' | Radio='Doesn't turn on') = 0.8687  

---

**P(Radio | Battery: 'Works')**

| Radio                  | φ(Radio) |
|-------------------------|-----------|
| Radio(turns on)         | 0.7500    |
| Radio(Doesn't turn on)  | 0.2500    |

**P(Radio | Battery: 'Works', Gas: 'Full')**

| Radio                  | φ(Radio) |
|-------------------------|-----------|
| Radio(turns on)         | 0.7500    |
| Radio(Doesn't turn on)  | 0.2500    |

**[Q3a]** P(Radio='turns on' | Battery='Works') = 0.75  
**[Q3b]** P(Radio='turns on' | Battery='Works', Gas='Full') = 0.75  
**[Q3]** Ans: No Change

---

**P(Ignition | Moves='no')**

| Ignition               | φ(Ignition) |
|-------------------------|-------------|
| Ignition(Works)         | 0.4334      |
| Ignition(Doesn't work)  | 0.5666      |

**P(Ignition | Moves='no', Gas='Empty')**

| Ignition               | φ(Ignition) |
|-------------------------|-------------|
| Ignition(Works)         | 0.5178      |
| Ignition(Doesn't work)  | 0.4822      |

**[Q4a]** P(Ignition='Doesn't work' | Moves='no') = 0.5666  
**[Q4b]** P(Ignition='Doesn't work' | Moves='no', Gas='Empty') = 0.4821  
**[Q4]** Ans: 0.5666 -> 0.4821 Observing that the car has no gas decreases the probability of ignition failure from 0.5666 to 0.4822, because the “no gas” event accounts for part of the car’s failure to move.

---

**P(Starts | Radio='turns on', Gas='Full')**

| Starts      | φ(Starts) |
|--------------|-----------|
| Starts(yes)  | 0.7212    |
| Starts(no)   | 0.2788    |

**[Q5]** Ans: P(Starts='yes' | Radio='turns on', Gas='Full') = 0.7212

---

## Step 3

**P(KeyPresent | Moves='no')**

| KeyPresent     | φ(KeyPresent) |
|-----------------|---------------|
| KeyPresent(yes) | 0.6604        |
| KeyPresent(no)  | 0.3396        |

P(KeyPresent='no' | Moves='no') = 0.3396

# Reflection

1. Correctly spelled word but incorrectly "corrected"

Example: coffee → ceffie
Explanation:
This happened because the model over-relied on transition probabilities from the training data.
The sequence "ceffie" had a slightly higher probability based on observed character transitions, even though "coffee" was already a valid word. 
The algorithm likely favored "ceffie" due to noisy or insufficient training data, which caused it to prioritize a statistically likely sequence over a semantically valid one.

2. Incorrectly spelled word but incorrectly corrected

Example: teea → tera
Explanation:
The main reason is the length mismatch between the input (teea, 4 letters) and the intended correction (tea, 3 letters). 
Although <eps> tokens were added to handle insertions/deletions in emission probabilities, the model’s training data did not have enough examples to learn reliable transitions that shorten a 4-letter input to a 3-letter target.
Additionally, the Hidden Markov Model’s emission and transition probabilities might have biased toward maintaining input length, leading it to prefer "tera" (same length) over the more correct "tea."

3. Incorrectly spelled word and correctly corrected

Example: caa → cat
Explanation:
This case worked because both the input and target word had the same length, so the HMM did not need to handle insertions or deletions. 
The training data also contained enough examples for the model to learn that the transition from aa to at has a high probability.
If the dataset were smaller or biased toward different vocabulary, the same input (caa) could have been mapped to another plausible word like "cow." 
This shows that correction accuracy depends heavily on training data coverage and distribution.

4. Real-world vs. synthetic training data

If the training dataset came from real-world typos, the model would likely perform better in practice, since it would learn realistic substitution, omission, and transposition patterns that people actually make.
In contrast, synthetic typos often lack these natural patterns and can produce unrealistic error distributions. This can cause the model to generalize poorly when encountering genuine human mistakes.
In summary, real-world data improves robustness and realism, while synthetic data may be cleaner but less representative.