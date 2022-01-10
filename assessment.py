from dealership_review.core.mediator import Mediator

# Tweak the search on `.get_scores()`
reviews = Mediator().get_scores()

print('###')
for review in reviews:
    print(review)
print('###')
