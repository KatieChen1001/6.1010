"""
6.101 Lab 3: Katie Chen
Bacon Number
"""

#!/usr/bin/env python3

import pickle

# NO ADDITIONAL IMPORTS ALLOWED!


def transform_data(raw_data):
    
    '''
     raw_data: list of 3-element tuples (actor1, actor2, film)

     transformed_data: python dictionary
     {
        'actor1' : {
            'actor2': 'film',
            'different actor2': 'film' 
        }
     }
    '''

    actor_indexed_transformed_data = dict()
    movie_indexed_transformed_data = dict()

    for actor1, actor2, film in raw_data: 
        actor_indexed_transformed_data = transform_to_actor_index(actor_indexed_transformed_data, actor1, actor2, film)
        actor_indexed_transformed_data = transform_to_actor_index(actor_indexed_transformed_data, actor2, actor1, film)
        movie_indexed_transformed_data = transform_to_movie_index(movie_indexed_transformed_data, actor1, actor2, film)
    return (actor_indexed_transformed_data, movie_indexed_transformed_data)

def transform_to_movie_index(transformed_data, actor1, actor2, film):
    if film not in transformed_data.keys():
        transformed_data[film] = {actor1, actor2}
    else: 
        if actor1 == actor2: 
            transformed_data[film].add(actor1)
        else: 
            transformed_data[film].add(actor1)
            transformed_data[film].add(actor2)
    return transformed_data

def transform_to_actor_index(transformed_data, actor1, actor2, film):
    if actor1 not in transformed_data.keys(): 
            transformed_data[actor1] = {actor2 : film}
    else: 
        if (actor2, film) not in transformed_data[actor1].items():
            transformed_data[actor1][actor2] = film
    return transformed_data

def get_actor_indexed(transformed_data): 
    return transformed_data[0]

def get_movied_indexed(transformed_data): 
    return transformed_data[1]

def acted_together(transformed_data, actor_id_1, actor_id_2):

    transformed_data = get_actor_indexed(transformed_data)
    
    if actor_id_1 == actor_id_2: 
        return True
    else:
        if actor_id_1 in transformed_data.keys(): 
            if actor_id_2 in transformed_data[actor_id_1].keys():
                return True
            else: 
                return False
        return False

def actors_with_bacon_number(transformed_data, n):

    transformed_data = get_actor_indexed(transformed_data)

    bacon_id = 4724
    bacon_previous_num = {bacon_id}
    
    i = 0
    bacon_next_num = set()
    history = bacon_previous_num
    while i < n: 
        for actor in bacon_previous_num:
            for new_actor in transformed_data[actor].keys(): 
                if new_actor not in history:
                    bacon_next_num.add(new_actor)
        if bacon_next_num == set():
            return bacon_next_num
        history.update(bacon_next_num)
        bacon_previous_num = bacon_next_num       
        bacon_next_num = set()
        i += 1 
    return bacon_previous_num

def bacon_path(transformed_data, actor_id):

    bacon_id = 4724
    return actor_to_actor_path(transformed_data, bacon_id, actor_id)

def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):


    def goal_test_for_actor_to_actor(actor_to_be_tested):
        return actor_to_be_tested == actor_id_2
    
    return actor_path(transformed_data, actor_id_1, goal_test_for_actor_to_actor)

def movie_path(transformed_data, actor_id_1, actor_id_2): 


    path = actor_to_actor_path(transformed_data, actor_id_1, actor_id_2)
    movies = []
    for index in range(len(path) - 1): 
        movies.append(transformed_data[path[index]][path[index + 1]])
    return movies

def actor_path(transformed_data, actor_id_1, goal_test_function):

    transformed_data = get_actor_indexed(transformed_data)
        
    def get_connected_actors(transformed_data, actor_id):
        # if actor_id in database, return actor's co-stars
        # else return ? 
        return set(transformed_data[actor_id].keys()) # set
    
    if goal_test_function(actor_id_1): 
        return [actor_id_1]
    
    actor_path = [(actor_id_1, )] # list

    checked_actors = {actor_id_1} # set 

    while actor_path: 
        current_path = actor_path.pop(0)
        last_actor_in_path = current_path[-1]
        connected_actors = get_connected_actors(transformed_data, last_actor_in_path)
        for connected_actor in connected_actors: 
            if connected_actor not in checked_actors and not goal_test_function(connected_actor):
                checked_actors.add(connected_actor)
                actor_path.append(current_path + (connected_actor, ))
            elif goal_test_function(connected_actor):
                path = list(current_path + (connected_actor,))
                return path

    return None

def actors_connecting_films(transformed_data, film1, film2):
    # actor_indexed = get_actor_indexed(transformed_data)
    movie_indexed = get_movied_indexed(transformed_data)
    # print(len())

    actors_in_film1 = movie_indexed[film1]
    actors_in_film2 = movie_indexed[film2]
    all_paths = []

    # print(actors_in_film1)

    for actor1 in actors_in_film1: 
        for actor2 in actors_in_film2: 
            all_paths.append(actor_to_actor_path(transformed_data, actor1, actor2))
    
    shortest_list = min(all_paths, key=len)
    if shortest_list: 
        return shortest_list
    else: 
        return None


if __name__ == "__main__":

    # with open("resources/tiny.pickle", "rb") as f:
    #     tinydb = pickle.load(f)
    # print(transform_data(tinydb)[1])
    # print(tinydb)

    # with open("resources/small.pickle", "rb") as f:
    #     smalldb = pickle.load(f)

    # with open("resources/large.pickle", "rb") as f:
    #     largedb = pickle.load(f)

    # with open("resources/names.pickle", "rb") as f:
    #     namedb = pickle.load(f)
    
    # with open("resources/movies.pickle", "rb") as f:
    #     moviedb = pickle.load(f)


    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    

    # actor1 = namedb['Kenneth McMillan']
    # actor2 = namedb['Barbra Rae']

    # print(acted_together(transform_data(smalldb), actor1, actor2))
    # print([key for key in namedb if namedb[key] == 952996])
    
    # bacon_6_large = actors_with_bacon_number(transform_data(largedb), 6)
    # print(bacon_6_large)
    # names = [key for key in namedb if namedb[key] in bacon_6_large]
    # print(names)

    # path = bacon_path(transform_data(largedb), namedb["Laura La Varnie"])
    # print([key for actor_id in path for key in namedb if namedb[key] == actor_id])
    
    # path = actor_to_actor_path(transform_data(largedb), namedb["Ollie Carlyle"], namedb["Donald Sutherland"])
    # print([key for actor_id in path for key in namedb if namedb[key] == actor_id])

    # movies = movie_path(transform_data(largedb), namedb["Kevin Rice"], namedb["Sven Batinic"])
    # print([key for movie in movies for key in moviedb if moviedb[key] == movie])

    # print(bacon_path(transform_data(tinydb), 1640))
    pass
    
