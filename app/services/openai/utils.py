from tiktoken import Encoding, get_encoding


def count_tokens(text: str) -> int:
    cl100k_base = get_encoding('cl100k_base')

    enc = Encoding(
        name='chatgpt',
        pat_str=cl100k_base._pat_str,
        mergeable_ranks=cl100k_base._mergeable_ranks,
        special_tokens={**cl100k_base._special_tokens}
    )
    tokens = enc.encode(text)
    return len(tokens)
