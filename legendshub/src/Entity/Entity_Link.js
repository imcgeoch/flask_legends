import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

function Entity_Link({entity_name='', world_id='', entity_id='', 
	                    local_id='', ...props}) {
	if (entity_id === local_id) {
		return {entity_name};
	}
	else {
		return <Link to={`/${world_id}/entity/${entity_id}`}>{entity_name}</Link>;
	}
}

export default Entity_Link;
