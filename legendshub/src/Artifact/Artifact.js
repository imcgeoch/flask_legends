import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import HistfigLink from "../Histfig/Histfig_Link";

const axios = require('axios');



function ArtifactDetails({name, item_type, mat}) {
	return( <div id="artifact details"> 
		{name} was a {mat} {item_type}. 
		</div>
	)
}

function WrittenContent({written_content, worldid}) {
	if(written_content){
		const { title, form, author_name, author_hfid, styles} = written_content;
		const authorProps = { hf_name:author_name, hfid:author_hfid, worldid:worldid };
		return ( 
			<div id="written content">
				It contains a {form} called {title} by <HistfigLink {... authorProps} />. 
					The writing is {styles}. 
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
			<WrittenContent written_content={items.written_content} worldid={worldid}/>
			</div>
		)

	}

}

export default Artifact;
