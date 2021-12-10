import './App.css';
import 'leaflet/dist/leaflet.css';

import L from 'leaflet';
import glify from 'leaflet.glify'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

import { MapContainer, TileLayer, Marker, Popup, useMap, GeoJSON } from 'react-leaflet'

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconUrl: markerIcon,
    iconRetinaUrl: markerIcon2x,
    shadowUrl: markerShadow,
})

function FocusScroll() {
  const map = useMap();
  map.scrollWheelZoom.enable();
  return null;
}

let called = false;

function GLGeoJson() {
  const map = useMap();
  if (called) return null
  called = true;
  console.log("call")
  
  fetch("data/pop.json", {
  headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
  }}).then((r) => {
    return r.json();
  }).then((geojson) => {
    L.glify.shapes({
      map,
      data: geojson,
      color: (_, feature) => {
        let rgb = feature.properties.rgb;
        rgb.a = 0.4;
        return rgb;
      }
    }); 
    })
  return null;
}

// function renderCountries(geoJson) {
//   return geoJson.features.map(feature => {
//     let featureCollection = {
//       "type": "FeatureCollection",
//       "features": [feature]
//     };
//     let style = { fillColor: feature.properties.color, fillOpacity: 0.75, weight: 0 };

//     return (
//       <GeoJSON data={featureCollection} style={style} />
//     );
//   });
// }

function App() {
  return (
    <div className="App">
      <MapContainer center={[47.6062, -122.3321]} zoom={8} scrollWheelZoom={false}>
        <FocusScroll/>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {/* <GeoJSON data={WaPop}/> */}
        {/* { renderCountries(WaPop) } */}
        <GLGeoJson/>
      </MapContainer>
    </div>
  );
}

export default App;
