import './App.css';
import 'leaflet/dist/leaflet.css';

import L from 'leaflet';
import glify from 'leaflet.glify'
// import 'leaflet-glify-layer';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

import { MapContainer, TileLayer, Marker, Popup, useMap, GeoJSON } from 'react-leaflet'

import WaPop from './assets/wa_pop';

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

function GLGeoJson() {
  const map = useMap();
  // const myLayer = L.glify.layer({
  //   geojson: WaPop,
  // });
  // myLayer.addTo(map);
  let geo = {
      "type": "FeatureCollection",
      "features": WaPop["features"]
    }
  L.glify.shapes({
    map,
    data: geo,
  });
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
