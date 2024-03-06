import regex

def get_regex_group(pattern: str, string: str, group_index: int=1):
    match = regex.search(pattern, string)
    return match.group(group_index)