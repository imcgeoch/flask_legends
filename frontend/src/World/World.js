import React from 'react';
import DFMap from './DFMap';
import axios from 'axios';
import {Link} from 'react-router-dom';

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
		const {name, altname, sites, size_info} = this.state.items;
		const {id, worldid} = this.props.match.params;
		return( 
			<div id="world">
				<h1> {name} </h1>
				<h2> {altname} </h2>
				<DFMap world_id={worldid} sites={sites} size_info={size_info}/>
				<ul>
					<li>
						<Link to={`/${worldid}/histfigs`}>Historical Figures</Link>
					</li>
					<li>
				<Link to={`/${worldid}/artifacts`}>Artifacts</Link>	
			</li>
			</ul>
			</div>
		);
	}
}
export default World;
