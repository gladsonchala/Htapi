const express = require('express');
const router = express.Router({ mergeParams: true });
const { v4: uuidv4 } = require('uuid');
const admin = require('firebase-admin');

const db = admin.database();

const getHotel = async (hotelId) => {
  const snapshot = await db.ref(`hotels/${hotelId}`).once('value');
  const hotel = snapshot.val();
  if (!hotel) {
    throw new Error('Hotel not found');
  }
  return hotel;
};

const getAllRooms = async (req, res) => {
  try {
    const hotelId = req.params.hotel_id;
    const hotel = await getHotel(hotelId);
    res.json(hotel.rooms);
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
};

const getRoomById = async (req, res) => {
  try {
    const hotelId = req.params.hotel_id;
    const roomId = req.params.room_id;
    const hotel = await getHotel(hotelId);
    const room = hotel.rooms.find((room) => room.room_id === roomId);
    if (room) {
      res.json(room);
    } else {
      res.status(404).json({ error: 'Room not found' });
    }
  } catch (error) {
    res.status(404).json({ error: error.message });
  }
};

const createRoom = (req, res) => {
  if (req.isAuthorized) {
    const hotelId = req.params.hotel_id;
    const { room_type, room_area, room_pricing, room_photos, additional_services, other_description } = req.body;
    const roomId = uuidv4();
    const newRoom = {
      room_id: roomId,
      room_type,
      room_area,
      room_pricing,
      room_photos,
      additional_services,
      other_description,
    };
    db.ref(`hotels/${hotelId}/rooms`).push(newRoom, (error) => {
      if (error) {
        res.status(500).json({ error: 'Failed to create room' });
      } else {
        res.status(201).json({ room_id: roomId });
      }
    });
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
};

const updateRoom = async (req, res) => {
  if (req.isAuthorized) {
    try {
      const hotelId = req.params.hotel_id;
      const roomId = req.params.room_id;
      const hotel = await getHotel(hotelId);
      const roomIndex = hotel.rooms.findIndex((room) => room.room_id === roomId);
      if (roomIndex !== -1) {
        const { room_type, room_area, room_pricing, room_photos, additional_services, other_description } = req.body;
        hotel.rooms[roomIndex].room_type = room_type || hotel.rooms[roomIndex].room_type;
        hotel.rooms[roomIndex].room_area = room_area || hotel.rooms[roomIndex].room_area;
        hotel.rooms[roomIndex].room_pricing = room_pricing || hotel.rooms[roomIndex].room_pricing;
        hotel.rooms[roomIndex].room_photos = room_photos || hotel.rooms[roomIndex].room_photos;
        hotel.rooms[roomIndex].additional_services = additional_services || hotel.rooms[roomIndex].additional_services;
        hotel.rooms[roomIndex].other_description = other_description || hotel.rooms[roomIndex].other_description;
        await db.ref(`hotels/${hotelId}/rooms`).set(hotel.rooms);
        res.json(hotel.rooms[roomIndex]);
      } else {
        res.status(404).json({ error: 'Room not found' });
      }
    } catch (error) {
      res.status(404).json({ error: error.message });
    }
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
};

const deleteRoom = async (req, res) => {
  if (req.isAuthorized) {
    try {
      const hotelId = req.params.hotel_id;
      const roomId = req.params.room_id;
      const hotel = await getHotel(hotelId);
      const roomIndex = hotel.rooms.findIndex((room) => room.room_id === roomId);
      if (roomIndex !== -1) {
        hotel.rooms.splice(roomIndex, 1);
        await db.ref(`hotels/${hotelId}/rooms`).set(hotel.rooms);
        res.sendStatus(204);
      } else {
        res.status(404).json({ error: 'Room not found' });
      }
    } catch (error) {
      res.status(404).json({ error: error.message });
    }
  } else {
    res.status(401).json({ error: 'Unauthorized' });
  }
};

router.get('/', getAllRooms);
router.get('/:room_id', getRoomById);
router.post('/', createRoom);
router.put('/:room_id', updateRoom);
router.delete('/:room_id', deleteRoom);

module.exports = router;
