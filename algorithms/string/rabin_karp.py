from typing import Any, Dict, List, Tuple


def run_rabin_karp(input_data: Dict[str, Any], mode: str = "record") -> Tuple[Any, Any]:
    text = str(input_data["text"])
    pattern = str(input_data["pattern"])
    n = len(text)
    m = len(pattern)

    matches = []
    char_comparisons = 0
    hash_calculations = 0
    hash_matches = 0

    prime = 101
    base = 256

    if mode == "silent":
        if m > 0 and m <= n:
            h = 1
            for _ in range(m - 1):
                h = (h * base) % prime
            p_hash = 0
            t_hash = 0
            for i in range(m):
                p_hash = (base * p_hash + ord(pattern[i])) % prime
                t_hash = (base * t_hash + ord(text[i])) % prime
            hash_calculations += 2

            for i in range(n - m + 1):
                if p_hash == t_hash:
                    hash_matches += 1
                    j = 0
                    while j < m:
                        char_comparisons += 1
                        if text[i + j] != pattern[j]:
                            break
                        j += 1
                    if j == m:
                        matches.append(i)
                if i < n - m:
                    t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
                    if t_hash < 0:
                        t_hash += prime
                    hash_calculations += 1
        return {"output": matches, "solution": matches, "counters": {"char_comparisons": char_comparisons, "hash_calculations": hash_calculations, "hash_matches": hash_matches}}

    def generator():
        nonlocal char_comparisons, hash_calculations, hash_matches
        found_matches = []

        yield {
            "type": "init",
            "message": f"Starting Rabin-Karp Search for text (len {n}) and pattern '{pattern}' (len {m}).",
            "state": {
                "text": text,
                "pattern": pattern,
                "position": 0,
                "pattern_hash": 0,
                "window_hash": 0,
                "char_states": {},
                "matches": []
            },
            "counters": {"char_comparisons": 0, "hash_calculations": 0, "hash_matches": 0}
        }

        if m == 0 or m > n:
            yield {
                "type": "done",
                "message": "Pattern length is invalid.",
                "state": {"text": text, "pattern": pattern, "position": 0, "matches": []},
                "counters": {}
            }
            return

        h = 1
        for _ in range(m - 1):
            h = (h * base) % prime

        p_hash = 0
        t_hash = 0
        for i in range(m):
            p_hash = (base * p_hash + ord(pattern[i])) % prime
            t_hash = (base * t_hash + ord(text[i])) % prime
        hash_calculations += 2

        yield {
            "type": "hash_calc",
            "message": f"Initial hashes calculated: Pattern Hash = {p_hash}, First Window Hash = {t_hash}.",
            "state": {
                "text": text,
                "pattern": pattern,
                "position": 0,
                "pattern_hash": p_hash,
                "window_hash": t_hash,
                "matches": []
            },
            "counters": {"hash_calculations": 2}
        }

        for i in range(n - m + 1):
            is_hash_match = (p_hash == t_hash)

            yield {
                "type": "window_check",
                "message": f"Window at index {i}: Window Hash ({t_hash}) {'==' if is_hash_match else '!='} Pattern Hash ({p_hash}).",
                "state": {
                    "text": text,
                    "pattern": pattern,
                    "position": i,
                    "pattern_hash": p_hash,
                    "window_hash": t_hash,
                    "hash_match": is_hash_match,
                    "matches": list(found_matches)
                },
                "counters": {}
            }

            if is_hash_match:
                hash_matches += 1
                j = 0
                match_ok = True
                while j < m:
                    char_comparisons += 1
                    is_match = (text[i + j] == pattern[j])
                    yield {
                        "type": "verify_char",
                        "message": f"Hash match! Verifying char text[{i+j}] ('{text[i+j]}') == pattern[{j}] ('{pattern[j]}').",
                        "state": {
                            "text": text,
                            "pattern": pattern,
                            "position": i,
                            "pattern_hash": p_hash,
                            "window_hash": t_hash,
                            "char_states": {
                                "text_index": i + j,
                                "pattern_index": j,
                                "status": "match" if is_match else "mismatch"
                            },
                            "matches": list(found_matches)
                        },
                        "counters": {"char_comparisons": 1, "hash_matches": 1}
                    }

                    if not is_match:
                        match_ok = False
                        break
                    j += 1

                if match_ok and j == m:
                    found_matches.append(i)
                    yield {
                        "type": "match_found",
                        "message": f"Verified match found at index {i}!",
                        "state": {
                            "text": text,
                            "pattern": pattern,
                            "position": i,
                            "pattern_hash": p_hash,
                            "window_hash": t_hash,
                            "matches": list(found_matches)
                        },
                        "counters": {}
                    }

            if i < n - m:
                t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
                if t_hash < 0:
                    t_hash += prime
                hash_calculations += 1

        yield {
            "type": "done",
            "message": f"Rabin-Karp complete. Found {len(found_matches)} match(es).",
            "state": {
                "text": text,
                "pattern": pattern,
                "position": n - m,
                "pattern_hash": p_hash,
                "window_hash": t_hash,
                "matches": list(found_matches)
            },
            "counters": {}
        }

    return generator(), matches