from pamda import pamda
import type_enforced
from datetime import datetime, timedelta

class GroupsUtils:
    def serialize(self):
        return {
            'name': self.group_name,
            'order': {
                'data': self.group_keys
            },
            'data': self.data_structure,
            'levels': self.levels_structure
        }
        
@type_enforced.Enforcer
class GroupsBuilder(GroupsUtils):
    def __init__(self, group_name:str, group_data:list[dict[str]]) -> None:
        self.group_name = group_name
        self.group_keys = list(group_data[0].keys())
        self.validate_group_data(group_data = group_data)
        self.gen_structures(group_data=group_data)


    def validate_group_data(self, group_data):
        for record in group_data:
            if list(record.keys()) != self.group_keys:
                raise ValueError("Group data must have the same keys in the same order for all records.")
            
    def gen_structures(self, group_data):
        groups = [i[0] for i in pamda.groupKeys(keys=self.group_keys, data=group_data)]
        self.id_structure = {}
        for idx, group in enumerate(groups):
            idx = str(idx)
            self.id_structure = pamda.assocPath(path=list(group.values()), value=idx, data=self.id_structure)
            group['id']=idx
        self.data_structure = pamda.pivot(groups)
        
        self.levels_structure = {}
        for idx, key in enumerate(self.group_keys):
            self.levels_structure[key] = {
                "name": key.replace("_", " ").replace('-',' ').title(),
            }
            if idx > 0:
                self.levels_structure[key]["parent"] = self.group_keys[idx-1]
        
    def get_id(self, group:dict[str]):
        return pamda.path(path=pamda.props(self.group_keys, group), data=self.id_structure)
    
@type_enforced.Enforcer
class DateGroupsBuilder(GroupsUtils):
    def __init__(
        self,
        group_name:str, 
        date_data:list[str], 
        date_format:str="%Y-%m-%d", 
        include_year:bool=True,
        include_year_month:bool=True,
        include_year_month_day:bool=True,
        include_year_week:bool=False,
        include_year_day:bool=False,
        include_month:bool=True,
        include_month_week:bool=False,
        include_month_day:bool=False,
        include_week_day:bool=True
    ) -> None:
        self.group_name = group_name
        self.date_format = date_format
        self.include_year = include_year
        self.include_year_month = include_year_month
        self.include_year_month_day = include_year_month_day
        self.include_year_week = include_year_week
        self.include_year_day = include_year_day
        self.include_month = include_month
        self.include_month_week = include_month_week
        self.include_month_day = include_month_day
        self.include_week_day = include_week_day
        self.date_objects = self.get_date_objects(date_data=date_data)
        self.gen_structures()

    def get_date_objects(self, date_data):
        date_objects_raw = [datetime.strptime(date, self.date_format) for date in date_data]
        max_date = max(date_objects_raw)
        min_date = min(date_objects_raw)
        date_objects = [min_date + timedelta(days=i) for i in range((max_date - min_date).days+1)]
        return date_objects
    
    def gen_structures(self):
        self.data_structure = {
            "id": [i.strftime(self.date_format) for i in self.date_objects],
        }
        self.levels_structure = {}
        self.group_keys = []
        if self.include_year:
            self.levels_structure["year"] = {
                "name": "Year",
                "ordering": sorted(list(set([i.year for i in self.date_objects])))
            }
            self.data_structure["year"] = [i.year for i in self.date_objects]
            self.group_keys.append("year")
        if self.include_year_month:
            self.levels_structure["year_month"] = {
                "name": "Year Month",
                "ordering": sorted(list(set([i.strftime("%Y-%m") for i in self.date_objects])))
            }
            self.data_structure["year_month"] = [i.strftime("%Y-%m") for i in self.date_objects]
            self.group_keys.append("year_month")
        if self.include_year_month_day:
            self.levels_structure["year_month_day"] = {
                "name": "Year Month Day",
                "ordering": sorted(list(set([i.strftime("%Y-%m-%d") for i in self.date_objects])))
            }
            self.data_structure["year_month_day"] = [i.strftime("%Y-%m-%d") for i in self.date_objects]
            self.group_keys.append("year_month_day")
        if self.include_year_week:
            self.levels_structure["year_week"] = {
                "name": "Year Week",
                "ordering": sorted(list(set([i.strftime("%Y-%U") for i in self.date_objects])))
            }
            self.data_structure["year_week"] = [i.strftime("%Y-%U") for i in self.date_objects]
            self.group_keys.append("year_week")
        if self.include_year_day:
            self.levels_structure["year_day"] = {
                "name": "Year Day",
                "ordering": sorted(list(set([i.strftime("%Y-%j") for i in self.date_objects])))
            }
            self.data_structure["year_day"] = [i.strftime("%Y-%j") for i in self.date_objects]
            self.group_keys.append("year_day")
        if self.include_month:
            self.levels_structure["month"] = {
                "name": "Month",
                "ordering": sorted(list(set([i.strftime("%m") for i in self.date_objects])))
            }
            self.data_structure["month"] = [i.strftime("%m") for i in self.date_objects]
            self.group_keys.append("month")
        if self.include_month_week:
            self.levels_structure["month_week"] = {
                "name": "Month Week",
                "ordering": sorted(list(set([i.strftime("%m-%U") for i in self.date_objects])))
            }
            self.data_structure["month_week"] = [i.strftime("%m-%U") for i in self.date_objects]
            self.group_keys.append("month_week")
        if self.include_month_day:
            self.levels_structure["month_day"] = {
                "name": "Month Day",
                "ordering": sorted(list(set([i.strftime("%m-%d") for i in self.date_objects])))
            }
            self.data_structure["month_day"] = [i.strftime("%m-%d") for i in self.date_objects]
            self.group_keys.append("month_day")
        if self.include_week_day:
            self.levels_structure["week_day"] = {
                "name": "Week Day",
                "ordering": sorted(list(set([i.strftime("%w") for i in self.date_objects])))
            }
            self.data_structure["week_day"] = [i.strftime("%w") for i in self.date_objects]
            self.group_keys.append("week_day")

    def get_id(self, *args, **kwargs):
        raise NotImplementedError("This function is not supported with date Groupss.")

