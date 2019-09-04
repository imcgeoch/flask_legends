import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

function Histfig_Link({hfid, world_id, hf_name, linking_hf_id}){
	if (hfid == linking_hf_id ){
		return hf_name.split(' ')[0]
	}
	else{ 
		return <Link to={`/${world_id}/histfig/${hfid}`}> {hf_name} </Link>
	}
}

export default Histfig_Link;
