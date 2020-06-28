import googlemaps
import polyline
import gmplot
import os
from collections import deque, namedtuple
from collections import defaultdict

apikey = 'AIzaSyC4my9ZMi0RiUXYdWqsexT4JSwSbULFnLE'
gmaps = googlemaps.Client(key=apikey)

uM = "University_Malaya"
tbs = "Terminal_Bersepadu_Selatan"
ps = "Penang_Sentral"
psahf = "Pangkalan_Sultan_Abdul_Halim_Ferry"
pp = "Pulau_Penang_Ferry_Terminal"
qb = "Queens_Bay_Mall"
klC = "Kuala_Lumpur_Sentral"
klia = "Kuala_Lumpur_International_Airport"
pia = "Penang_International_Airport"
kbw = "KTM_Butter_Worth"
locations = [uM, tbs, ps, psahf, pp, qb, klC, klia, pia, kbw]

gUM = gmaps.geocode(uM)  # to find the info about UM
initLat = gUM[0]['geometry']['location']['lat']  # lat for UM
initLng = gUM[0]['geometry']['location']['lng']  # lng for UM
# print(location[0][0]['address_components'][0]['long_name'])
# print(location[0][0]['formatted_address'])
# get lats and lngs
lats = [];
lngs = [];
for place in locations:
    placeObject = gmaps.geocode(place)
    lat = placeObject[0]['geometry']['location']['lat']
    lng = placeObject[0]['geometry']['location']['lng']
    lats.append(lat)
    lngs.append(lng)
# All Points Distance
# 0
umtbsDriveDist = (gmaps.distance_matrix(uM, tbs, mode='driving'))['rows'][0]['elements'][0]['distance'][
    'value']  # value in unit 'm'
# 1
umklCDriveDist = (gmaps.distance_matrix(uM, klC, mode='driving'))['rows'][0]['elements'][0]['distance']['value']
# 2
umklCBusDist = \
    (gmaps.distance_matrix(uM, klC, mode='transit', transit_mode='bus'))['rows'][0]['elements'][0]['distance']['value']
# 3
tbspsBusDist = \
    (gmaps.distance_matrix(tbs, ps, mode='transit', transit_mode='bus'))['rows'][0]['elements'][0]['distance']['value']
# 4
pspsahfWalkDist = (gmaps.distance_matrix(ps, psahf, mode='walking'))['rows'][0]['elements'][0]['distance']['value']
# 5
ppqbDriveDist = (gmaps.distance_matrix(pp, qb, mode='driving'))['rows'][0]['elements'][0]['distance']['value']
# 6
ppqbBusDist = (gmaps.distance_matrix(pp, qb, mode='transit', transit_mode='bus'))['rows'][0]['elements'][0]['distance'][
    'value']
# 7
klCkbwTrainDist = \
    (gmaps.distance_matrix(klC, kbw, mode='transit', transit_mode='train'))['rows'][0]['elements'][0]['distance'][
        'value']
# 8
klCkliaTrainDist = \
    (gmaps.distance_matrix(klC, klia, mode='transit', transit_mode='train'))['rows'][0]['elements'][0]['distance'][
        'value']
# 9
piaqbDriveDist = (gmaps.distance_matrix(pia, qb, mode='driving'))['rows'][0]['elements'][0]['distance']['value']
# 10
kbwqbDriveDist = (gmaps.distance_matrix(kbw, qb, mode='driving'))['rows'][0]['elements'][0]['distance']['value']
# 11
kbwpsahfWalkDist = (gmaps.distance_matrix(kbw, psahf, mode='walking'))['rows'][0]['elements'][0]['distance']['value']
# 12
psahfppFerryDist = \
    (gmaps.distance_matrix((lats[3], lngs[3]), (lats[4], lngs[4]), mode='walking'))['rows'][0]['elements'][0][
        'distance'][
        'value']
