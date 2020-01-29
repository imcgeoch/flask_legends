import React from 'react';

const axios = require('axios');

class Occasion extends React.Component {
	constructor(props) {
		super(props);
		this.state = {items : {}};
  }
	
	getFromAPI() {
		const {worldid, entityid, id} = this.props.match.params
		axios.get(`/api/${worldid}/occasion/${entityid}/${id}`)
		  .then(response => {
				//			console.log(response); 
				this.setState( {items : response.data} );
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
		const items = this.state.items;
		return( <div> <h1>Occasion Page</h1>
				<p> World: {this.props.match.params.worldid} </p>
				<p> Entity: {this.props.match.params.entityid} </p>
				<p> Occasion: {this.props.match.params.id} </p>
			</div>
		)

	}

}
export default Occasion;
