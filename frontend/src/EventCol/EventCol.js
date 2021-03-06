import React from 'react';
import EntityLink from "../Entity/Entity_Link";
import SiteLink from "../Site/SiteLink";
import HistfigLink from "../Histfig/Histfig_Link";
import EventColLink from "./EventColLink";
import OccasionLink from "../Occasion/OccasionLink";
import Event from "../Events/Event";

import axios from "axios";

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

function Occasion({start_year, ordinal, occasion, schedules, ...items}){
	return(
		<div>
			In {start_year}, the {ordinal}st celebration 
			of <OccasionLink {...occasion} /> was held.

			The festival included:
			<ul>
				{schedules.map((schedule) => 
					(<li><EventColLink {...schedule} name={"a " + schedule.type}/></li>))}

			</ul>
		</div>
	);
}

function Schedule({type, year, occasion, event}){
	return(
		<div>
			A {type} was held in {year} as 
			part of <EventColLink {... occasion} name='a festival' />.


			<h3> Events </h3>
			<ul>
				<Event {...event} />
			</ul>
		</div>
	)
}

function Purge({adjective, events=[], year, site}){
	return( 
		<div>
			In {year}, an {adjective} purge happened in <SiteLink {... site}/>. As a result,
			<h3> Events </h3>
			<ul>
				{events.map((event)=>(<li><Event {...event} /></li>))}
			</ul>
		</div>
			);
}

function Journey({events, year, ordinal}){
	return(
		<div>
			In {year}, a historical figure took their {ordinal}st journey.
			<h3> Events </h3>
			<ul>
				{events.map((event)=>(<li><Event {...event} /></li>))}
			</ul>
		</div>
	);
}

function Theft({events, year, duels}){
	return (
		<div>
			In {year}, a theft occured. 
			<h3> Events </h3>
			<ul>
				{events.map((event)=>(<li><Event {...event} /></li>))}
			</ul>
			<h3> Duels </h3>
			<ul>
				{duels.map((duel, i) => 
					(<li><EventColLink {...duel} name={i+1} /> </li>))}
			</ul>
		</div>
	);
}


function EventColDetails(items){
	switch(items.type){
		case 'war':
			return <War {... items} />
		case 'battle':
		  return <Battle {... items} />
		case 'duel':
			return <Duel {... items} />
		case 'site conquered':
			return <Conquest {... items} />
		case 'occasion': 
			return <Occasion {... items} />
		case 'ceremony':
		case 'procession':
		case 'performance':
		case 'competition':
			return <Schedule {... items} />
		case 'purge':
			return <Purge {... items} />
		case 'journey':
			return <Journey {... items} />
    case 'theft':
			return <Theft {... items} />
		default:
				return <div>Event Collection: {items.type}</div>
	}
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
