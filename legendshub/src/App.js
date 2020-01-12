import React from 'react';
//import './App.css';
import Histfig from './Histfig/Histfig';
import Entity from './Entity/Entity';
import Artifact from './Artifact/Artifact';
import Site from './Site/Site';
import Occasion from './Occasion/Occasion';
import WrittenContent from './WrittenContent/WrittenContent';
import LegendsIndex from './LegendsIndex';
import { BrowserRouter as Router, Route } from 'react-router-dom';

//const axios = require('axios');

/*
class MyComponent extends React.Component {

  constructor(props) {
		super(props)
		this.state = {
			error: null,
			isLoaded: false,
			items: "hey" 
		};
	}

	componentDidMount() {
		axios.get("/api/hello")
		  .then(response => {console.log(response); 
				this.setState({ items : response.data.greeting });
		});
	}

	render () {
		const {items} = this.state;
    return <div> {items} </div>
	}
}
*/

function AppRouter() {
	return (
		<Router>
			<div>
				<Route path="/" exact component={LegendsIndex} />
				<Route path="/:worldid/histfig/:id" component={Histfig} />
				<Route path="/:worldid/entity/:id" component={Entity} />
				<Route path="/:worldid/artifact/:id" component={Artifact} />
				<Route path="/:worldid/site/:id" component={Site} />
				<Route path="/:worldid/occasion/:id" component={Occasion} />
				<Route path="/:worldid/written_content/:id" component={WrittenContent} />
			</div>
		</Router>
	);
}


function App() {
  return (
    <div className="App">
		<AppRouter />
		</div>
  );
}

export default App;
