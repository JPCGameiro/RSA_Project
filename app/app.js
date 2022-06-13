// Initialize leaflet.js
var L = require('leaflet');

// Initialize the map
var map = L.map('map', {
  scrollWheelZoom: false
});

// Set the position and zoom level of the map
map.setView([40.631491, -8.656481], 200);

// Initialize the base layer
var osm_mapnik = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; OSM Mapnik <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


//RSU icon
var rsuIcon = L.icon({
    iconUrl: 'static/antenna.png',
    iconSize: [39, 39],
    iconAnchor: [18, 39],
    popupAnchor: [10, -35]
});
//OBU icon
var obuIcon = L.icon({
    iconUrl: 'static/car.png',
    iconSize: [39, 39],
    iconAnchor: [18, 39],
    popupAnchor: [10, -35]
});

var rsu = L.marker([40.631491, -8.656481], {icon: rsuIcon}).bindPopup('RSU1');
var parkedobu = L.marker([40.631662, -8.656547], {icon: obuIcon}).bindPopup('OBU1');


//Add icons to the map
rsu.addTo(map);
parkedobu.addTo(map);
