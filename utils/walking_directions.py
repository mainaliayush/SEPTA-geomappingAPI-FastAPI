import openrouteservice
import httpx


# # Open Route Service uses requests internally, hence this function is synchronous
# # Might run into unexpected issues if Async is added. FastAPI does not know how to properly await non-async function
 
# def get_walking_directions(start_coordinates, end_coordinates, ors_api_key):
#     client = openrouteservice.Client(key=ors_api_key)

#     route = client.directions(
#         coordinates=[start_coordinates, end_coordinates],
#         profile='foot-walking',
#         format='geojson'
#     )
#     return route 



## CODE OPTIMIZATION 
## For million of API requests per day replace ORS client library -> httpx.AsyncClient . 
## The function needs to be be asynchronous to handle large number of requests in a non-blocking manner.

async def get_walking_directions(start_coordinates, end_coordinates, ors_api_key):
    url = "https://api.openrouteservice.org/v2/directions/foot-walking/geojson"
    headers = {
        "Authorization": ors_api_key,
        "Content-Type": "application/json"
    }
    body = {
        "coordinates": [start_coordinates, end_coordinates]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()