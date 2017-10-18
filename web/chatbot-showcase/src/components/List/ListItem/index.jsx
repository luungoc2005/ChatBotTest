import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const ListItem = ({className, children, selectable}) => {
  return (
    <li className={className}>
      {children}
    </li>
  );
};

ListItem.propTypes = {
  className: PropTypes.string,
  children: PropTypes.node,
  selectable: PropTypes.bool,
}

export default styled(ListItem)`
  padding: 12px 24px;
  ${props => props.selectable && `
    cursor: default;
    &:hover {
      background-color: rgba(0,0,0,0.05);
    }
  `}
`;