# 13
kliapiaFlightDist = \
    (gmaps.distance_matrix((lats[7], lngs[7]), (lats[8], lngs[8]), mode='walking'))['rows'][0]['elements'][0][
        'distance'][
        'value']


################Start: Find Routes Using Polyline Decode! ###################
def plotRoute(origin, destination, mode, transit_mode=None):
    evaLats = []  # decoded polylines' lats
    evaLons = []  # decoded polylines' lngs
    route = gmaps.directions(origin, destination, mode=mode, transit_mode=transit_mode)
    for i in range(len(route[0]['legs'][0]['steps'])):
        poly = route[0]['legs'][0]['steps'][i]['polyline']['points']
        decoded = polyline.decode(poly)  # decoded into list of lats and lngs
        for k in range(len(decoded)):
            evaLats.append(decoded[k][0])
            evaLons.append(decoded[k][1])
    return evaLats, evaLons;


def getAllLatsNLons():
    listEvaLats = []
    listEvaLons = []
    # define all routes, total 14 paths
    # 0
    lat, lng = plotRoute(uM, tbs, mode='driving')
    listEvaLats.append(lat)
    listEvaLons.append(lng)
    # 1
    lat, lng = plotRoute(uM, klC, mode='driving')
    listEvaLats.append(lat)
    listEvaLons.append(lng)
    # 2
    lat, lng = plotRoute(uM, klC, mode='transit', transit_mode='bus')
    listEvaLats.append(lat)
    listEvaLons.append(lng)
    # 3
    lat, lng = plotRoute(tbs, ps, mode='transit', transit_mode='bus')
    listEvaLats.append(lat)
    listEvaLons.append(lng)
    # 4
    lat, lng = plotRoute(ps, psahf, mode='walking')
    listEvaLats.append(lat)
    listEvaLons.append(lng)
    # 5
    lat, lng = plotRoute(pp, qb, mode='driving')
    listEvaLats.append(lat)
    listEvaLons.append(lng)
    # 6
    lat, lng = plotRoute(pp, qb, mode='transit', transit_mode='bus')
    listEvaLats.append(lat)
    listEvaLons.append(lng)
    # 7
    lat, lng = plotRoute(klC, kbw, mode='transit', transit_mode='train')
    listEvaLats.append(lat)
    listEvaLons.append(lng)
    # 8
    lat, lng = plotRoute(klC, klia, mode='transit', transit_mode='train')
    listEvaLats.append(lat)
    listEvaLons.append(lng)
    # 9
    lat, lng = plotRoute(pia, qb, mode='driving')
    listEvaLats.append(lat)
    listEvaLons.append(lng)
    # 10
    lat, lng = plotRoute(kbw, qb, mode='driving')
    listEvaLats.append(lat)
    listEvaLons.append(lng)
    # 11
    lat, lng = plotRoute(kbw, psahf, mode='walking')
    listEvaLats.append(lat)
    listEvaLons.append(lng)

    # 12 ferry qsahf -> pp
    listEvaLats.append([lats[3], lats[4]])
    listEvaLons.append([lngs[3], lngs[4]])

    # 13 flight klia -> pia
    listEvaLats.append([lats[7], lats[8]])
    listEvaLons.append([lngs[7], lngs[8]])

    return listEvaLats, listEvaLons


################End: Find Routes Using Polyline Decode! ###################

