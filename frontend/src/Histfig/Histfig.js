import React from 'react';
//import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import EntityLink from "../Entity/Entity_Link";

//import Event from "../Events/Event"
import Event_List from "../Events/Event_List"

import HistfigLink from "./Histfig_Link"

import axios from "axios";

function StringList({items=[], ...props}){
	const listItems = items.map((item) => 
		<li key={item}>{item}</li>
	);
	return <ul>{listItems}</ul>;
}

function Entity_Link_List({entity_links=[], worldid='', ...props}){
	return(
		<ul>
			{
				entity_links.map(({type, ...props}) => 
				(<li key={props.entity_id}> <EntityLink {...props} worldid={worldid} />: {type} </li>))
			}
		</ul>
	);
}

function HF_Link_List({hf_links=[], worldid='', ...props}){
	return(
		<ul>
			{
				hf_links.map(({type, ...props}) => 
					(<li key={props.id}> <HistfigLink {...props} worldid={worldid}/>: {type} </li>))
			}
		</ul>
	)
}

function HF_Vitals({caste, race, birth_year, death_year, deity, force}){
	return(
			<div id="vitalstatistics">
				{caste} {race}, born {birth_year} {death_year !== -1 && 'died ' + death_year }
				</div>
	);
}

function HF_Supernatural({deity=false, force=false, spheres=[]}){
	if (deity || force || spheres.length > 0){
		return(
			<div id="supernatural">
				{deity && "A deity "}{force && "A force of nature " } 
				{spheres.length > 0 &&  "associated with " + spheres.join()}.

			</div>
		);
	}
	else 
		return (<div id="supernatural"> </div>);
}


function HF_Goals({goals}){
	return(
		<div><h2>Goals</h2> <StringList items={goals}/></div>
	);
}

function HF_Entity_Links(props){
	return(
		<div id="entitylinkblock">
					<h2>Entity Links</h2> 
					<Entity_Link_List {... props} />
		</div>
	);
}

function HF_HF_Links(props){
	return(
		<div id="entitylinkblock">
					<h2>Histfig Links</h2> 
					<HF_Link_List {... props} />
		</div>
	);
}

function HF_Events({events, id, worldid}){
	return(
		<div id="eventblock">
			<h2>Events</h2> 
			<Event_List events={events} 
									linking_hf_id={id} 
									worldid={worldid}/>
		</div>
	);
}

class Histfig extends React.Component {
	
	constructor(props) {
		super(props);
		this.state = {items : {}};
	}

  getFromAPI() {
		let worldid = this.props.match.params.worldid;
		let id = this.props.match.params.id;
		axios.get(`/api/${worldid}/histfig/${id}`)
		  .then(response => {
				console.log(response); 
				this.setState( {items : response.data} );
			});
		axios.get(`/api/${worldid}/events?hf=${id}`)
		  .then(response => {
				console.log(response); 
				this.setState( {events : response.data} );
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
		const {name, entity_links, hf_links} = this.state.items;
		const events = this.state.events;
		const {id, worldid} = this.props.match.params;
		return( 
			<div id="histfig"> 
				<h1>{name}</h1>
					<HF_Vitals {... this.state.items} />
			<HF_Supernatural {... this.state.items} />
			  <HF_Goals {... this.state.items} />
			  <HF_HF_Links hf_links={hf_links} worldid={worldid}/>
				<HF_Entity_Links entity_links={entity_links} worldid={worldid} />
			  <HF_Events events={events} id={id} worldid={worldid} />
			</div>
		);
	}
}
export default Histfig;
