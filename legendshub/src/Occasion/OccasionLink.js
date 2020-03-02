import React from 'react';
import { BrowserRouter as Route, Link } from 'react-router-dom';

function OccasionLink({name='', worldid='', id='', entityid='', local_id=''}) {
	if (id === local_id) {
		return <div> {name} </div>;
	}
	else {
		return <Link to={`/${worldid}/occasion/${entityid}/${id}`}>{name}</Link>;
	}
}

export default OccasionLink;
