import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import Entity_Link from "../Entity/Entity_Link";

import Event from "../Events/Event"
import Event_List from "../Events/Event_List"


const axios = require('axios');

function StringList({items=[], ...props}){
	const listItems = items.map((item) => 
		<li key={item}>{item}</li>
	);
	return <ul>{listItems}</ul>;
}

function Entity_Link_List({entity_links=[], world_id='', ...props}){
	return(
		<ul>
			{
				entity_links.map(({type, ...props}) => 
				(<li key={props.entity_id}> <Entity_Link {...props} world_id={world_id} />: {type} </li>))
			}
		</ul>
	);
}

class Histfig_Inner extends React.Component {
	constructor(props) {
		super(props);
		this.state = {items : {}};
	}


  getFromAPI() {
		let worldid = this.props.worldid;
		let id = this.props.id;
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
		if (this.props.id !== prevProps.id ){
			this.getFromAPI();
		}
	}

	render() {
		return( <div> <h1>Histfig Page</h1>
			<p> World : {this.props.worldid} </p>
				<p> Histfig : {this.props.id} </p>
			<p> Pronoun : {this.state.items.pronoun} </p>
			<p> Name: {this.state.items.name} </p>
			Goals: <StringList items={this.state.items.goals} />
			Entity_Links: <Entity_Link_List entity_links={this.state.items.entity_links} 
				world_id={this.worldid} />
			Events: <Event_List events={this.state.events} 
			         linking_hf_id={this.props.id} 
			         world_id={this.props.worldid}/>
			</div>
		);
	}

}

function Histfig(props) {
	return <Histfig_Inner worldid={props.match.params.worldid} id={props.match.params.id} />
}

export default Histfig;
