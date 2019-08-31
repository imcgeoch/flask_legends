import React from 'react';
//import logo from './logo.svg';
import './App.css';
const axios = require('axios');


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

function App() {
  return (
    <div className="App">
		  My Edits
		<MyComponent />
		</div>
  );
}

export default App;
