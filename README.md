## CAL Trivia - Adaptive Based Testing

```python
from catsim.initialization import *
from catsim.selection import *
from catsim.estimation import *
from catsim.stopping import *
import numpy
from questions import questions
from redis_interface import CandidateDbInterface
from candidate import Candidate, get_question_parameters, get_user_profile, store_user_profile, delete_user_profile

# Get question parameters and convert to numpy array
question_params = get_question_parameters()  # This can be done on the client side - fetch question parameters
bank_size = len(question_params)
question_params = numpy.array(question_params)
# question_params = generate_item_bank(3)
```


#### Try to fetch candidate from Redis. If they aren't present, create one
```
username = 'rram'
candidate = get_user_profile(username)
if not candidate:
    print("Creating candidate")
    candidate = Candidate(username, question_params)
else:
    # When a candidate is retrieved, remove their previously incorrect answers so it goes back into the question bank
    candidate.remove_incorrect_answers()
    print(candidate.administered_items)
    print(candidate.responses)
    print("Found user in storage.")
```


#### Simulate getting the next question to ask and storing the results in the user profile
```
import random

# Iterate over the remaining questions and get the next question
for i in range(bank_size - len(candidate.responses)):
    question_number = candidate.get_next_question()
    candidate.store_result(question_number, random.choice([True, False]))

print(candidate.administered_items)  # Questions that were asked
print(candidate.responses)  # Candidate responses - True/False based on correctness

# Store user profile for next time
store_user_profile(candidate)

# Delete user from database
print("Deleting user")
delete_user_profile(username)
```