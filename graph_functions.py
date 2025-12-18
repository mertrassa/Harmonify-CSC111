"""CSC111 Project 2"""
from __future__ import annotations
import csv
from typing import Any

import networkx as nx  # Used for visualizing graphs (by convention, referred to as "nx")


class _Vertex:
    """A vertex in a song-user graph, used to represent a user or a song.

    Each vertex item is either a username or song id. Both are represented as strings,
    even though we've kept the type annotation as Any to be consistent.

    Instance Attributes:
        - key: A key used for extracting the related vertex object.
        - item: The data stored in this vertex, representing a user or a song.
                - For users, this item attribute stores a list of:
                ["username", "name", "age", "province"]
                - For songs, this item attribute stores a list of:
                ["song_id", "song_name", "artist" "duration (in ms)", "genre"]
        - kind: The type of this vertex: 'user' or 'song'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'song'}
        - all(isinstance(x, str) for x in self.item)
    """

    key: Any
    item: Any
    kind: str
    neighbours: set[_Vertex]

    def __init__(self, key: Any, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given key, item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'song'}
        """
        self.key = key
        self.item = item
        self.kind = kind
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def similarity_score(self, other: _Vertex, genre: str, duration: str) -> float:
        """
        Return the similarity score between this vertex and the other.
        Similarity score is calculated by finding;
         - the number of common songs listened by this user and the other user,
         - the number of songs that 1) this user and the other user listens and
         2) matches with this user's favourite genre.
         - the number of songs that 1) this user and the other user listens and
         2) duration of the song matches with this user's preferred duration.

         after calculating these values, we find the similarity_score by
         "number_of_common_songs * 3 + number_of_common_genres * 2 + number_of_common_duration * 1" formula

         Preconditions:
            - self.kind == 'user' and other.kind == 'user'
            - self != other

        """
        number_of_common_songs = 0
        number_of_common_genres = 0
        number_of_common_duration = 0

        for v1 in self.neighbours:
            for v2 in other.neighbours:
                if v1 == v2:
                    number_of_common_songs += 1
                    if genre.lower() == v2.item[4]:
                        number_of_common_genres += 1

                    if int(v2.item[3]) < 120000 and duration.lower() == "short":
                        number_of_common_duration += 1

                    elif int(v2.item[3]) <= 480000 and int(v2.item[3]) >= 120000 and duration.lower() == "medium":
                        number_of_common_duration += 1

                    elif int(v2.item[3]) > 480000 and duration.lower() == "long":
                        number_of_common_duration += 1

        return number_of_common_songs * 3 + number_of_common_genres * 2 + number_of_common_duration * 1


class Graph:
    """A graph used to represent a user-song network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, key: Any, item: Any, kind: str) -> None:
        """Add a vertex with the given key, item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'song'}
        """
        if key not in self._vertices:
            self._vertices[key] = _Vertex(key, item, kind)

    def add_edge(self, key1: Any, key2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if key1 or key2 do not appear as vertices in this graph.

        Preconditions:
            - key1 != key2
        """
        if key1 in self._vertices and key2 in self._vertices:
            v1 = self._vertices[key1]
            v2 = self._vertices[key2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, key1: Any, key2: Any) -> bool:
        """Return whether key1 and key2 are adjacent vertices in this graph.

        Return False if key1 or key2 do not appear as vertices in this graph.
        """
        if key1 in self._vertices and key2 in self._vertices:
            v1 = self._vertices[key1]
            return any(v2.key == key2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, key: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if key in self._vertices:
            v = self._vertices[key]
            return {neighbour.key for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'book'}
        """
        if kind != '':
            return {v.key for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.key, kind=v.kind)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.key, kind=u.kind)

                if u.key in graph_nx.nodes:
                    graph_nx.add_edge(v.key, u.key)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx

    def get_similarity_score(self, item1: Any, item2: Any, genre: str, duration: str) -> float:
        """Return the similarity score between the two given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.
        """
        if (item1 not in self._vertices) or (item2 not in self._vertices):
            raise ValueError

        else:
            return self._vertices[item1].similarity_score(self._vertices[item2], genre, duration)

    def compatible_user_rec_songs(self, user: str, genre: str, duration: str) -> list[list]:
        """
        Return the 1) recommended user's item based on similarity to the given user
        considering genre and duration and 2) The songs both users have in common and recommended songs.
        lst[0] in the returned list of list is the features of the recommended user,
        formatted as:
        ["username", "name", "age", "province"]
        2) The songs both users have in common, and recommended songs.

        The returned list should NOT contain:
            - any user with a similarity score of 0 to the input user

        Preconditions:
            - user in self._vertices
            - self._vertices[user].kind == 'user'
        """

        all_users = {}
        scores = []

        for u in self._vertices:
            if self._vertices[u].kind == 'user' and u != user:
                score = self.get_similarity_score(user, u, genre, duration)
                if score > 0:
                    scores.append(score)
                    if score in all_users:
                        all_users[score] = all_users[score] + [u]
                    else:
                        all_users[score] = [u]

        scores.sort()
        max_score = scores.pop()
        # The user at the first index is returned
        # if there are multiple users with the same compatibility score.
        user_parameters = self._vertices[all_users[max_score][0]].item  # ["username", "name", "age", "province"]

        recommended_songs = []
        both_songs_you_listen = []
        songs_user_listen = []

        for s1 in self._vertices[user].neighbours:
            songs_user_listen = songs_user_listen + [s1.item[1]]

        for s2 in self._vertices[user_parameters[0]].neighbours:
            if s2.item[1] in songs_user_listen:
                both_songs_you_listen = both_songs_you_listen + [s2.item[1]]
            else:
                recommended_songs = recommended_songs + [s2.item[1]]

        return [user_parameters, [both_songs_you_listen, recommended_songs], [max_score]]


def load_review_graph(users: str, songs: str) -> Graph:
    """Return a user-song graph corresponding to the given datasets.

    The user-song graph stores all the information from user_data_all and songs_sorted_by_popularity as follows:
    Create one vertex for each user, AND one vertex for each unique song in the dataset.
    An edge is created between the user and song vertex if the user listens to that song.

    The vertices of the 'user' kind should have the username as its key.
    The vertices of the 'song' kind representing each reviewed book should have the song id as its key (you should
     use the book_names_file to find the book title associated with each book id).

    Use the "kind" _Vertex attribute to differentiate between the two vertex types.

    Preconditions:
        - reviews_file is the path to a CSV file corresponding to the book review data
          format described on the assignment handout
        - book_names_file is the path to a CSV file corresponding to the book data
          format described on the assignment handout
        - each book ID in reviews_file exists as a book ID in book_names_file

    """

    gr = Graph()
    all_songs = {}
    with open(songs, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            all_songs[row[0]] = row

    with open(users, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            gr.add_vertex(row[0], row[:4], "user")
            gr.add_vertex(row[4], all_songs[row[4]], "song")
            gr.add_edge(row[0], row[4])
    return gr


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts

    # python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136'],
        'extra-imports': ['csv', 'networkx'],
        'allowed-io': ['load_review_graph'],
        'max-nested-blocks': 4
    })
