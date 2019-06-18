import redis
import config
import pickle


class CandidateDbInterface:
    """
    Interface for Candidate and Redis
    """
    def __init__(self, candidate_id, prepend_string="trivia"):
        self.host = config.REDIS_HOST
        self.port = config.REDIS_PORT
        self.password = config.REDIS_PASS
        self.candidate_id = candidate_id
        self.r = redis.StrictRedis(host=self.host, password=self.password, port=self.port, ssl=True)
        self.prepend_string = prepend_string
        self.redis_key = f"{self.prepend_string}_candidate_{candidate_id}"

    def store_candidate(self, candidate_obj):
        """
        Store candidate object in Redis
        :param candidate_obj: Candidate Object
        :return: True/False based on success
        """
        try:
            picked_candidate = pickle.dumps(candidate_obj)
            self.r.set(self.redis_key, picked_candidate)
            return True
        except Exception as err:
            print(str(err))
            return False

    def get_candidate(self):
        """
        Fetches candidate from Redis
        :return: True if successfully retrieved, False if retrieval failed.
        """
        try:
            unpacked_candidate = pickle.loads(self.r.get(self.redis_key))
            return unpacked_candidate
        except TypeError:
            print("Candidate not found...")
            return None

    def delete_candidate(self):
        """
        Delete's candidate from Redis
        :return: True if delete successful, False if failed for some reason.
        """
        try:
            self.r.delete(self.redis_key)
            return True
        except Exception as err:
            print(err)
            return False



