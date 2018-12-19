import csv

from generator.AnalyticsModel.history_action_type import HistoryActionType

TIMESTAMP_COLUMN_NAMES = {HistoryActionType.SEARCH: "searchDatetime", HistoryActionType.CLICK: "clickDatetime"}
VALUE_COLUMN_NAMES = {HistoryActionType.SEARCH: ["queryExpression"], HistoryActionType.CLICK: ["documentUrl", "documentTitle"]}


def extract_history_actions(csv_path, action_type, history):
    with open(csv_path, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, escapechar="\\")
        headers = next(csv_reader)
        user_id_column_index = headers.index("userId")
        timestamp_column_index = headers.index(TIMESTAMP_COLUMN_NAMES[action_type])
        value_column_indices = {
            value_column_name: headers.index(value_column_name)
            for value_column_name in VALUE_COLUMN_NAMES[action_type]
        }
        for row in csv_reader:
            user_id = row[user_id_column_index]
            timestamp = row[timestamp_column_index]
            value = {
                value_column_name: row[value_column_indices[value_column_name]]
                for value_column_name in VALUE_COLUMN_NAMES[action_type]
            }
            action = HistoryAction(timestamp, action_type, value)
            if user_id not in history:
                history[user_id] = [action]
            else:
                history[user_id].append(action)


def get_history(searches_file_path, clicks_file_path):
    raw_history = {}
    extract_history_actions(searches_file_path, HistoryActionType.SEARCH, raw_history)
    extract_history_actions(clicks_file_path, HistoryActionType.CLICK, raw_history)

    sorted_history = {}
    for user_id, actions in raw_history.items():
        sorted_history[user_id] = sorted(actions, key=lambda history_action: history_action.timestamp)
    return sorted_history


class HistoryAction(object):
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __init__(self, timestamp, action_type, value):
        self.timestamp = timestamp
        self.action_type = action_type
        self.value = value
