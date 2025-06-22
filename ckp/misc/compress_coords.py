def compress_coords(values: list|set|dict) -> list:
    """ Compress the coordinates of the given values. """
    if not values: return []
    if isinstance(values, list): values = set(values)
    if isinstance(values, set): return sorted(values)
    else: return sorted(values.keys())