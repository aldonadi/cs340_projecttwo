""" Class for loading and parsing Quick Filter Button YAML data"""

class QuickFilterButton:
    def __init__(self, button_text, breeds, sex, min_age_in_weeks, max_age_in_weeks):
        self.button_text = button_text
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

        if not QuickFilterButton.is_dict_empty(age_range):
            query["age_upon_outcome_in_weeks"] = age_range

        return query



    @staticmethod
    def is_dict_empty(dict):
        return bool(dict)      # empty dicts evaluate to False

class QuickFilterButtons:

