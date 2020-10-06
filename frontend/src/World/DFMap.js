import React from 'react';
import {Map, ImageOverlay} from 'react-leaflet';
import {CRS} from 'leaflet';

class DFMap extends React.Component {

	render() {
		let {height, width, world_id} = this.props;


    return (
			<Map center={[height/2,width/2]} crs={CRS.Simple} zoom={0}
			  style={{height:`${height}px`, width:`${width}px`}}>
			  <ImageOverlay 
			    url={`/explorer/static/img/${world_id}/world_world_map.png`} 
					bounds={[[0,0],[height,width]]} />
			</Map>
		)
	}
}

export default DFMap;
