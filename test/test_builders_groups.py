from cave_utils.builders.groups import GroupsBuilder

group_data = [
    {"continent": "North America", "country": "USA", "state": "New York"},
    {"continent": "North America", "country": "USA", "state": "California"},
    {"continent": "North America", "country": "Canada", "state": "Ontario"},
    {"continent": "Europe", "country": "France", "state": "Paris"},
    {"continent": "Europe", "country": "France", "state": "Lyon"},
    {"continent": "Europe", "country": "Germany", "state": "Berlin"},
]
group_parents = {'state': 'country', 'country': 'continent'}
group_names = {'continent': 'Continents', 'country': 'Countries', 'state': 'States'}

success = {
    "init": False,
    "double_init": False,
    "serialize": False,
    "get_id": False,
    "bad_parents": False,
    "circular_group_parents": False,
    "bad_group_data": False
}

geo_builder = GroupsBuilder(
    group_name="Geography", 
    group_data=group_data, 
    group_parents=group_parents, 
    group_names=group_names
)
success["init"] = True

try:
    geo_builder = GroupsBuilder(
        group_name="Geography", 
        group_data=group_data, 
        group_parents=group_parents, 
        group_names=group_names
    )
    success['double_init'] = True
except:
    pass

expected_output = {
    'data': {
        'continent': ['North America', 'North America', 'North America', 'Europe', 'Europe', 'Europe'],
        'country': ['USA', 'USA', 'Canada', 'France', 'France', 'Germany'],
        'id': ['0', '1', '2', '3', '4', '5'],
        'state': ['New York', 'California', 'Ontario', 'Paris', 'Lyon', 'Berlin']
    },
    'levels': {
        'continent': {'name': 'Continents'},
        'country': {'name': 'Countries', 'parent': 'continent'},
        'state': {'name': 'States', 'parent': 'country'}
    },
    'name': 'Geography',
    'order': {'data': ['continent', 'country', 'state']}
}

if geo_builder.serialize() == expected_output:
    success["serialize"] = True

if geo_builder.get_id({"continent": "North America", "country": "USA", "state": "New York"}) == "0":
    success["get_id"] = True

bad_parents = {'state_mispelled': 'country'}
circular_group_parents = {'state': 'country', 'country': 'state'}
bad_group_data = group_data + [{'bad_record': 'bad_value'}]

try:
    test_builder = GroupsBuilder(
        group_name="Geography", 
        group_data=group_data, 
        group_parents=bad_parents, 
        group_names=group_names
    )
except ValueError as e:
    success['bad_parents'] = True

try:
    test_builder = GroupsBuilder(
        group_name="Geography", 
        group_data=group_data, 
        group_parents=circular_group_parents, 
        group_names=group_names
    )
except ValueError as e:
    success['circular_group_parents'] = True


try:
    test_builder = GroupsBuilder(
        group_name="Geography", 
        group_data=bad_group_data, 
        group_parents=group_parents, 
        group_names=group_names
    )
except ValueError as e:
    success['bad_group_data'] = True

if all(success.values()):
    print("Builder Groups Tests: passed!")
else:
    print("Builder Groups Tests: Failed!")
    print(success)