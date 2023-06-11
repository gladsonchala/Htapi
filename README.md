# Htapi
Hotel API 

Code of REST-API of The data model:
```
{
  "hotels": {
    "hotel_id": {
      "name": "",
      "photos_url": ["url1", "url2", "..."],
      "ground": "G+1",
      "city": "",
      "approximate_location": "",
      "google_map_location_url": "",
      "latitude": "",
      "longitude": "",
      "price_range": {
        "min": "",
        "max": ""
      },
      "additional_services": ["service1", "service2", "..."],
      "rooms": [
        {
          "room_id": "",
          "room_type": "",
          "room_area": "",
          "room_pricing": "",
          "room_photos": ["url1", "url2", "..."],
          "additional_services": ["service1", "service2", "..."],
          "other_description": ""
        }
      ],
      "other_description": ""
    }
  }
}
```
The hotels object includes fields like photos_url, ground, city, approximate_location, google_map_location_url, latitude, longitude, price_range, additional_services, and other_description.
The rooms object includes room_type, room_area, room_pricing, room_photos, additional_services & other_description fields.

The endpoints:

1. GET /hotels - Returns a list of all hotels
2. GET /hotels/{hotel_id} - Returns details for a specific hotel
3. POST /hotels - Creates a new hotel with the provided details
4. PUT /hotels/{hotel_id} - Updates the details for a specific hotel
5. DELETE /hotels/{hotel_id} - Deletes a specific hotel
6. GET /hotels/{hotel_id}/rooms - Returns a list of all rooms for a specific hotel
7. GET /hotels/{hotel_id}/rooms/{room_id} - Returns details for a specific room in a specific hotel
8. POST /hotels/{hotel_id}/rooms - Creates a new room for a specific hotel with the provided details
9. PUT /hotels/{hotel_id}/rooms/{room_id} - Updates the details for a specific room in a specific hotel
10. DELETE /hotels/{hotel_id}/rooms/{room_id} - Deletes a specific room in a specific hotel
11. GET /hotels/search?query={search_query} - Returns a list of hotels that match the search query.
