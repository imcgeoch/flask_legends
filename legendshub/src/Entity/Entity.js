import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import EntityLink from "./Entity_Link";
import HistfigLink from "../Histfig/Histfig_Link";
import SiteLink from "../Site/SiteLink";
import RelatedList from "../RelatedList";
import OccasionLink from "../Occasion/OccasionLink";
import Event_List from "../Events/Event_List"
const axios = require('axios');


function Entity_Details({name, race, type}) {
	return( <div id="entity details"> 
		{name} was a {race} {type}. 
		</div>
	)
}

function EntityLinkListItem({link_type="", entity_type, worldid="", ... props}){
	return (<li key={props.entity_id}>
					 <EntityLink {... props} worldid={worldid} />, its {link_type.toLowerCase()}, a {entity_type} 
		     </li>);
}

function EntityLinkList({entity_links=[], worldid='', ... props}){
	const fn = (prps) => (<EntityLinkListItem {... prps} worldid={worldid}/> );
	return <RelatedList fn={fn} list={entity_links} divId="entity links" title="Entity Links" />
}

function EntityPositionListItem({name, vacant, ... props}){
	return <li key={name}> {name}: {vacant ? "Vacant" : <HistfigLink {... props} />} </li>
}

function EntityPositionList({entity_positions=[], worldid='', ...props}){
	const fn = (prps) => (<EntityPositionListItem {... prps} worldid={worldid} /> );
	return <RelatedList fn={fn} list={entity_positions} divId="entity positions" title="Positions" />
}

function EntitySiteListItem(props){
	  const {id, type} = props;
		return <li key={id}><SiteLink {... props} />: {type}  </li>
}

function EntitySiteList({sites=[], worldid='', ...props}){
	const fn = (prps) => (<EntitySiteListItem {... prps} worldid={worldid} />);
	return <RelatedList fn={fn} list={sites} divId="entity sites" title="Sites" />
}

function EntityOccasionListItem(props){
	const {id} = props;
	return <li key={id}><OccasionLink {... props} /> </li>
}

function EntityOccasionList({occasions=[], worldid='', entityid='', ... props}){
	const fn = (prps) => (<EntityOccasionListItem {... prps} worldid={worldid} entityid={entityid}/> );
	return <RelatedList fn={fn} list={occasions} divId="entity occasions" title="Occasions" />; 
}

function EntityEvents({events, id, worldid}){
	return(
		<div id="eventblock">
			<h2>Events</h2> 
			<Event_List events={events} 
									linking_entity_id={id} 
									worldid={worldid}/>
		</div>
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
			<EntityPositionList entity_positions={items.entity_positions} worldid={worldid}/>
			<EntitySiteList sites={items.sites} worldid={worldid} />
			<EntityOccasionList occasions={items.occasions} entityid={id} worldid={worldid} />
			<EntityEvents events={this.state.events} id={id} worldid={worldid} />
			</div>
		)

	}



}


export default Entity;
