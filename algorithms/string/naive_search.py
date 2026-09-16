def naive_search(text, pattern):
    """
    Naive String Matching Algorithm.

    Returns:
        matches: list of starting positions
        states: list of intermediate execution states
        comparisons: number of character comparisons
    """

    matches = []
    states = []
    comparisons = 0

    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return matches, states, comparisons

    for i in range(n - m + 1):

        states.append({
            "type": "alignment",
            "position": i
        })

        j = 0

        while j < m:

            comparisons += 1

            states.append({
                "type": "comparison",
                "text_index": i + j,
                "pattern_index": j,
                "comparison_number": comparisons
            })

            if text[i + j] != pattern[j]:

                states.append({
                    "type": "mismatch",
                    "text_index": i + j,
                    "pattern_index": j
                })

                break

            j += 1

        if j == m:

            matches.append(i)

            states.append({
                "type": "match",
                "position": i
            })

    return matches, states, comparisons