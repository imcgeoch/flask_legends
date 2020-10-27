import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import HistfigLink from "../Histfig/Histfig_Link";
import SiteLink from "../Site/SiteLink";
import Event from "../Events/Event.js"
import WrittenContentLink from "./WrittenContent_Link";
import MusicalFormLink from "../MusicalForm/MusicalFormLink";
import DanceFormLink from "../DanceForm/DanceFormLink";
import PoeticFormLink from "../PoeticForm/PoeticFormLink";

import axios from "axios";

function WritingStyle({styles}){
	if (styles != ''){
		return <span>The writing is {styles}.</span>
	}
	else return null
}

function WrittenContentDetails(items){
		const authorProps = { hf_name:items.author_name, 
			                    hfid:items.author_hfid, 
			                    worldid:items.worldid };
	return(
	<div>
	  {items.title} is a {items.form}. It was written by <HistfigLink {... authorProps} />.
		<WritingStyle styles={items.styles}/>
	</div>
	)
}

function WrittenContentReferences({worldid = '', subj_hf=[], subj_evt=[], subj_site=[],
	                                 subj_artifact=[], subj_entity=[], subj_region=[], 
	                                 subj_wc=[], subj_poetic=[], subj_dance=[], 
	                                 subj_musical=[]}){
	return (
		<div>
			<ul>
				{subj_hf.map((hfprops) => 
					 <li> It concerns <HistfigLink {... hfprops} worldid={worldid} />.</li>)}
				{subj_evt.map((eventprops) => 
					 <li> It concerns the event where <Event {... eventprops} worldid={worldid}/></li>)}
				{subj_site.map((siteprops) => 
					 <li> It concerns <SiteLink {... siteprops} worldid={worldid}/></li>)}
				{subj_artifact.map((artifactprops) => 
					 <li> It concerns artifact {artifactprops.id} </li>)}
				{subj_entity.map((entityprops) => 
					 <li> It concerns entity {entityprops.id} </li>)}
				{subj_region.map((regionprops) => 
					 <li> It concerns region {regionprops.id} </li>)}
				{subj_wc.map((wcprops) => 
					<li> It concerns the work <WrittenContentLink {... wcprops} /> </li>)}
				{subj_poetic.map((poeticprops) => 
					<li> It concerns poetic form <PoeticFormLink {... poeticprops} worldid={worldid} /> </li>)}
				{subj_dance.map((danceprops) => 
					<li> It concerns dance form <DanceFormLink {... danceprops} worldid={worldid}/> </li>)}
				{subj_musical.map((musicalprops) => 
					<li> It concerns musical form <MusicalFormLink {... musicalprops} worldid={worldid}/> </li>)}
			</ul>
		</div>
	)
}

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
		
		return( <div> <h1>{items.title}</h1>
			<WrittenContentDetails {... items} worldid={worldid} />
			<WrittenContentReferences {... items} worldid={worldid} />
			</div>
		)

	}

}

export default WrittenContent;
