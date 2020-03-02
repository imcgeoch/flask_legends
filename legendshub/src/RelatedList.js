import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

function RelatedList({divId, title, list, fn}){
	return(
		<div id={divId}>
		  <h2>{title}</h2>
				<ul>{list.map(fn)}</ul>
		</div>
	);
}

export default RelatedList;
