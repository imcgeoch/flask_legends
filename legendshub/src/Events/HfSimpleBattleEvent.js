import React from 'react';
//import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import HistfigLink from "../Histfig/Histfig_Link";

function HfSimpleBattleEvent({world_id, hfid, hfid2, hf_name, hf_name2, subtype, linking_hf_id}) {
	const hf1 = {world_id:world_id, hfid:hfid, hf_name:hf_name, linking_hf_id:linking_hf_id};
	const hf2 = {world_id:world_id, hfid:hfid2, hf_name:hf_name2, linking_hf_id:linking_hf_id};
	return (
		<div> <HistfigLink {...hf1} /> battled <HistfigLink {...hf2} /> </div>
	)
}

export default HfSimpleBattleEvent;
