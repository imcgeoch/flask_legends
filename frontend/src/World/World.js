import React from 'react';
import {Map, ImageOverlay} from 'react-leaflet';
import {CRS} from 'leaflet';

const axios = require('axios');

class World extends React.Component {
	
	constructor(props) {
		super(props);
		this.state = {items : {}};
	}

  getFromAPI() {
		let worldid = this.props.match.params.worldid;
		let id = this.props.match.params.id;
		axios.get(`/api/${worldid}`)
		  .then(response => {
				console.log(response); 
				this.setState( {items : response.data} );
			});
	}

	componentDidMount() {
	  this.getFromAPI();
	}

	componentDidUpdate(prevProps) {
		console.log("update");
		console.log(this.props.match.params);
		console.log(prevProps.match.params);
		if (this.props.match.params.id !== prevProps.match.params.id ){
			this.getFromAPI();
		}
	}

	render() {
		const {name } = this.state.items;
		const {id, worldid} = this.props.match.params;
		return( 
			<div id="world">
				<h1> {name} </h1>
				<Map center={[0,0]} zoom={2} crs={CRS.Simple}> 
					<ImageOverlay url="/explorer/static/img/1/world_world_map.png"
				                bounds={[[0,0],[396,360]]}/>
        </Map>
			</div>
		);
	}
}
export default World;
