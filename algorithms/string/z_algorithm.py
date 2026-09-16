def build_z_array(string):
    """
    Builds the Z-array for a string.

    Z[i] = length of the substring starting at i
           that matches the prefix of the string.
    """

    n = len(string)

    z = [0] * n

    left = 0
    right = 0

    states = []
    comparisons = 0

    for i in range(1, n):

        if i <= right:
            z[i] = min(
                right - i + 1,
                z[i - left]
            )

        while i + z[i] < n:

            comparisons += 1

            states.append({
                "type": "comparison",
                "index": i + z[i],
                "prefix_index": z[i],
                "comparison_number": comparisons
            })

            if string[z[i]] == string[i + z[i]]:

                z[i] += 1

            else:

                states.append({
                    "type": "mismatch",
                    "index": i + z[i],
                    "prefix_index": z[i]
                })

                break

        if i + z[i] - 1 > right:

            left = i
            right = i + z[i] - 1

            states.append({
                "type": "z_box_update",
                "left": left,
                "right": right
            })

        states.append({
            "type": "z_update",
            "index": i,
            "value": z[i]
        })

    return z, states, comparisons


def z_search(text, pattern):
    """
    Z Algorithm String Matching.

    Returns:
        matches: list of starting positions
        states: list of intermediate states
        comparisons: number of character comparisons
    """

    matches = []
    states = []

    if not pattern or len(pattern) > len(text):
        return matches, states, 0

    separator = "$"

    # Ensure separator does not occur in text/pattern
    while separator in text or separator in pattern:
        separator += "$"

    combined = pattern + separator + text

    states.append({
        "type": "combined_string",
        "string": combined
    })

    z, z_states, comparisons = build_z_array(combined)

    states.extend(z_states)

    states.append({
        "type": "z_complete",
        "z": z.copy()
    })

    pattern_length = len(pattern)

    for i in range(pattern_length + len(separator), len(combined)):

        if z[i] == pattern_length:

            position = i - pattern_length - len(separator)

            matches.append(position)

            states.append({
                "type": "match",
                "position": position
            })

    return matches, states, comparisons