__author__ = 'Austin Ouyang'

from statemachine import StateMachine
from transitions import Transitions

if __name__ == "__main__":
    m = StateMachine()

    t = Transitions()       # next state functions for state machine

    m.add_state("initialize_state", t.initialize_transitions)
    m.add_state("single_unmarked_state", t.single_unmarked_transitions)
    m.add_state("matching_pairs_in_zone_state", t.matching_pairs_in_zone_transitions)
    m.add_state("matching_pairs_in_row_state", t.matching_pairs_in_row_transitions)
    m.add_state("matching_pairs_in_col_state", t.matching_pairs_in_col_transitions)
    m.add_state("single_in_zone_state", t.single_in_zone_transitions)
    m.add_state("single_in_row_state", t.single_in_row_transitions)
    m.add_state("single_in_col_state", t.single_in_col_transitions)
    m.add_state("show_results_state", t.show_results_transitions)
    m.add_state("stuck_state", t.stuck_transitions)
    m.add_state("error_state", t.error_transitions)


    m.add_state("finished_state", None, end_state=1)

    m.set_start("initialize_state")

    filename = raw_input("Enter path of csv file: ")
    m.run(filename)


