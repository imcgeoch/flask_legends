import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import Histfig_Link from "../Histfig/Histfig_Link";

function HfSimpleBattleEvent({world_id, hfid, hfid2, hf_name, hf_name2, subtype, linking_hf_id}) {
	const hf1 = {world_id:world_id, hfid:hfid, hf_name:hf_name, linking_hf_id:linking_hf_id};
	const hf2 = {world_id:world_id, hfid:hfid2, hf_name:hf_name2, linking_hf_id:linking_hf_id};
	return (
		<div> <Histfig_Link {...hf1} /> battled <Histfig_Link {...hf2} /> </div>
	)
}

export default HfSimpleBattleEvent;
