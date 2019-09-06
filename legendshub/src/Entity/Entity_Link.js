import React from 'react';
import { BrowserRouter as Route, Link } from 'react-router-dom';

function EntityLink({entity_name='', worldid='', entity_id='', 
	                    local_id='', ...props}) {
	if (entity_id === local_id) {
		return {entity_name};
	}
	else {

		return <Link to={`/${worldid}/entity/${entity_id}`}>{entity_name}</Link>;
	}
}

export default EntityLink;
