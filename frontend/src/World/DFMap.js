import React from 'react';
import {Map, ImageOverlay, Marker, Popup, Tooltip} from 'react-leaflet';
import {CRS, icon} from 'leaflet';

let greyDot = icon({
	iconUrl:'./greydot.png',
	iconSize: [10,10], // Set this to tile size
	iconAnchor: [5,5],
});

function SiteMarker({world_id, coords, id, name, type, show=0, }) {
	let coordsList = coords.split(",");
	console.log(id)
	console.log(coordsList)
	let pos = [coordsList[1]*-12+390, coordsList[0]*10+5];
	

  return(
	  <Marker position={pos} icon={greyDot} opacity={0.5 * show}
		        onClick={()=>window.location.href= `/${world_id}/site/${id}`}>
	    <Tooltip>{name} ({type})</Tooltip>
	  </Marker>
   )
}

class DFMap extends React.Component {

	constructor(props) {
		super(props);
		this.state = {showSites : 0};
	}

	toggle(name) {
		this.setState({[name] : 1^ this.state[name]})
	}
	
	render() {
		let {height, width, world_id, sites=[]} = this.props;

		return (
			<div>
			<Map center={[height/2,width/2]} crs={CRS.Simple} zoom={0}
			  style={{height:`${height}px`, width:`${width}px`}}>
			  <ImageOverlay 
			    url={`/explorer/static/img/${world_id}/world_world_map.png`} 
				bounds={[[0,0],[height,width]]} />
				
				{this.state.showSites 
						? sites.map((s) => (<SiteMarker {...s} show={this.state.showSites}/>))
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
