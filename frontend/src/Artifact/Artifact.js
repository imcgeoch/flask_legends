import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import HistfigLink from "../Histfig/Histfig_Link";
import SiteLink from "../Site/SiteLink";
import WrittenContentLink from "../WrittenContent/WrittenContent_Link";

import axios from "axios"

function ArtifactDescription({item_type, item_description}){
	const {type, desc} = {item_type, item_description};
	if (type === 'slab'){
		if (desc === 'the secrets of life and death'){
			return <span> It displays the secrets of life and death.</span>
		}
		return <span> It reads, "{desc}"</span>
	}
	if (desc != null) {
		return <span> It depicts {desc}.</span>
	}
	return null
}

function ArtifactLocation(items){
	if (items.holder != null) {
		return <span> It is in the posession of <HistfigLink {... items.holder}/></span>
	}
	if (items.site != null) {
		// add structure one day? Not in model at the moment.
		return <span> It is stored in <SiteLink {... items.site} /> </span>
	}
	return null
}

function ArtifactName({name, name_string}){
	if (name_string === ""){
		return <span> {name} </span>
	}
	else{
		return <span> {name}, "{name_string}"</span>
	}
}

function ArtifactDetails(items) {
	const {mat, item_type} = items;
	return( <div id="artifact details"> 
		<ArtifactName {... items}/> was a {mat} {item_type}. 
		<ArtifactDescription {... items} />
		<ArtifactLocation {... items} />
		</div>
	)
}

function Content(items) {
	const {written_content, worldid} = items;
	if(written_content){
		written_content.worldid = worldid;
		return ( 
			<div id="written content">
				It contains the work <WrittenContentLink {... written_content} />
			</div>
		);
	}
	return (<div id="written content" />);
}

class Artifact extends React.Component {
	constructor(props) {
		super(props);
		this.state = {items : {}};
  }

	getFromAPI() {
		const {worldid, id} = this.props.match.params
		axios.get(`/api/${worldid}/artifact/${id}`)
		  .then(response => {
				this.setState( {items : response.data} );
			});
		axios.get(`/api/${worldid}/events?artifact=${id}`)
		  .then(response => {
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
		items.worldid = worldid;
		
		return( <div> <h1>{items.name}</h1>
			<ArtifactDetails {... items} />
			<Content {... items}/>
			</div>
		)

	}

}

export default Artifact;
