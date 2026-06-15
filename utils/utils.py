def debug(content, var):
    print(f"debug: {content} {var}")
    
def generate_index(start: int, stop: int) -> list[int]:
    return list(x for x in range(start, stop))