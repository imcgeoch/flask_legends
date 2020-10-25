import React from 'react';
import {Link} from 'react-router-dom';
import queryString from 'query-string';

import HistfigLink from "../Histfig/Histfig_Link"

const axios = require('axios');


class HistfigListPage extends React.Component {
	constructor(props) {
		super(props);
		this.state = {items : {}};
  }
	
	getFromAPI() {
		const {worldid} = this.props.match.params
		const queryParams = queryString.parse(this.props.location.search)
		const after = queryParams.after ? `?after=${queryParams.after}` : '';
		axios.get(`/api/${worldid}/histfigs${after}`)
		  .then(response => {
				//			console.log(response); 
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
		const {hfs=[]} = this.state.items;
		const {worldid} = this.props.match.params
		const queryParams = queryString.parse(this.props.location.search)
		const after = queryParams.after ? `${queryParams.after}` : 0;

		//console.log(after);
		return( <div>
			<ul>
				{hfs.map((props) => (<li> The {props.race} <HistfigLink {...props} worldid={worldid}/></li>))} 
			</ul>
			{ after != 0 ?
					<Link to={`/${worldid}/histfigs/?after=${after > 25 ? after-25 : 0}`}> PREV </Link>
		      : <div/>}
			{ hfs.length == 25 ?
					<Link to={`/${worldid}/histfigs/?after=${25 + Number(after)}`}> NEXT </Link>	
			    : <div/> }
			</div>
		)

	}

}

export default HistfigListPage;
