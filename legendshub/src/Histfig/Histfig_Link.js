import React from 'react';
import { BrowserRouter as Route, Link } from 'react-router-dom';

function HistfigLink({hfid, worldid, hf_name, linking_hf_id}){
	if (hfid === Number(linking_hf_id)){
		return hf_name.split(' ')[0]
	}
	else{ 
		return <Link to={`/${worldid}/histfig/${hfid}`}>{hf_name}</Link>
	}
}

export default HistfigLink;
