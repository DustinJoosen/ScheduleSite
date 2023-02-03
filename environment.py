
def get_environment_rule(search_value: str) -> str:
    with open(".env", "r") as handle:
        while line := handle.readline().rstrip():
            # Check the key, and compare it
            rule: str = line[0:line.index("=")]

            if rule == search_value:
                # Return the value that corresponds to the key.
                return line[line.index("=")+1:]

    return ""  # Default value.
