import React, {Component} from 'react';
import HomePage from './HomePage'
import {Provider} from 'react-redux';
import {configureStore} from './store';


class App extends Component {
  componentWillMount() {
    this.store = configureStore();
  }
  render() {
    return (
      <div className="App">
        <Provider store={this.store}>
          <HomePage />
        </Provider>
      </div>
    );
  }
}

export default App;
