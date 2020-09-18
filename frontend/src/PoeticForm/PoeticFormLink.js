import React from 'react';
import { BrowserRouter as Route, Link } from 'react-router-dom';

function PoeticFormLink({name='', worldid='', id='', 
	local_id='', ...props}) {
	if (id === local_id) {
		return <div> {name} </div>;
	}
	else {
		return <Link to={`/${worldid}/poetic_form/${id}`}>{name}</Link>;
	}
}

export default PoeticFormLink;
