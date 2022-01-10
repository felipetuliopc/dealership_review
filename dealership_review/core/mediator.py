# pylint: disable=too-few-public-methods,too-many-arguments

from dealership_review.core.dealership_review_scrapper import DealerShipReviewScrapper
from dealership_review.core.review import Review
from dealership_review.core.review_sorter import sort_reviews, SortType

from dealership_review.utils.logger import Logger


DEFAULT_REVIEWED_PAGES = 5
DEFAULT_RETURNED_REVIEWS = 3
DEFAULT_DEALERSHIP_URL = 'https://www.dealerrater.com/dealer/' \
                 'McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685'


class Mediator:
    """
    Responsible for coordinating the review scrapping, the score generation
    and sort
    """

    def __init__(self):
        self.dealership_review_scrapper = DealerShipReviewScrapper()
        self.logger = Logger()
        self.debug_log = False

    def get_scores(
            self,
            pages: int = DEFAULT_REVIEWED_PAGES,
            count: int = DEFAULT_RETURNED_REVIEWS,
            dealership_url: str = DEFAULT_DEALERSHIP_URL,
            sort_type: SortType = SortType.ASC,
            debug_log: bool = False
    ) -> list:
        """
        Scraps data from the Dealership review pages, generates Reviews from it,
        calculate their score, sort them and select the desired amount.
        """
        self.debug_log = debug_log
        self._log(f'Starting getting reviews for {dealership_url}')

        scrapped_reviews = self.dealership_review_scrapper.scrap_reviews(
            pages=pages,
            dealership_url=dealership_url,
            debug_log=debug_log
        )

        self._log(f'Finished getting reviews for {dealership_url}')

        self._log(f'Calculating scores for {len(scrapped_reviews)} reviews')

        reviews = self._map_scrapped_reviews_into_reviews(scrapped_reviews)

        sorted_reviews = sort_reviews(reviews, sort_type)

        self._log('Finished calculating scores')

        return sorted_reviews[:count]

    @staticmethod
    def _map_scrapped_reviews_into_reviews(scrapped_reviews: list) -> list:
        def to_review(scrapped_review: dict) -> Review:
            return Review(
                reviewer=scrapped_review['reviewer'],
                overall_score=scrapped_review['overall-score'],
                employees_scores=scrapped_review['employees-scores'],
                message=scrapped_review['message'],
                recommend_dealer=scrapped_review['recommend-dealer'],
                specific_scores=scrapped_review['specific-scores'],
            )

        return list(map(to_review, scrapped_reviews))

    def _log(self, message: str):  # pylint: disable=missing-function-docstring
        if self.debug_log:
            self.logger.debug(message)
