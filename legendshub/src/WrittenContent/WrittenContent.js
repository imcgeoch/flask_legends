import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import HistfigLink from "../Histfig/Histfig_Link";

const axios = require('axios');




class WrittenContent extends React.Component {
	constructor(props) {
		super(props);
		this.state = {items : {}};
  }

	getFromAPI() {
		const {worldid, id} = this.props.match.params
		axios.get(`/api/${worldid}/written_content/${id}`)
		  .then(response => {
			  console.log(response); 
				this.setState( {items : response.data} );
			});
		axios.get(`/api/${worldid}/events?written_content=${id}`)
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
		const {id, worldid} = this.props.match.params;
		const items = this.state.items;
		const authorProps = { hf_name:items.author_name, 
			                    hfid:items.author_hfid, 
			                    worldid:items.worldid };
		
		return( <div> <h1>{items.title}</h1>
			{items.title} is a {items.form}. It was written by <HistfigLink {... authorProps} />.
			The writing is {items.styles}. 
			</div>
		)

	}

}

export default WrittenContent;
