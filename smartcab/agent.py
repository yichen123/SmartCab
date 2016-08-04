import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from collections import defaultdict

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.success = 0
        self.qTable = defaultdict(int)
        self.state_0 = None

        self.discounting = 0.5
        self.learning_rate = 0.5

    def reset(self, destination=None):
        self.planner.route_to(destination)
        print 'number of success is ' + str(self.success)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        self.actions = self.env.valid_actions
        self.state = {'next_waypoint': self.next_waypoint, inputs}
        print state_pos

        # helper functions
        def randomMove():
            return random.choice(self.actions)

        def get_qValue(state, action):
            return self.qtable[str((state, action))]

        def update_qValue(state_0, action_0, reward_0, state, 
                          gamma = self.discounting, alpha = self.learning_rate):
            # using current state to update the q value of the previous state
            qValue = get_qValue(state_0, action_0)
            qValue = (1 - alpha) * qValue + alpha * reward_0
            for action in self.valid_actions:
                qValue += alpha * gamma * get_qValue(state, action)
            self.qTable[str((state_0, action_0))] = qValue

        # TODO: Update state
        
        # TODO: Select action according to your policy



        action = randomMove()

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward

        # print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.00, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=1)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
