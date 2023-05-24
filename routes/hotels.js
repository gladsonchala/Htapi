const express = require('express');
const router = express.Router();
const { v4: uuidv4 } = require('uuid');
const admin = require('firebase-admin');

const db = admin.database();

const getAllHotels = (req, res) => {
  db.ref('hotels').once('value', (snapshot) => {
    const hotels = snapshot.val();
    res.json(hotels);
  });
};

const getHotelById = (req, res) => {
  const { hotel_id } = req.params;
  db.ref(`hotels/${hotel_id}`).once('value', (snapshot) => {
    const hotel = snapshot.val();
    if (hotel) {
      res.json(hotel);
    } else {
      res.status(404).json({ error: 'Hotel not found' });
    }
  });
};

const createHotel = (req, res) => {
  if (req.isAuthorized) {
    const { name, photos_url, ground, city, approximate_location, google_map_location_url, latitude, longitude, price_range, additional_services, rooms, other_description } = req.body;
    const hotelId = uuidv4();
    const newHotel = {
      name,
      photos_url,
      ground,
      city,
      approximate_location,
      google_map_location_url,
      latitude,
      longitude,
      price_range,
      additional_services,
      rooms,
      other_description,
    };
    db.ref(`hotels/${hotelId}`).set(newHotel, (error) => {
      if (error) {
        res.status(500).json({ error: 'Failed to create hotel' });
      } else {
        res.status(201).json({ hotel_id: hotelId });
      }
    });
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
};

const updateHotel = (req, res) => {
  if (req.isAuthorized) {
    const { hotel_id } = req.params;
    const { name, photos_url, ground, city, approximate_location, google_map_location_url, latitude, longitude, price_range, additional_services, rooms, other_description } = req.body;
    db.ref(`hotels/${hotel_id}`).once('value', (snapshot) => {
      const hotel = snapshot.val();
      if (hotel) {
        hotel.name = name || hotel.name;
        hotel.photos_url = photos_url || hotel.photos_url;
        hotel.ground = ground || hotel.ground;
        hotel.city = city || hotel.city;
        hotel.approximate_location = approximate_location || hotel.approximate_location;
        hotel.google_map_location_url = google_map_location_url || hotel.google_map_location_url;
        hotel.latitude = latitude || hotel.latitude;
        hotel.longitude = longitude || hotel.longitude;
        hotel.price_range = price_range || hotel.price_range;
        hotel.additional_services = additional_services || hotel.additional_services;
        hotel.rooms = rooms || hotel.rooms;
        hotel.other_description = other_description || hotel.other_description;

        db.ref(`hotels/${hotel_id}`).set(hotel, (error) => {
          if (error) {
            res.status(500).json({ error: 'Failed to update hotel' });
          } else {
            res.json(hotel);
          }
        });
      } else {
        res.status(404).json({ error: 'Hotel not found' });
      }
    });
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
};

const deleteHotel = (req, res) => {
  if (req.isAuthorized) {
    const { hotel_id } = req.params;
    db.ref(`hotels/${hotel_id}`).once('value', (snapshot) => {
      const hotel = snapshot.val();
      if (hotel) {
        db.ref(`hotels/${hotel_id}`).remove((error) => {
          if (error) {
            res.status(500).json({ error: 'Failed to delete hotel' });
          } else {
            res.sendStatus(204);
          }
        });
      } else {
        res.status(404).json({ error: 'Hotel not found' });
      }
    });
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
};

router.get('/', getAllHotels);
router.get('/:hotel_id', getHotelById);
router.post('/', createHotel);
router.put('/:hotel_id', updateHotel);
router.delete('/:hotel_id', deleteHotel);

module.exports = router;
