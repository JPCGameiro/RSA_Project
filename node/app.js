//const sql = require('sqlite3');
var L = require('leaflet');

// Initialize the map
var map = L.map('map',{ center: [40.633258, -8.659097], zoom: 5000 });

// Initialize the base layer
var osm_mapnik = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	attribution: '&copy; OSM Mapnik <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var rsuIcon = L.icon({
    iconUrl: 'style/antenna.png',
    iconSize: [39, 39],
    iconAnchor: [18, 39],
    popupAnchor: [10, -35]
});

var obuIcon = L.icon({
    iconUrl: 'style/car.png',
    iconSize: [39, 39],
    iconAnchor: [18, 39],
    popupAnchor: [10, -35]
});

/*
const db = new sql.Database('./park.db', sql.OPEN_READONLY, (err)=>{
	if(err) return console.error(err.message);
});


db.all('select name, lat, long from RSU', [name, lat, long], (err, rows) => {
    if(err) return console.error(err.message);
    rows,array.forEach(element => {
        console.log(element.name);
    });
});*/

L.marker([40.633258, -8.659097], {icon: rsuIcon}).addTo(map)
    	.bindTooltip("center", {permanent: true})
        .openTooltip();

var x = 1
setInterval(moveObus, 100);
function moveObus() {
	x+=1;
	console.log(x);
}