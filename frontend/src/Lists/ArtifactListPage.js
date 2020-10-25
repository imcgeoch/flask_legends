import React from 'react';
import {Link} from 'react-router-dom';
import queryString from 'query-string';

import ArtifactLink from "../Artifact/Artifact_Link"

const axios = require('axios');


class ArtifactListPage extends React.Component {
	constructor(props) {
		super(props);
		this.state = {items : {}};
  }
	
	getFromAPI() {
		const {worldid} = this.props.match.params
		const queryParams = queryString.parse(this.props.location.search)
		const after = queryParams.after ? `?after=${queryParams.after}` : '';
		axios.get(`/api/${worldid}/artifacts${after}`)
		  .then(response => {
				this.setState( {items : response.data} );
			});
	}

	componentDidMount() {
	  this.getFromAPI();
	}

	componentDidUpdate(prevProps) {
		if (this.props.location.search !== prevProps.location.search ){
			this.getFromAPI();
		}
	}

	render() {
		const {artifacts=[]} = this.state.items;
		const {worldid} = this.props.match.params
		const queryParams = queryString.parse(this.props.location.search)
		const after = queryParams.after ? `${Number(queryParams.after)}` : 0;
		
		return( <div>
			<ul>
				{artifacts.map((props) => (
					<li> The {props.mat} {props.item_type} <ArtifactLink {...props} worldid={worldid}/> 
               {props.name != props.name_string ? ", " + props.name : ""}
					</li>))} 
			</ul>
			{ after != 0 ?
					<Link to={`/${worldid}/artifacts/?after=${after > 25 ? after-25 : 0}`}> PREV </Link>
		      : <div/>}
			{ artifacts.length == 25 ?
					<Link to={`/${worldid}/artifacts/?after=${25 + Number(after)}`}> NEXT </Link>	
			    : <div/> }
			</div>
		)
	}
}

export default ArtifactListPage;
