from collections import defaultdict
from itertools import dropwhile

from generator.AnalyticsModel.history_action_type import HistoryActionType


def get_search_to_clicks_mapping(history):
    search_to_clicks_mapping = defaultdict(set)
    for actions in history.values():
        _update_search_to_clicks_mapping(actions, search_to_clicks_mapping)
    return search_to_clicks_mapping


def _update_search_to_clicks_mapping(actions, search_to_clicks_mapping):
    last_search = None
    last_click = None
    actions_starting_at_first_search = dropwhile(lambda x: x.action_type != HistoryActionType.SEARCH, actions)
    for action in actions_starting_at_first_search:
        if action.action_type == HistoryActionType.SEARCH and last_click:
            search_to_clicks_mapping[last_search].add(last_click)
            last_click = None
        last_search = action.value if action.action_type == HistoryActionType.SEARCH else last_search
        last_click = action.value if action.action_type == HistoryActionType.CLICK else last_click
    if last_click:
        search_to_clicks_mapping[last_search].add(last_click)
