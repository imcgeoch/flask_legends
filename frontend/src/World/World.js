import React from 'react';
import DFMap from './DFMap';

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
		const {name, altname, sites} = this.state.items;
		const {id, worldid} = this.props.match.params;
		return( 
			<div id="world">
				<h1> {name} </h1>
				<h2> {altname} </h2>
				<DFMap height={396} width={330} world_id={1} sites={sites}/>
			</div>
		);
	}
}
export default World;
