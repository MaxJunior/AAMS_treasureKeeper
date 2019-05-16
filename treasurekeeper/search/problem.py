class Problem:

    def __init__(self, state0, operator, is_goal, equals):
        """
        Class that describes a search problem.
        Arguments:
            initial_state  -- initial state of the search.
            operator -- function to obtain successor states.
            is_goal -- function to check if a state is the goal.
            equal_state -- function to verify state equality.
        """

        self.state0 = state0
        self.operator = operator
        self.is_goal = is_goal
        self.equals = equals
