import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import HistfigLink from "../Histfig/Histfig_Link";
import WrittenContentLink from "../WrittenContent/WrittenContent_Link";

const axios = require('axios');

function ArtifactDescription({type, desc}){
	if (type === 'slab'){
		if (desc === 'the secrets of life and death'){
			return <span> It displays the secrets of life and death.</span>
		}
		return <span> It displays the words "{desc}"</span>
	}
	if (desc != null) {
		return <span> It depicts {desc}.</span>
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

function ArtifactDetails({name, name_string, item_type, mat, item_description}) {
	return( <div id="artifact details"> 
		<ArtifactName name={name} name_string={name_string}/> was a {mat} {item_type}. 
		<ArtifactDescription type={item_type} desc={item_description} /> 
		</div>
	)
}

function Content({written_content, worldid}) {
	if(written_content){
		console.log(written_content)
		return ( 
			<div id="written content">
				It contains the work <WrittenContentLink {... written_content} worldid={worldid} />
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
				//			console.log(response); 
				this.setState( {items : response.data} );
			});
		axios.get(`/api/${worldid}/events?artifact=${id}`)
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
			<ArtifactDetails {... items} />
			<Content written_content={items.written_content} worldid={worldid}/>
			</div>
		)

	}

}

export default Artifact;
