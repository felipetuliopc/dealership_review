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
                if not scrapped_reviews:
                    self.logger.error(str(exception))
                    return []

        self._log('Finished scrapping reviews')

        return scrapped_reviews

    def _get_reviews_for_page(self, dealership_url: str, page_number: int):
        self._log(f'Fetching review page {page_number}')

        html = self.http_client.get_html(f'{dealership_url}/page{page_number}/')

        scrapper = Scrapper(html)

        raw_reviews = scrapper.find_all_elements('div', cls='review-entry')

        self._log(f'Scrapping reviews on page {page_number}')

        reviews = list(map(self._get_processed_review_from_raw_review, raw_reviews))

        return reviews

    def _get_processed_review_from_raw_review(self, raw_review: ScrapperElement) -> dict:
        review = {
            'reviewer': self._get_reviewer_name(raw_review),
            'overall-score': self._get_overall_score(raw_review),
            'employees-scores': self._get_employees_score(raw_review),
            'message': self._get_message(raw_review),
        }

        review.update(self._get_specific_scores(raw_review))

        return review

    @staticmethod
    def _get_reviewer_name(raw_review: ScrapperElement) -> str:
        name_element = raw_review.find_first_element(
            'span',
            cls='italic font-16 bolder notranslate'
        )
        return name_element.get_value()[3:]

    def _get_overall_score(self, raw_review: ScrapperElement) -> int:
        overall_score_elements = raw_review.select_css('div.rating-static.hidden-xs')

        if not overall_score_elements:
            raise OverallScoreNotFound()

        overall_score_element = overall_score_elements[0]

        return self._get_score_from_element_class(overall_score_element.get_class(), 'rating-')

    def _get_employees_score(self, raw_review: ScrapperElement) -> list:
        scores = []
        employees_scores_table = raw_review.find_first_element('div', cls='employees-wrapper')
        employees_score_elements = employees_scores_table.find_all_elements(
            'div',
            cls='rating-static'
        )

        for employees_score_element in employees_score_elements:
            scores.append(self._get_score_from_element_class(
                employees_score_element.get_class(),
                'rating-'
            ))

        return scores

    @staticmethod
    def _get_message(raw_review: ScrapperElement) -> str:
        message_root_element = raw_review.find_first_element('p', cls='font-16')
        title_element = message_root_element.find_first_element('span', cls='review-title')
        whole_message_element = message_root_element.find_first_element('span', cls='review-whole')

        message = f'{title_element.get_value()} {whole_message_element.get_value()}'

        return message

    def _get_specific_scores(self, raw_review: ScrapperElement) -> dict:
        scores = {'specific-scores': {}}
        specific_scores_table_element = raw_review.find_first_element(
            'div',
            cls='review-ratings-all'
        )
        specific_scores_element = specific_scores_table_element.find_all_elements('div', cls='tr')

        for specific_score_element in specific_scores_element:
            specific_score_name_element = specific_score_element.find_first_element('div', cls='td')
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
                    self._get_score_from_element_class(
                        specific_score_rating_element.get_class(),
                        'rating-'
                    )

        return scores

    @staticmethod
    def _get_score_from_element_class(cls: list, matching_score_string: str) -> int:
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
