import React from 'react';
import { BrowserRouter as Route, Link } from 'react-router-dom';

function ArtifactLink({id, worldid, name_string, linking_artifact_id}){
	if (id === Number(linking_artifact_id)){
		return name_string
	}
	else{ 
		return <Link to={`/${worldid}/artifact/${id}`}>{name_string}</Link>
	}
}

export default ArtifactLink;
