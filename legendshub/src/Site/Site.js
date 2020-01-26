import React from 'react';
const axios = require('axios');
//import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

class Site extends React.Component {
	constructor(props) {
		super(props);
		this.state = {items : {}};
  }
	
	getFromAPI() {
		const {worldid, id} = this.props.match.params
		axios.get(`/api/${worldid}/site/${id}`)
		  .then(response => {
				//			console.log(response); 
				this.setState( {items : response.data} );
			});
		axios.get(`/api/${worldid}/events?site=${id}`)
		  .then(response => {
				//console.log(response); 
				this.setState( {events : response.data} );
			});
	}

	componentDidMount() {
	  this.getFromAPI();
	}

	componentDidUpdate(prevProps) {
		if (this.props.match.params.id !== prevProps.match.params.id ){
			this.getFromAPI();
		}
	}

	render() {
		return( <div> <h1>Site Page</h1>
			<p> Site: {this.props.match.params.worldid} </p>
			<p> Site: {this.props.match.params.id} </p>
		</div>
		)

	}

}

export default Site;
