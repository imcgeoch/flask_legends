import React from 'react';
//import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

function Artifact({ match }) {
	return( <div> <h1>Artifact Page</h1>
			<p> World : {match.params.worldid} </p>
			<p> Artifact : {match.params.id} </p>
		</div>
	)
}

export default Artifact;
