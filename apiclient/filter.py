
class Filter:
    # TODO: change the types of the min and max dates.
    def __init__(self, min_date: str, max_date: str, show_zelfstudie=True):
        self.min_date: str = min_date
        self.max_date: str = max_date

        self.show_zelfstudie: bool = show_zelfstudie

    def filter(self, content) -> list:
        filtered: list = []
        for record in content:
            if not (self.min_date <= record["roosterdatum"] <= self.max_date):
                continue

            if (not self.show_zelfstudie) and "zelfstudie" in record["publicatietekst"].lower():
                continue

            filtered.append(record)

        return filtered
