""" Class for loading and parsing Quick Filter Button YAML data"""

import yaml

DEFAULT_QUICK_FILTER_YAML_FILENAME="quick-filters.yml"

class QuickFilter:
    def __init__(self, filter_text, breeds, sex, min_age_in_weeks, max_age_in_weeks):
        self.filter_text = filter_text
        self.breeds = breeds
        self.sex = sex
        self.min_age_in_weeks = min_age_in_weeks
        self.max_age_in_weeks = max_age_in_weeks

    def query_json(self):
        query = {}

        age_range = {}

        if self.breeds:
            pattern = f"({'|'.join(self.breeds)})"    # => e.g. "(breed1|breed2|breed3)"
            query["breed"] = pattern

        if self.sex:
            query["sex_upon_outcome"] = self.sex

        if self.min_age_in_weeks:
            age_range["$gte"] = self.min_age_in_weeks

        if self.max_age_in_weeks:
            age_range["$tle"] = self.max_age_in_weeks

        if not QuickFilter.is_dict_empty(age_range):
            query["age_upon_outcome_in_weeks"] = age_range

        return query



    @staticmethod
    def is_dict_empty(dict):
        return bool(dict)      # empty dicts evaluate to False

class QuickFilters:

    @staticmethod
    def load(filters_yaml_file = ""):
        # load default filename if not specified in argument
        if filters_yaml_file == "":
            filters_yaml_file = DEFAULT_QUICK_FILTER_YAML_FILENAME

        # try to load the quick filters YAML file into a YAML object
        try:
            with open(filters_yaml_file, 'r') as file:
                data = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Quick filter filter YAML file '{filters_yaml_file}' not found")

        filters = []
        for entry in data:
            filter_text = entry.__name__
            breeds = entry.get('breeds')
            sex = entry.get('sex')
            min_age_in_weeks = entry.get("min-age-in-weeks")
            max_age_in_weeks = entry.get("max-age-in-weeks")

            filter = QuickFilter(filter_text, breeds, sex, min_age_in_weeks, max_age_in_weeks)
            filters.append(filter)







