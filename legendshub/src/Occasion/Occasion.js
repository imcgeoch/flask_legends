import React from 'react';
import Event from "../Events/Event.js"
import EntityLink from "../Entity/Entity_Link.js"

const axios = require('axios');

function OccasionIntroEvent({event, name, worldid, entityid, entity_name}){
	return ( <div> 
		<Event {... event} worldid={worldid} />
		In recognition of this event, the festival {name} was celebrated 
		by <EntityLink entity_name={entity_name} entity_id={entityid} worldid={worldid}/>.
	</div>)
}

function OccasionIntroNoEvent({name, entityid, worldid, entity_name}){
	return ( <div> 
		{name} was a festival celebrated 
		by <EntityLink entity_name={entity_name} entity_id={entityid} worldid={worldid}/>.
	</div>)
}

function FeaturesSchedule({type, features=[]}){
	if (features.length > 0){
		return (
			<li>
				A {type} featuring:
				<ul> {features.map((feature) =>(<OccasionItem {... feature} />))} </ul>
			</li>
		)
	}
	return <li> A {type} </li>
}

function OccasionItem({type, dance_form, musical_form, 
	                     poetic_form, event, features }){
	switch (type) {
		case 'ceremony':
		case 'procession':
			return <FeaturesSchedule features={features} type={type} />
		case 'dance performance':
		case 'dance competition':
			return <li> A {type} of {dance_form.name} </li>
		case 'poetry recital':
		case 'poetry competition':
			return <li> A {type} in the style of {poetic_form.name} </li>
		case 'musical performance':
		case 'musical competition':
			return <li> A {type} of {musical_form.name} </li>
		case 'storytelling':
			return <li> Storytelling of the time when <Event {... event}  /></li>
		case 'foot race':
			return <li> A foot race </li>
		default:
			return <li> {type.charAt(0).toUpperCase() + type.slice(1)} </li>
	}
}

function OccasionDetails({schedules=[], ...items}){
	return( 
		<div>
			{items.event != undefined ? <OccasionIntroEvent {... items} /> 
					: <OccasionIntroNoEvent {... items} />}
					{schedules.length > 0 ? "The festival includes:" : "" }
			<ul>
				{schedules.map((schedule) => (<OccasionItem {... schedule} />))}
			</ul>
		</div>
	)

}

class Occasion extends React.Component {
	constructor(props) {
		super(props);
		this.state = {items : {}};
  }
	
	getFromAPI() {
		const {worldid, entityid, id} = this.props.match.params
		axios.get(`/api/${worldid}/occasion/${entityid}/${id}`)
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
		const params = this.props.match.params
		return( <div> <h1>{items.name}</h1>
				<OccasionDetails {... items} {... params} />
			</div>
		)

	}

}
export default Occasion;
