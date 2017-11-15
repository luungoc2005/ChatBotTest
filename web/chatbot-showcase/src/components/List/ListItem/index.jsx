import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import {Close} from 'rebass';

const DeleteButton = styled(Close)`
  position: absolute;
  right: 8px;
  z-index: 1;
  top: 50%;
  transform: translateY(-50%);
  color: inherit;
  border-radius: 3px;
  opacity: 0.8;
  
  &:focus,
  &:hover {
    color: inherit;
    background-color: rgba(0,0,0,.2);
    box-shadow: initial;
  }

  &:active {
    color: inherit;
    background-color: rgba(0,0,0,.3);
    box-shadow: initial;
  }
`

const ListItem = ({className, children, selectable, deletable, onDelete}) => {
  return (
    <li className={className}>
      {children}
      {deletable && <DeleteButton onClick={() => { if (onDelete) onDelete() }} />}
    </li>
  );
};

ListItem.propTypes = {
  className: PropTypes.string,
  children: PropTypes.node,
  selectable: PropTypes.bool,
  deletable: PropTypes.bool,
  onDelete: PropTypes.func,
}

export default styled(ListItem)`
  position: relative;
  padding: 12px 24px;
  color: white;
  ${props => props.selectable && `
    cursor: default;
    &:hover {
      color: #333;
      background-color: white;
      box-shadow: 0px 5px 30px 0px rgba(0,0,0,0.5);
    }
  `}
`;