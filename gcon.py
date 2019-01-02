import requests 
import time

API_KEY = '###'

place_id_list = []

def search_maps(search_term , next_page_token):
    search_term = search_term.replace(' ' , '+')
    print("Running data extraction for "+search_term)

    SEARCH = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+search_term+"&key="+API_KEY+"&pagetoken="+next_page_token
    
    data = requests.get(SEARCH).json()

    for place in data['results']:
            if place['place_id'] not in place_id_list: 
                place_id_list.append(place['place_id'])

    try:
        next_page_token = data['next_page_token']
    except KeyError:
        return 
    time.sleep(1)
    search_maps(search_term , next_page_token)


    # while next_page_token is not False:
    #     print('in')
    #     SEARCH = "https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken="+next_page_token+"&key="+API_KEY+""
    #     data = requests.get(SEARCH).json()
    #     for place in data['results']:
    #         if place['place_id'] not in place_id_list: 
    #             place_id_list.append(place['place_id'])
    #     time.sleep(2)

    #     try:
    #         next_page_token = data['next_page_token']
    #         if next_page_token is None:
    #             next_page_token = False
    #     except:
    #         next_page_token = False

        

#     # if result_list["next_page_token"] :
#     #     next_page = result_list["next_page_token"]
#     #     SEARCH = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken="+next_page+"&key="+API_KEY+""
#     #     result_list(SEARCH)
        

# def result_list(maps_url):
#     result_list = requests.get(maps_url).json()

#     place_id_list = []
#     for place_id in result_list["results"]:
#         place_id_list.append(place_id["place_id"])
    
#     print(place_id_list)


def get_contact(place_id):
    DETAIL = "https://maps.googleapis.com/maps/api/place/details/json?placeid="+place_id+"&fields=name,formatted_address,international_phone_number,website&key="+API_KEY+""
    place_details = requests.get(DETAIL).json()
    name = place_details["result"]["name"]
    address = place_details["result"]["formatted_address"]
    phone_number = place_details["result"]["international_phone_number"]
    website = place_details["result"]["website"]
    return name , address , phone_number , website  

if __name__ == "__main__" :
    search_maps("Womens Boutique Kochi" , "")
    # search_maps("Ladies Tailoring Kochi")
    # search_maps("Saree Shop Kochi")
    # search_maps("Kuriti Shop Kochi")
    # search_maps("Ladies Dress Materials Kochi")

    print(len(place_id_list))
