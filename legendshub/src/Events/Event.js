import React from 'react';
//import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import HfSimpleBattleEvent from './HfSimpleBattleEvent';

function Event(props) {
	if (props.type === 'hf simple battle event')
		return <HfSimpleBattleEvent {...props} />
	else
		return <div> {props.type} </div>
}

export default Event;
