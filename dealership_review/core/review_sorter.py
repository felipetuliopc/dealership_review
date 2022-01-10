from enum import Enum


class SortType(Enum):
    """
    Enum class to define different kinds of sort types
    """
    ASC = 'asc'
    DESC = 'desc'


def sort_reviews(reviews: list, sort_type: SortType = SortType.ASC) -> list:
    """
    Method that sorts a list of reviews with the given sort type
    """
    if sort_type is SortType.ASC:
        reviews.sort(key=(lambda review: review.score))
    elif sort_type is SortType.DESC:
        reviews.sort(reverse=True, key=(lambda review: review.score))

    return reviews
