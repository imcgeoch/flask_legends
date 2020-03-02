import React from 'react';
import { BrowserRouter as Route, Link } from 'react-router-dom';

function WrittenContentLink({wc_id, worldid, wc_name, linking_wc_id}){
	if (wc_id === Number(linking_wc_id)){
		return wc_name
	}
	else{ 
		return <Link to={`/${worldid}/written_content/${wc_id}`}>{wc_name}</Link>
	}
}

export default WrittenContentLink;
