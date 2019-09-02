import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

function Entity({ match }) {
	return( <div> <h1>Entity Page</h1>
			<p> World : {match.params.worldid} </p>
			<p> Histfig : {match.params.id} </p>
		</div>
	)
}

export default Entity;
