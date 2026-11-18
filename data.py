import math
PLACES=[["Shivajinagar",18.5308,73.8475],["Pune Station",18.5286,73.8744],["Swargate",18.5018,73.8636],["Kothrud",18.5074,73.8077],["Aundh",18.559,73.8077],["Baner",18.559,73.7868],["Hinjewadi",18.5912,73.7389],["Wakad",18.5987,73.7607],["Pimpri",18.6279,73.8007],["Chinchwad",18.6448,73.7978],["Viman Nagar",18.5679,73.9143],["Kharadi",18.5515,73.94],["Hadapsar",18.5089,73.9259],["Katraj",18.4575,73.8676],["Koregaon Park",18.5362,73.8938]]
EDGES=[[0,1],[0,3],[0,4],[0,2],[1,2],[1,14],[1,12],[14,10],[14,12],[14,11],[10,11],[11,12],[2,13],[2,3],[2,12],[3,5],[5,4],[5,7],[7,6],[7,8],[8,9],[8,4],[5,6],[13,12],[0,8]]
# Sample data: facilities are attached to the nearest area, not exact addresses.
FACILITIES=[{"t":"h","n":"Ruby Hall Clinic","at":1},{"t":"h","n":"Sahyadri Hospital","at":3},{"t":"h","n":"Deenanath Mangeshkar Hospital","at":0},{"t":"h","n":"Aditya Birla Hospital","at":9},{"t":"h","n":"Noble Hospital","at":12},{"t":"s","n":"Katraj Relief Shelter","at":13},{"t":"s","n":"Baner Community Hall","at":5},{"t":"s","n":"Viman Nagar School Camp","at":10},{"t":"p","n":"Swargate Supply Depot","at":2},{"t":"p","n":"Wakad Relief Depot","at":7},{"t":"p","n":"Kharadi Supply Point","at":11}]
FLOOD_NODE=3
def key(a,b): return f"{min(a,b)}-{max(a,b)}"
def haversine(a,b):
    r=math.pi/180
    x=math.sin((b[1]-a[1])*r/2)**2+math.cos(a[1]*r)*math.cos(b[1]*r)*math.sin((b[2]-a[2])*r/2)**2
    return 12742*math.asin(math.sqrt(x))
WEIGHTS={key(a,b):haversine(PLACES[a],PLACES[b])*1.3 for a,b in EDGES}
