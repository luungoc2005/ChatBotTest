import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {connect} from 'react-redux';
import {TealInput} from '../components/Input';
import {getResponseRequest} from './actions';

export class HomePage extends Component {
  static propTypes = {
    getResponseRequest: PropTypes.func,
    response: PropTypes.string,
  }

  constructor() {
    super();
    this.state = {
      input: ''
    }
  }

  handleKeyPress(event) {
    if (event.key === 'Enter') {
      event.preventDefault();
      this.props.getResponseRequest(this.state.input);
      this.setState({input: ''});
    }
  }
  render() {
    return (
      <div>
        <TealInput 
          value={this.state.input} 
          onChange={(event) => this.setState({input: event.target.value})}
          onKeyPress={(event) => this.handleKeyPress(event)}
        />
        <pre>{this.props.response}</pre>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    response: state.home.response.payload
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    getResponseRequest: (text) => dispatch(getResponseRequest(text))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(HomePage)