######################Start of Finding All Paths codes######################################
# This class represents a directed graph
# using adjacency list representation
class GraphAllPath:

    def __init__(self, vertices):
        # No. of vertices
        self.V = vertices

        # default dictionary to store graph
        self.graph = defaultdict(list)

        # function to add an edge to graph

    def addEdge(self, u, v):
        self.graph[u].append(v)

    '''A recursive function to print all paths from 'u' to 'd'. 
    visited[] keeps track of vertices in current path. 
    path[] stores actual vertices and path_index is current 
    index in path[]'''

    def printAllPathsUtil(self, u, d, visited, path, result):

        # Mark the current node as visited and store in path
        visited[u] = True
        path.append(u)

        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            result.append(
                path.copy())  # refer: https://stackoverflow.com/questions/52480524/appending-an-empty-list-with-list-in-recursive-function

        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.graph[u]: #every possible for u to v --> O(n)
                if visited[i] == False: #if haven't visit, go visit
                    self.printAllPathsUtil(i, d, visited, path, result) #--> O(n)

                    # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u] = False #Refalse it to go back previous node

    # Prints all paths from 's' to 'd'
    def printAllPaths(self, s, d):
        result = []
        # Mark all the vertices as not visited
        visited = [False] * (self.V)

        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        self.printAllPathsUtil(s, d, visited, path, result)
        return result

    # Create a graph given in the above diagram

    def getAllPath(self, allPathinNum):

        uM = "University_Malaya"
        uM_Bus = "University_Malaya_Bus"
        uM_Drive = "University_Malaya_Drive"
        tbs = "Terminal_Bersepadu_Selatan"
        ps = "Penang_Sentral"
        psahf = "Pangkalan_Sultan_Abdul_Halim_Ferry"
        pp_Bus = "Pulau_Penang_Ferry_Terminal_Bus"
        pp_Drive = "Pulau_Penang_Ferry_Terminal_Drive"
        qb = "Queens_Bay_Mall"
        klC = "Kuala_Lumpur_Sentral"
        klia = "Kuala_Lumpur_International_Airport"
        pia = "Penang_International_Airport"
        kbw = "KTM_Butter_Worth"
        locations = [uM, uM_Bus, uM_Drive, tbs, ps, psahf, pp_Bus, pp_Drive, qb, klC, klia, pia, kbw]
        # 0     1      2        3   4     5       6        7     8    9    10   11,   12
        locationDicts = {
            0: uM,
            1: uM_Bus,
            2: uM_Drive,
            3: tbs,
            4: ps,
            5: psahf,
            6: pp_Bus,
            7: pp_Drive,
            8: qb,
            9: klC,
            10: klia,
            11: pia,
            12: kbw
        }
        allPath = []
        for i in range(len(allPathinNum)):
            temp = []
            for location in allPathinNum[i][1:]:
                temp.append(locationDicts[location])
            allPath.append(temp)
        return allPath
    # Create a graph given in the above diagram


######################End of Finding All Paths codes######################################

######################Start of Dijkstra Python codes######################################

# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
    return Edge(start, end, cost)


class GraphDij:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices: # --> O(n)
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]: # --> O(n)
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]: # in first loop, inf become the cost
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex
        path, current_vertex = deque(), dest #deque made it double-ended dequeable.
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path


######################END of Dijkstra Python codes######################################

######################Sentiment dict######################################
sentimentDict = {
    'flight': pow(0.95, 1),
    'drive': pow(0.95, 1),
    'train': pow(0.95, 1),
    'bus': pow(0.95, 1),  # positive articles reduces the weightage
}


# print(sentimentDict['flight'])
######################Sentiment dict######################################

