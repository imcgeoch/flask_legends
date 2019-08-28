import React from 'react';
//import logo from './logo.svg';
import './App.css';


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
		fetch("/api/hello")
			.then(res => res.json())
		  .then(
				 (result) => {
					 this.setState({
						 items : result.greeting
					 });
				 },
				(error) => {
					this.setState({
						items : error.message
					});
				}
			)
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
