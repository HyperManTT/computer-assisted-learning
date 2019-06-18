from catsim.initialization import *
from catsim.selection import *
from catsim.estimation import *
from catsim.stopping import *
import numpy
from questions import questions
from redis_interface import CandidateDbInterface


def get_question_parameters():
    """
    Retrieve question parameters from question JSON - This method can be implemented on the client side.
    :return: :type:List - List containing question params
    """
    question_parameters = []
    for q in questions:
        question_parameters.append([
            q['parameters']['discrimination'],
            q['parameters']['difficulty'],
            q['parameters']['pseudo-guessing'],
            q['parameters']['upper-asymptote'],
            q['parameters']['item-count']
        ])
    return question_parameters


def get_user_profile(_id):
    """
    Retrieve the candidate's profile via their ID
    :param _id: Candidate's ID
    :return: Candidate Object
    """
    return CandidateDbInterface(_id).get_candidate()


def store_user_profile(candidate_obj):
    """
    Store the user profile in Redis
    :param candidate_obj: The candidate object that is being stored
    :return: True if user was stored/False if storage failed
    """
    CandidateDbInterface(candidate_obj.id).store_candidate(candidate_obj)


def delete_user_profile(_id):
    """
    Delete a candidate from Redis based on their id
    :param _id: Candidate ID
    :return: True is deletion was successful/ False if deletion failed.
    """
    CandidateDbInterface(_id).delete_candidate()


class Candidate:
    """
    Candidate class representing a test/trivia taker.
    """
    def __init__(self, _id, question_parameters):
        self.id = _id
        self.responses = []
        self.administered_items = []
        self.initializer = RandomInitializer()
        self.selector = MaxInfoSelector()
        self.estimator = HillClimbingEstimator()
        self.stopper = MaxItemStopper(4)
        self.items = question_parameters
        self.est_theta = self.initializer.initialize()
        self.new_theta = self.est_theta

    def get_new_theta(self):
        self.new_theta = self.estimator.estimate(items=self.items, administered_items=self.administered_items,
                                                 response_vector=self.responses, est_theta=self.est_theta)
        return self.new_theta

    def get_next_question(self):
        """
        Fetches the next applicable question based on previous questions/answers
        :return: Question Index to ask
        """
        if not self.new_theta:
            self.get_new_theta()
        if len(self.responses) != 0:
            self.new_theta = self.get_new_theta()
        question_index = self.selector.select(items=self.items, administered_items=self.administered_items,
                                              est_theta=self.new_theta)
        return question_index

    def store_result(self, question: int, result: bool):
        """
        Save the user's answer to a question
        :param question: Question Index
        :param result: True/False
        :return: None
        """
        self.administered_items.append(question)
        self.responses.append(result)

    def remove_incorrect_answers(self):
        """
        Removes all incorrect answers from the response list. This enables the algorithm to ask previous questions,
        which the user would have gotten incorrect, again.
        :return: None
        """
        indices = []
        for i in range(len(self.responses)):
            # Store locations of all incorrect responses
            if self.responses[i] is False:
                indices.append(i)
        if len(indices) > 0:
            responses = []
            for idx, val in enumerate(self.responses):
                if idx not in indices:
                    responses.append(val)
            self.responses = responses

            administered_items = []
            for idx, val in enumerate(self.administered_items):
                if idx not in indices:
                    administered_items.append(val)
            self.administered_items = administered_items


# ###################################### Sample Usage ######################################

# Get question parameters and convert to numpy array
question_params = get_question_parameters()  # This can be done on the client side - fetch question parameters
bank_size = len(question_params)
question_params = numpy.array(question_params)
# question_params = generate_item_bank(3)

# Try to get candidate and if they aren't present, create one
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

# Simulate getting the next question to ask and storing the results in the user profile
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