class allFunction:

    def __init__(self, gmaps, api_key):
        self.api_key = api_key
        self.gmaps = gmaps

    # def plotMap(self, number=None):
    #     apikey = 'AIzaSyC4my9ZMi0RiUXYdWqsexT4JSwSbULFnLE'
    #     map = gmplot.GoogleMapPlotter(initLat, initLng, 8, apikey=apikey)
    #     listEvaLats, listEvaLons = getAllLatsNLons()
    #     if number == 1:
    #         map.plot(listEvaLats[0], listEvaLons[0], 'blue', edge_width=5)  # UM -> Grab -> TBS
    #         map.plot(listEvaLats[3], listEvaLons[3], 'red', edge_width=5)  # TBS -> Bus -> Penang Sentral
    #         map.plot(listEvaLats[4], listEvaLons[4], 'black', edge_width=5)  # Penang Sentral -> walk -> Ferry
    #         map.plot(listEvaLats[12], listEvaLons[12], 'yellow', edge_width=5)  # Ferry -> Ship -> Pulau Pinang
    #         map.plot(listEvaLats[5], listEvaLons[5], 'blue', edge_width=5)  # Pulau Pinang -> Grab -> Queen's Bay
    #     elif number == 2:
    #         map.plot(listEvaLats[2], listEvaLons[2], 'red', edge_width=5)  # UM -> Bus -> KL Central
    #         map.plot(listEvaLats[7], listEvaLons[7], 'purple', edge_width=5)  # KL Central -> LRT -> KTM Butterworth
    #         map.plot(listEvaLats[10], listEvaLons[10], 'blue', edge_width=5)  # KTM Butterworth -> Grab -> Queen's Bay
    #     elif number == 3:
    #         map.plot(listEvaLats[2], listEvaLons[2], 'red', edge_width=5)  # UM -> Bus -> KL Central
    #         map.plot(listEvaLats[8], listEvaLons[8], 'purple', edge_width=5)  # KL Central -> Train -> KLIA
    #         map.plot(listEvaLats[13], listEvaLons[13], 'green', edge_width=5)  # KLIA -> Flight -> PIA
    #         map.plot(listEvaLats[9], listEvaLons[9], 'blue', edge_width=5)  # PIA -> Grab -> Queen's Bay
    #     elif number == 4:
    #         map.plot(listEvaLats[2], listEvaLons[2], 'red', edge_width=5)  # UM -> Bus -> KL Central
    #         map.plot(listEvaLats[7], listEvaLons[7], 'purple', edge_width=5)  # KL Central -> LRT -> KTM Butterworth
    #         map.plot(listEvaLats[11], listEvaLons[11], 'black', edge_width=5)  # KTM Butterworth -> Walk -> Ferry
    #         map.plot(listEvaLats[12], listEvaLons[12], 'yellow', edge_width=5)  # Ferry -> Ship -> Pulau Pinang
    #         map.plot(listEvaLats[5], listEvaLons[5], 'blue', edge_width=5)  # Pulau Pinang -> Grab -> Queen's Bay
    #     elif number == 5:
    #         map.plot(listEvaLats[1], listEvaLons[1], 'blue', edge_width=5)  # UM -> Grab -> KL Central
    #         map.plot(listEvaLats[7], listEvaLons[7], 'purple', edge_width=5)  # KL Central -> LRT -> KTM Butterworth
    #         map.plot(listEvaLats[11], listEvaLons[11], 'black', edge_width=5)  # KTM Butterworth -> Walk -> Ferry
    #         map.plot(listEvaLats[12], listEvaLons[12], 'yellow', edge_width=5)  # Ferry -> Ship -> Pulau Pinang
    #         map.plot(listEvaLats[6], listEvaLons[6], 'red', edge_width=5)  # Pulau Pinang -> Bus -> Queen's Bay
    #
    #     route1Dist = umtbsDriveDist + tbspsBusDist + pspsahfWalkDist + psahfppFerryDist + ppqbDriveDist
    #     route2Dist = umklCBusDist + klCkbwTrainDist + kbwqbDriveDist
    #     route3Dist = umklCBusDist + klCkliaTrainDist + kliapiaFlightDist + piaqbDriveDist
    #     route4Dist = umklCBusDist + klCkbwTrainDist + kbwpsahfWalkDist + psahfppFerryDist + ppqbDriveDist
    #     route5Dist = umklCDriveDist + klCkbwTrainDist + kbwpsahfWalkDist + psahfppFerryDist + ppqbBusDist
    #     map.draw(
    #         "D:\\YiChongFiles\\WID180017\\Sem4\\WIA2005_Algorithm_Design_And_Analysis\\Assignments\\flaskMapProject\\src\\templates\\layout.html")
    #     return route1Dist, route2Dist, route3Dist, route4Dist, route5Dist
    def getAllPath(self):  # in all function, used method in Graph function
        g = GraphAllPath(13)
        # -2
        g.addEdge(0, 1)
        # -1
        g.addEdge(0, 2)
        # 0
        g.addEdge(2, 3)
        # 1
        g.addEdge(2, 9)
        # 2
        g.addEdge(1, 9)
        # 3
        g.addEdge(3, 4)
        # 4
        g.addEdge(4, 5)
        # 5
        g.addEdge(7, 8)
        # 6
        g.addEdge(6, 8)
        # 7
        g.addEdge(9, 12)
        # 8
        g.addEdge(9, 10)
        # 9
        g.addEdge(11, 8)
        # 10
        g.addEdge(12, 8)
        # 11
        g.addEdge(12, 5)
        # 12
        g.addEdge(5, 6)
        # 13
        g.addEdge(5, 7)
        # 14
        g.addEdge(10, 11)
        s = 0
        d = 8
        allPathinNum = g.printAllPaths(s, d)
        allPath = g.getAllPath(allPathinNum)
        return allPath

    def getShortest(self):
        graphShortest = GraphDij([
            (uM, uM + "_Bus", 0), (uM, uM + "_Drive", 0),
            (uM + "_Bus", klC, umklCBusDist), (uM + "_Drive", tbs, umtbsDriveDist),
            (uM + "_Drive", klC, umklCDriveDist),
            (tbs, ps, tbspsBusDist), (ps, psahf, pspsahfWalkDist),
            (psahf, pp + "_Drive", psahfppFerryDist), (psahf, pp + "_Bus", psahfppFerryDist),
            (pp + "_Drive", qb, ppqbDriveDist), (pp + "_Bus", qb, ppqbBusDist), (klC, kbw, klCkbwTrainDist),
            (klC, klia, klCkliaTrainDist),
            (klia, pia, kliapiaFlightDist), (pia, qb, piaqbDriveDist), (kbw, qb, kbwqbDriveDist),
            (kbw, psahf, kbwpsahfWalkDist)])
        pathShortest = graphShortest.dijkstra(uM, qb)
        pathShortest.popleft()
        return pathShortest

    def getAlgoReco(self):
        graphAlgoReco = GraphDij([
            (uM, uM + "_Bus", 0), (uM, uM + "_Drive", 0),
            (uM + "_Bus", klC, umklCBusDist * sentimentDict['bus']),
            (uM + "_Drive", tbs, umtbsDriveDist * sentimentDict['drive']),
            (uM + "_Drive", klC, umklCDriveDist * sentimentDict['drive']),
            (tbs, ps, tbspsBusDist * sentimentDict['bus']), (ps, psahf, pspsahfWalkDist),
            (psahf, pp + "_Drive", psahfppFerryDist * sentimentDict['drive']),
            (psahf, pp + "_Bus", psahfppFerryDist * sentimentDict['bus']),
            (pp + "_Drive", qb, ppqbDriveDist * sentimentDict['drive']),
            (pp + "_Bus", qb, ppqbBusDist * sentimentDict['bus']), (klC, kbw, klCkbwTrainDist * sentimentDict['train']),
            (klC, klia, klCkliaTrainDist * sentimentDict['train']),
            (klia, pia, kliapiaFlightDist * sentimentDict['flight']),
            (pia, qb, piaqbDriveDist * sentimentDict['drive']), (kbw, qb, kbwqbDriveDist * sentimentDict['drive']),
            (kbw, psahf, kbwpsahfWalkDist)])
        pathAlgoReco = graphAlgoReco.dijkstra(uM, qb)
        pathAlgoReco.popleft()
        return pathAlgoReco

    def plotPath(self, path=None):
        distance = 0;
        apikey = 'AIzaSyC4my9ZMi0RiUXYdWqsexT4JSwSbULFnLE'
        map = gmplot.GoogleMapPlotter(initLat, initLng, 8, apikey=apikey)
        listEvaLats, listEvaLons = getAllLatsNLons()
        if path != None:
            for i in range(len(path)):
                if path[i] == uM + "_Drive" and path[i + 1] == tbs:
                    map.plot(listEvaLats[0], listEvaLons[0], 'blue', edge_width=5)  # UM -> Grab -> TBS
                    distance += umtbsDriveDist
                elif path[i] == uM + "_Drive" and path[i + 1] == klC:
                    map.plot(listEvaLats[1], listEvaLons[1], 'blue', edge_width=5)  # UM -> Grab -> KL Central
                    distance += umklCDriveDist
                elif path[i] == uM + "_Bus" and path[i + 1] == klC:
                    map.plot(listEvaLats[2], listEvaLons[2], 'red', edge_width=5)  # UM -> Bus -> KL Central
                    distance += umklCBusDist
                elif path[i] == tbs and path[i + 1] == ps:
                    map.plot(listEvaLats[3], listEvaLons[3], 'red', edge_width=5)  # TBS -> Bus -> Penang Sentral
                    distance += tbspsBusDist
                elif path[i] == ps and path[i + 1] == psahf:
                    map.plot(listEvaLats[4], listEvaLons[4], 'black',
                             edge_width=5)  # Penang Sentral -> walk -> Ferry
                    distance += pspsahfWalkDist
                elif path[i] == pp + "_Drive" and path[i + 1] == qb:
                    map.plot(listEvaLats[5], listEvaLons[5], 'blue',
                             edge_width=5)  # Pulau Pinang -> Grab -> Queen's Bay
                    distance += ppqbDriveDist
                elif path[i] == pp + "_Bus" and path[i + 1] == qb:
                    map.plot(listEvaLats[6], listEvaLons[6], 'red',
                             edge_width=5)  # Pulau Pinang -> Bus -> Queen's Bay
                    distance += ppqbBusDist
                elif path[i] == klC and path[i + 1] == kbw:
                    map.plot(listEvaLats[7], listEvaLons[7], 'purple',
                             edge_width=5)  # KL Central -> LRT -> KTM Butterworth
                    distance += klCkbwTrainDist
                elif path[i] == klC and path[i + 1] == klia:
                    map.plot(listEvaLats[8], listEvaLons[8], 'purple', edge_width=5)  # KL Central -> Train -> KLIA
                    distance += klCkliaTrainDist
                elif path[i] == pia and path[i + 1] == qb:
                    map.plot(listEvaLats[9], listEvaLons[9], 'blue', edge_width=5)  # PIA -> Grab -> Queen's Bay
                    distance += piaqbDriveDist
                elif path[i] == kbw and path[i + 1] == qb:
                    map.plot(listEvaLats[10], listEvaLons[10], 'blue',
                             edge_width=5)  # KTM Butterworth -> Grab -> Queen's Bay
                    distance += kbwqbDriveDist
                elif path[i] == kbw and path[i + 1] == psahf:
                    map.plot(listEvaLats[11], listEvaLons[11], 'black',
                             edge_width=5)  # KTM Butterworth -> Walk -> Ferry
                    distance += kbwpsahfWalkDist
                elif path[i] == psahf and (path[i + 1] == pp + "_Drive" or path[i + 1] == pp + "_Bus"):
                    map.plot(listEvaLats[12], listEvaLons[12], 'yellow',
                             edge_width=5)  # Ferry -> Ship -> Pulau Pinang
                    distance += psahfppFerryDist
                elif path[i] == klia and path[i + 1] == pia:
                    map.plot(listEvaLats[13], listEvaLons[13], 'green', edge_width=5)  # KLIA -> Flight -> PIA
                    distance += kliapiaFlightDist
        map.draw(
            os.getcwd() + "\\templates\layout.html")
        return distance
    ######################End of Dijkstra Python codes######################################
