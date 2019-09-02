import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import Entity_Link from "../Entity/Entity_Link";


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
				(<li> <Entity_Link {...props} world_id={world_id} />: {type} </li>))
			}
		</ul>
	);
}

class Histfig extends React.Component {

	constructor(props) {
		super(props);
		this.state = {items : {}};
	}
	
	componentWillMount() {
		let worldid = this.props.match.params.worldid;
		let id = this.props.match.params.id;
		axios.get(`/api/${worldid}/histfig/${id}`)
		  .then(response => {
				console.log(response); 
				this.setState( {items : response.data} );
		});
	}

	render() {
		return( <div> <h1>Histfig Page</h1>
				<p> World : {this.props.match.params.worldid} </p>
				<p> Histfig : {this.props.match.params.id} </p>
			  <p> Pronoun : {this.state.items.pronoun} </p>
			  <p> Name: {this.state.items.name} </p>
			  Goals: <StringList items={this.state.items.goals} />
			  Entity_Links: <Entity_Link_List entity_links={this.state.items.entity_links} 
			                                  world_id={this.props.match.params.worldid} />
			</div>
		);
	}
}

export default Histfig;
