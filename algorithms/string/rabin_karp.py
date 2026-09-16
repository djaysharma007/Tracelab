def rabin_karp(text, pattern):
    """
    Rabin-Karp String Matching Algorithm.

    Uses rolling hash to find pattern occurrences.

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

    # Prime number used for hashing
    prime = 101

    # Base for polynomial hashing
    base = 256

    pattern_hash = 0
    window_hash = 0

    # base^(m-1)
    highest_power = 1

    for _ in range(m - 1):
        highest_power = (highest_power * base) % prime

    # Calculate initial hashes
    for i in range(m):
        pattern_hash = (
            (base * pattern_hash) + ord(pattern[i])
        ) % prime

        window_hash = (
            (base * window_hash) + ord(text[i])
        ) % prime

    states.append({
        "type": "hash_calculation",
        "position": 0,
        "pattern_hash": pattern_hash,
        "window_hash": window_hash
    })

    for i in range(n - m + 1):

        states.append({
            "type": "window",
            "position": i,
            "pattern_hash": pattern_hash,
            "window_hash": window_hash
        })

        # Hashes match
        if pattern_hash == window_hash:

            states.append({
                "type": "hash_match",
                "position": i
            })

            # Verify characters
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

        # Calculate hash for next window
        if i < n - m:

            window_hash = (
                base * (
                    window_hash
                    - ord(text[i]) * highest_power
                )
                + ord(text[i + m])
            ) % prime

            window_hash = window_hash % prime

            states.append({
                "type": "shift",
                "from": i,
                "to": i + 1
            })

    return matches, states, comparisons