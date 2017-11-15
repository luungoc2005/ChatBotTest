
import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const PortalBase = ({active, children, ...ownProps}) => 
  <div {...ownProps}>{active && children}</div>

PortalBase.propTypes = {
  active: PropTypes.bool,
  children: PropTypes.node,
}

PortalBase.defaultProps = {
  active: false,
}

export const Portal = styled(PortalBase)`
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,.6);
  transition: opacity 0.35s ease-in-out 0.2s;
  z-index: 5;
  align-items: center;
  justify-content: center;
  opacity: ${props => props.active ? `1` : `0`};
  display: ${props => props.active ? `flex`: `none`};
  div {
    max-width: 96vw;
    max-height: 96vh;
    transition: transform .15s ease-in-out .5s;
    transform: translateY(${props => props.active ? `0` : `-110%`});
  }
`

export default Portal;