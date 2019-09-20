import React from 'react';
//import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

function Occasion({ match }) {
	return( <div> <h1>Occasion Page</h1>
			<p> Occasion: {match.params.worldid} </p>
			<p> Occasion: {match.params.id} </p>
		</div>
	)
}

export default Occasion;
