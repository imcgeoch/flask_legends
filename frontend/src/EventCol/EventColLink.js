import React from 'react';
import { BrowserRouter as Route, Link } from 'react-router-dom';

function EventColLink({name='', worldid='', id='', 
	local_id='', ...props}) {
	if (id === local_id) {
		return <div> {name} </div>;
	}
	else {
		return <Link to={`/${worldid}/eventcollection/${id}`}>{name}</Link>;
	}
}

export default EventColLink;
