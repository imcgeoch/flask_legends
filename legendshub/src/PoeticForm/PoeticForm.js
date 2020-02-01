import React from 'react';

const axios = require('axios');

function PoeticFormDetails({description=''}){
	return (<div>
		{description.split('[B]').map((item, key) => (
			<p>{item}</p>))} 
		</div>);
}


class PoeticForm extends React.Component {
	constructor(props) {
		super(props);
		this.state = {items : {}};
  }

	getFromAPI() {
		const {worldid, id} = this.props.match.params
		axios.get(`/api/${worldid}/poeticform/${id}`)
		  .then(response => {
				//			console.log(response); 
				this.setState( {items : response.data} );
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
			<PoeticFormDetails {... items} />
			</div>
		)

	}

}

export default PoeticForm;
