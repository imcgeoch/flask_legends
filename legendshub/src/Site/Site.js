import React from 'react';
//import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

function Site({ match }) {
	return( <div> <h1>Site Page</h1>
			<p> Site: {match.params.worldid} </p>
			<p> Site: {match.params.id} </p>
		</div>
	)
}

export default Site;
