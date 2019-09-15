import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import EntityLink from "./Entity_Link";
const axios = require('axios');


function Entity_Details({name, race, type}) {
	return( <div id="entity details"> 
		{name} was a {race} {type}. 
		</div>
	)
}

function EntityLinkList({entity_links = [], worldid='', ...props}) {
	console.log(entity_links);
	return(
		<ul>
			{
				entity_links.map(({link_type, entity_type,  ...props}) => 
					(<li key={props.entity_id}> <EntityLink {... props} worldid={worldid} />, its {link_type}, a {entity_type} </li>))
			}
		</ul>
	);
}

class Entity extends React.Component {
	constructor(props) {
		super(props);
		this.state = {items : {}};
  }

	getFromAPI() {
		const {worldid, id} = this.props.match.params
		//let worldid = this.props.match.params.worldid;
		//let id = this.props.id;
		axios.get(`/api/${worldid}/entity/${id}`)
		  .then(response => {
				//			console.log(response); 
				this.setState( {items : response.data} );
			});
		axios.get(`/api/${worldid}/events?entity=${id}`)
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
		
		return( <div> <h1>{items.name}</h1>
			<Entity_Details {... items} />
			<EntityLinkList entity_links={items.entity_links} worldid={worldid} />
			</div>
		)

	}



}


export default Entity;
