import pandas as pd


class Filter:
    def __init__(self, active=True):
        self.active = active  # Enable filtering
        self.filter_select = {}  # Column: [List of selected items]
        self.filter_date_time = {}  # Column: (from, to)

        self.max_number_of_elements = None
        self.max_number_from_tail = False

    def set_max_number_of_elements(self, max_number_of_elements, max_number_from_tail=False):
        self.max_number_of_elements = max_number_of_elements
        self.max_number_from_tail = max_number_from_tail

    def get_filter_date_from(self, column):
        if self.filter_date_time[column]:
            dates = self.filter_date_time[column]
            return dates[0]
        else:
            return None

    def get_filter_date_to(self, column):
        if self.filter_date_time[column]:
            dates = self.filter_date_time[column]
            return dates[1]
        else:
            return None

    def select(self, column, item):
        if column in self.filter_select.keys():
            existing_list = self.filter_select[column]
            existing_list.append(item)
            self.filter_select[column] = existing_list
        else:
            self.filter_select[column] = [item]

    def deselect(self, column, item):
        if column in self.filter_select.keys():
            existing_list = self.filter_select[column]
            if item in existing_list:
                index = existing_list.index(item)
                del existing_list[index]
                self.filter_select[column] = existing_list

    def select_date_range(self, column, date_from, date_to):
        self.filter_date_time[column] = (date_from, date_to)

    def deselect_date_range(self, column):
        _ = self.filter_date_time.pop(column, None)

    def filter(self, data_frame):
        df = data_frame.copy()
        # If filtering is inactive then just return passed data frame
        if not self.active:
            return df
        # Initialize empty result
        result = pd.DataFrame(columns=df.columns)
        # # If no item is selected return empty data frame
        # if not self.filter_select:
        #     return result
        # ToDo: Add check if configured filter fits to data frame columns
        relevant = None
        # Filter selections
        # Loop through all columns
        for column, itm_list in self.filter_select.items():
            # Initialize item selection with False
            # ToDo: Fix this temporary solution: Do not compare to dummy string!
            relevant_items = (df[column] == "___dummy___")
            # Loop through selected items in column
            for itm in itm_list:
                relevant_items = relevant_items | (df[column] == itm)
            if relevant is None:
                # Initialize if its still None
                relevant = relevant_items
            else:
                # Add logic connection to new column filter
                relevant = relevant & relevant_items
            result = df.loc[relevant]

        # Filter time span
        for column, itm in self.filter_date_time.items():
            if relevant is None:
                # Initialize if its still None
                result = df.loc[df[column] >= itm[0]]
            else:
                # Add logic connection to new column filter
                result = result.loc[df[column] >= itm[0]]
            result = result.loc[result[column] <= itm[1]]

        # Filter maximum number of items if configured
        if self.max_number_of_elements != None:
            if self.max_number_from_tail:
                result = result.tail(self.max_number_of_elements)
            else:
                result = result.head(self.max_number_of_elements)
        return result

    def check_if_selected(self, column, item_list):
        result = []
        for itm in item_list:
            if (column in self.filter_select.keys()) and (itm in self.filter_select[column]):
                result.append(True)
            else:
                result.append(False)
        return result
