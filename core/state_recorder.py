class StateRecorder:
    """
    Stores intermediate execution states of algorithms.
    """

    def __init__(self):
        self.states = []

    def record(self, state):
        self.states.append(state)

    def extend(self, states):
        self.states.extend(states)

    def get_states(self):
        return self.states

    def clear(self):
        self.states.clear()

    def count(self):
        return len(self.states)