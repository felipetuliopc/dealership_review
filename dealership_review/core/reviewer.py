# pylint: disable=too-few-public-methods

from dealership_review.core.dealership_review_scrapper import DealerShipReviewScrapper

from dealership_review.utils.logger import Logger


REVIEWED_PAGES = 5
DEALERSHIP_URL = 'https://www.dealerrater.com/dealer/' \
                 'McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685'


class Reviewer:
    """
    Responsible for scrapping a limited review pages from a dealership
    in DealerRater, convert those reviews into a score and return
    some in given criteria
    """

    def __init__(self):
        self.dealership_review_scrapper = DealerShipReviewScrapper()
        self.logger = Logger()
        self.debug_log = False

    def get_review(
            self,
            pages: int = REVIEWED_PAGES,
            dealership_url: str = DEALERSHIP_URL,
            debug_log: bool = False
    ) -> list:
        """
        pass
        """
        self.debug_log = debug_log
        self._log(f'Starting getting reviews for {dealership_url}')

        scrapped_reviews = self.dealership_review_scrapper.scrap_reviews(
            pages=pages,
            dealership_url=dealership_url,
            debug_log=debug_log
        )

        self._log(f'Finished getting reviews for {dealership_url}')

        return scrapped_reviews

    def _log(self, message: str):  # pylint: disable=missing-function-docstring
        if self.debug_log:
            self.logger.debug(message)
