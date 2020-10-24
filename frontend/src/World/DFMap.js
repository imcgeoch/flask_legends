import React from 'react';
import {Map, ImageOverlay, Marker, Popup, Tooltip} from 'react-leaflet';
import {CRS, icon} from 'leaflet';

let greyDot = icon({
	iconUrl:'../greydot.png',
	iconSize: [10,10], // Set this to tile size
	iconAnchor: [5,5],
});

function SiteMarker({world_id, coords, id, name, type, coord_size}) {

	let coordsList = coords.split(",");
	let {coord_height, coord_width, height_pixels} = coord_size
	let pos = [coordsList[1] * -1 * coord_height - coord_height/2 + height_pixels, 
		         coordsList[0] * coord_width + coord_width/2];

  return(
	  <Marker position={pos} icon={greyDot} opacity={0}>
			<Popup><a href={`/${world_id}/site/${id}`}>{name}</a> ({type})  </Popup>
	  </Marker>
   )
}

class DFMap extends React.Component {

	constructor(props) {
		super(props);
		this.state = {showSites : 1};
	}

	toggle(name) {
		this.setState({[name] : 1^ this.state[name]})
	}
	
	render() {
		let {world_id, size_info, sites=[]} = this.props;
		if (size_info == undefined)
			return <div/>
	  let {height_pixels, width_pixels, height_coords, width_coords} = size_info;
	  let coord_height = height_pixels / height_coords;
	  let coord_width = width_pixels / width_coords;
		let coord_size = {coord_height, coord_width, height_pixels}


		return (
			<div>
				<Map center={[198,165]} crs={CRS.Simple} zoom={0}
			  style={{height:`${height_pixels}px`, width:`${width_pixels}px`}}>
			  <ImageOverlay 
			    url={`/explorer/static/img/${world_id}/world_world_map.png`} 
				  bounds={[[0,0],[396,330]]} />
				
				{this.state.showSites 
						? sites.map((s) => (<SiteMarker {...s} 
						                                coord_size={coord_size} 
					                                  world_id={world_id}
							                   />))
						: <div/>}

			</Map>
			<button onClick={()=>this.toggle("showSites")}>
				Toggle Sites
			</button>
		</div>
		)
	}
}

export default DFMap;
