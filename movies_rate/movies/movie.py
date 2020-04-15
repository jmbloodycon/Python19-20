from typing import List


class Movie:
    def __init__(self, name: str, year: int) -> None:
        self.name = name
        self.year = year
        self.overall_rating = 0
        self.comments: List[str] = []
        self.number_rated = 0

    def add_comment(self, comment: str) -> None:
        self.comments.append(comment)

    def rate_film(self, appraisal: int) -> None:
        self.overall_rating += appraisal
        self.number_rated += 1

    def get_rating(self) -> float:
        if self.overall_rating == 0 or self.number_rated == 0:
            return 0.0

        return self.overall_rating / self.number_rated

    def get_comments_count(self) -> int:
        return len(self.comments)
