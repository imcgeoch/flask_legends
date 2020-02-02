import React from 'react';
import EntityLink from "../Entity/Entity_Link";
import SiteLink from "../Site/SiteLink";
import HistfigLink from "../Histfig/Histfig_Link";
import EventColLink from "./EventColLink";
import Event from "../Events/Event";

const axios = require('axios');

function Generals({side, generals}){
	if (generals.length > 0) {
		return (
			<div>
				<h3>{side} Generals</h3>
				<ul>
					{generals.map((general)=>(<li><HistfigLink {... general} /></li>))} 
				</ul>
			</div>
		);
	}
	else return null
}

function Squads({side, squads}){
	if (squads.length > 0) {
		return (
			<div>
				<h3>{side} Squads</h3>
				<ul>
					{squads.map(({number, race, site, deaths})=>
						(<li>
							{number} {race} from <SiteLink {... site} /> ({deaths} casualties)
						 </li>))} 
				</ul>
			</div>
		);
	}
	else return null
}

function Duels({duels}){
	if (duels.length > 0){
		return (
			<span>
				<h3> Duels </h3>
				{duels.map((duel, i) => 
					(<span><EventColLink {...duel} name={i+1} /> </span>))}
			</span>
		);
	}
	return null;
}

function Conquest({start_year, war, site, aggressor, defender, events} ){
	return (
		<div>
			In {start_year}, <EntityLink {... aggressor}/> conquered <SiteLink {...site}/> from <EntityLink {... defender} />.

			The conquest involved the following events:
			<ul>
				{events.map((event)=>(<li><Event {...event} /></li>))}
			</ul>
		</div>
	);
}

function Duel({start_year, events, battle}){
	return (
		<div>
			In {start_year}, a duel was fought 
		  as part of <EventColLink {...battle}/>.

			<h3> Events </h3>
			<ul>
				{events.map((event)=>(<li><Event {...event} /></li>))}
			</ul>
		</div>

	)
}

function Battle(items){
	const {start_year, end_year, name, war, attacking_hfs, defending_hfs,
	  attacking_squads, defending_squads, duels} = items;
	return (
		<div> 
			From {start_year} to {end_year} , {name} was fought as 
			part of <EventColLink {... war}/>.

			<Generals side='Attacking' generals={attacking_hfs} />
			<Squads side='Attacking' squads={attacking_squads} />
			<Generals side='Defending' generals={defending_hfs} />
			<Squads side='Defending' squads={defending_squads} />
			<Duels duels={duels} />

		</div>
	)
}


function War(items){
	const {aggressor, defender, name, start_year, end_year, battles, events} = items;
	return (
		<div>
			From {start_year} to {end_year}, {name} was waged 
			between <EntityLink {... aggressor} /> and <EntityLink {... defender} />.

			<h2>Battles:</h2>
			<ul>
				{battles.map((battle) => (<li><EventColLink {... battle} /></li>))}
		  </ul>
		</div>
	)
}

function EventColDetails(items){
	if (items.type == 'war'){
		return <War {... items} />
	}
	if (items.type == 'battle'){
		return <Battle {... items} />
	}
	if (items.type == 'duel'){
		return <Duel {... items} />
	}
	if (items.type == 'site conquered'){
		return <Conquest {... items} />
	}
	return <div>Event Collection: {items.type}</div> 
}

class EventCol extends React.Component {
	constructor(props) {
		super(props);
		this.state = {items : {}};
  }
	
	getFromAPI() {
		const {worldid, id} = this.props.match.params
		axios.get(`/api/${worldid}/eventcollection/${id}`)
		  .then(response => {
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
			<EventColDetails {... items} />
		</div>
		)

	}

}

export default EventCol;
