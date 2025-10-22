from collections import defaultdict

def read_aspell(path: str = "aspell.txt"):
    pairs = []
    vocab = set()

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or ":" not in line:
                continue

            correct, mistakes = line.split(":", 1)
            correct = correct.strip()

            wrong_words = [word.strip() for word in mistakes.split() if word.strip()]

            pairs.append((correct, wrong_words))

            for word in [correct] + wrong_words:
                for ch in word:
                    vocab.add(ch)
    return pairs, list(vocab)

def align(correct: str, wrong: str):
    correct_len, wrong_len = len(correct), len(wrong)
    dp = [[0]*(wrong_len+1) for _ in range(correct_len+1)]
    for i in range(1, correct_len+1): dp[i][0] = i
    for j in range(1, wrong_len+1): dp[0][j] = j

    for i in range(1, correct_len+1):
        for j in range(1, wrong_len+1):
            cost = 0 if correct[i-1] == wrong[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,
                dp[i][j-1] + 1,
                dp[i-1][j-1] + cost
            )

    i, j = correct_len, wrong_len
    aligned = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + (0 if correct[i-1] == wrong[j-1] else 1):
            aligned.append((correct[i-1], wrong[j-1]))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + 1:
            aligned.append((correct[i-1], "<eps>"))
            i -= 1
        else:
            aligned.append(("<eps>", wrong[j-1]))
            j -= 1

    aligned.reverse()
    return aligned

def compute_emissions(pairs, smoothing = 1):
    counts = {}
    emissions = {}

    for correct, wrong_words in pairs:
        for wrong_word in wrong_words:
            for correct_char, wrong_char in align(correct, wrong_word):
                if correct_char not in counts:
                    counts[correct_char] = defaultdict(int)
                counts[correct_char][wrong_char] += 1

    for char, row in counts.items():
        total = sum(row.values())
        emissions[char] = {char: count / total for char, count in row.items()}

    return emissions

def compute_transitions(pairs, smoothing = 1):
    counts = defaultdict(lambda: defaultdict(int))
    transitions = {}

    for word, _ in pairs:
        counts["<s>"][word[0]] += 1

        for idx in range(len(word) - 1):
            counts[word[idx]][word[idx + 1]] += 1

        counts[word[-1]]["</s>"] += 1

    for curr_char, row in counts.items():
        total = sum(row.values())
        transitions[curr_char] = {next_char: count / total for next_char, count in row.items()}

    return transitions

def viterbi(obs, states, start_p, transitions, emissions):
    v = [{}]
    path = {}

    start_char = obs[0]
    for state in states:
        p_start = start_p.get(state, 0)
        p_emit  = emissions.get(state, {}).get(start_char, 0)
        v[0][state] = p_start * p_emit
        path[state] = [state]

    for idx in range(1, len(obs)):
        v.append({})
        new_path = {}

        curr_obs = obs[idx]
        for state in states:
            best_prob, best_state = max(
                (
                    v[idx-1].get(next_state, 0)
                    * transitions.get(next_state, {}).get(state, 0)
                    * emissions.get(state,  {}).get(curr_obs, 0),
                    next_state
                )
                for next_state in states
            )
            v[idx][state] = best_prob
            new_path[state] = path[best_state] + [state]

        path = new_path

    final_prob, last_state = max(
        (
            v[-1].get(state, 0) * transitions.get(state, {}).get("</s>", 1.0),
            state
        )
        for state in states
    )

    result_path = []
    for char in path[last_state]:
        if char == "</s>":
            break
        if char not in ["<s>", "<eps>"]:
            result_path.append(char)

    return final_prob, result_path

def main():
    df, vocab = read_aspell()
    emissions = compute_emissions(df)
    transitions = compute_transitions(df)

    states = list(emissions.keys())
    start_p = transitions.get("<s>", {})
    print(viterbi(list("coffee"), states, start_p, transitions, emissions))
    print(viterbi(list("teea"), states, start_p, transitions, emissions))
    print(viterbi(list("caa"), states, start_p, transitions, emissions))


# ['RSX', 'absorption', 'butter', 'flux', 'infamy', 'knowing', 'media', 'scrabble', 'the']
if __name__ == "__main__":
    main()