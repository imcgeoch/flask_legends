import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import Event from "../Events/Event"

function Event_List({events=[], ...props}){
	return(
		<ul>
			{
				events.map((event) => (
					<li id={event.id}> <Event {...event} {...props} /> </li>
				))
			}
		</ul>
	);
}

export default Event_List;
