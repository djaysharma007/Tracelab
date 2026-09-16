def build_lps(pattern):
    """
    Builds the LPS (Longest Prefix Suffix) array.
    """

    m = len(pattern)

    lps = [0] * m

    length = 0
    i = 1

    states = []

    while i < m:

        states.append({
            "type": "lps_comparison",
            "index": i,
            "prefix_index": length
        })

        if pattern[i] == pattern[length]:

            length += 1
            lps[i] = length

            states.append({
                "type": "lps_update",
                "index": i,
                "value": length
            })

            i += 1

        else:

            if length != 0:

                length = lps[length - 1]

                states.append({
                    "type": "lps_fallback",
                    "index": i,
                    "new_prefix_index": length
                })

            else:

                lps[i] = 0

                states.append({
                    "type": "lps_update",
                    "index": i,
                    "value": 0
                })

                i += 1

    return lps, states


def kmp_search(text, pattern):
    """
    Knuth-Morris-Pratt String Matching Algorithm.

    Returns:
        matches: list of starting positions
        states: list of intermediate states
        comparisons: number of character comparisons
    """

    matches = []
    states = []
    comparisons = 0

    n = len(text)
    m = len(pattern)

    if m == 0 or m > n:
        return matches, states, comparisons

    # Build LPS array
    lps, lps_states = build_lps(pattern)

    states.extend(lps_states)

    states.append({
        "type": "lps_complete",
        "lps": lps.copy()
    })

    i = 0
    j = 0

    while i < n:

        comparisons += 1

        states.append({
            "type": "comparison",
            "text_index": i,
            "pattern_index": j,
            "comparison_number": comparisons
        })

        if text[i] == pattern[j]:

            i += 1
            j += 1

            states.append({
                "type": "match_progress",
                "text_index": i - 1,
                "pattern_index": j - 1
            })

            if j == m:

                position = i - j

                matches.append(position)

                states.append({
                    "type": "match",
                    "position": position
                })

                j = lps[j - 1]

                states.append({
                    "type": "pattern_shift",
                    "new_pattern_index": j
                })

        else:

            states.append({
                "type": "mismatch",
                "text_index": i,
                "pattern_index": j
            })

            if j != 0:

                j = lps[j - 1]

                states.append({
                    "type": "pattern_shift",
                    "new_pattern_index": j
                })

            else:

                i += 1

    return matches, states, comparisons