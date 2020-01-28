import React from 'react';
import EntityLink from "../Entity/Entity_Link";

const axios = require('axios');
//import { BrowserRouter as Router, Route, Link } from 'react-router-dom';


function SiteEntities({civ, site_gvt}){
	return (<div> 
		{civ != null ? <span> It belongs to <EntityLink {... civ} />. </span> : null }
		{site_gvt != null ? <span> It is localy run by <EntityLink {... site_gvt} />. 
		                                                              </span> : null }
	</div>
	)
}

function SiteImage({img}){
	if (img != null) {
		return <div> <img src={img} height="300" width="300" /> </div>
	}
	else return null
}

function SiteDetails(items){
	const {name, type, civ, site_gvt} = items;
	return <div> {name} is a {type}. <SiteEntities {... items} /></div>
}

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
		const items = this.state.items;
		
		return( <div> <h1>{items.name}</h1>
			<SiteDetails {... items} />
			<SiteImage {... items} />
		</div>
		)

	}

}

export default Site;
