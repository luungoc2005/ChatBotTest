import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

/// Generators polyfill for redux-saga.
window.regeneratorRuntime = require("regenerator-runtime");

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
