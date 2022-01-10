# pylint: disable=missing-function-docstring,bad-staticmethod-argument,too-few-public-methods

import re

from dealership_review.utils.logger import Logger
from dealership_review.utils.http_client import HttpClient
from dealership_review.utils.scrapper import Scrapper, ScrapperElement
from dealership_review.utils.slugifier import Slugifier

from dealership_review.exceptions.http_client_exceptions import (
    HttpRequestDidNotReturnOk, HttpRequestConnectionError,
)
from dealership_review.exceptions.reviewer_exceptions import (
    OverallScoreNotFound, UnableToProcessRating,
)
from dealership_review.exceptions.scrapper_exceptions import ElementNotFound


RECOMMEND_DEALER_RATING = 'Recommend Dealer'
RECOMMEND_DEALER_YES_ANSWER = 'yes'


class DealerShipReviewScrapper:
    """
    Class intended to scrap a limited number of page reviews from the
    DealerRater website for a specific dealership.
    """

    def __init__(self):
        self.http_client = HttpClient()
        self.logger = Logger()
        self.debug_log = False

    def scrap_reviews(
            self,
            pages: int,
            dealership_url: str,
            debug_log: bool = False
    ) -> list:
        """
        Scraps through a limited number of pages reviews for a specific dealership
        The returned value is a list of dictionaries containing a score/rating
        data for each review.
        """
        self.debug_log = debug_log
        self._log('Starting scrapping reviews')
        scrapped_reviews = []

        for page_number in range(1, pages + 1):
            try:
                scrapped_reviews += self._get_reviews_for_page(dealership_url, page_number)
            except (HttpRequestDidNotReturnOk, HttpRequestConnectionError):
                if not scrapped_reviews:
                    self.logger.error('It was not possible to fetch data from DealerRater')
                    return []
            except (ElementNotFound, OverallScoreNotFound, UnableToProcessRating) as exception:
                self.logger.error(str(exception))
                return []

        self._log('Finished scrapping reviews')

        return scrapped_reviews

    def _get_reviews_for_page(self, dealership_url: str, page_number: int):
        self._log(f'Fetching review page {page_number}')

        html = self.http_client.get_html(f'{dealership_url}/page{page_number}/')

        scrapper = Scrapper(html)

        online_reviews = scrapper.find_all_elements('div', cls='review-entry')

        self._log(f'Scrapping reviews on page {page_number}')

        reviews = list(map(self._get_review_element_from_online_review, online_reviews))

        return reviews

    def _get_review_element_from_online_review(self, online_review: ScrapperElement) -> dict:
        score = {
            'reviewer': self._get_reviewer_name(online_review),
            'overall-score': self._get_overall_score(online_review),
            'employees-scores': self._get_employees_score(online_review),
        }

        score.update(self._get_specific_scores(online_review))

        return score

    @staticmethod
    def _get_reviewer_name(online_review: ScrapperElement) -> str:
        name_element = online_review.find_first_element(
            'span',
            cls='italic font-16 bolder notranslate'
        )
        return name_element.get_value()[3:]

    def _get_overall_score(self, online_review: ScrapperElement) -> int:
        elements = online_review.select_css('div.rating-static.hidden-xs')

        if not elements:
            raise OverallScoreNotFound()

        overall_review = elements[0]

        return self._get_rating_from_class(overall_review.get_class(), 'rating-')

    def _get_specific_scores(self, online_review: ScrapperElement) -> dict:
        scores = {'specific-scores': {}}
        specific_scores_table = online_review.find_first_element('div', cls='review-ratings-all')
        specific_scores = specific_scores_table.find_all_elements('div', cls='tr')

        for specific_score in specific_scores:
            specific_score_name_element = specific_score.find_first_element('div', cls='td')
            specific_score_name = specific_score_name_element.get_value()

            if specific_score_name == RECOMMEND_DEALER_RATING:
                specific_score_rating_element = specific_score_name_element.find_next_sibling(
                    'div',
                    cls='boldest',
                )
                recommend_dealer_score = Slugifier.slugify(
                    specific_score_rating_element.get_value()
                )
                scores[Slugifier.slugify(specific_score_name)] = \
                    recommend_dealer_score == RECOMMEND_DEALER_YES_ANSWER
            else:
                specific_score_rating_element = specific_score_name_element.find_next_sibling(
                    'div',
                    cls='rating-static-indv',
                )
                scores['specific-scores'][Slugifier.slugify(specific_score_name)] = \
                    self._get_rating_from_class(
                        specific_score_rating_element.get_class(),
                        'rating-'
                    )

        return scores

    def _get_employees_score(self, online_review: ScrapperElement) -> list:
        scores = []
        employees_scores_table = online_review.find_first_element('div', cls='employees-wrapper')
        employees_scores = employees_scores_table.find_all_elements('div', cls='rating-static')

        for employees_score in employees_scores:
            scores.append(self._get_rating_from_class(employees_score.get_class(), 'rating-'))

        return scores

    @staticmethod
    def _get_rating_from_class(cls: list, matching_score_string: str) -> int:
        rating_class_match = list(filter(
            lambda a: re.match(rf'\W*{matching_score_string}\D*(\d+)', a),
            cls
        ))

        if not rating_class_match:
            raise UnableToProcessRating()

        rating_class = rating_class_match[0]

        rating_match = re.findall(r'\d+', rating_class)

        if not rating_match:
            raise UnableToProcessRating()

        return int(rating_match[0])

    def _log(self, message: str):
        if self.debug_log:
            self.logger.debug(message)
