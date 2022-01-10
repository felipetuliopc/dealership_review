from dealership_review.core.mediator import Mediator

reviews = Mediator().get_scores()

print('###')
for review in reviews:
    print(review)
print('###')
