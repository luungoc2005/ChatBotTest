import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const List = ({className, children, selectable}) => {
  return (
    <ul className={className}>
      {children && children.map((child) => React.cloneElement(child, {selectable}))}
    </ul>
  );
};

List.propTypes = {
  className: PropTypes.string,
  children: PropTypes.node,
  selectable: PropTypes.bool,
  border: PropTypes.bool,
}

export default styled(List)`
  list-style-type: none;
  margin: 0px;
  padding: 0px;
  color: #333;
  ${props => props.border && `
    li {
      border-top: 1px solid rgba(0,0,0,0.15);
      &:last-child {
        border-bottom: 1px solid rgba(0,0,0,0.15);
      }
    }
  `}
`;