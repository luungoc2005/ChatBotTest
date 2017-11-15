import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const TableBase = ({className, border, children, ...ownProps}) => (
  <table className={className} {...ownProps}>
    <tbody>
      {children}
    </tbody>
  </table>
)

TableBase.propTypes = {
  className: PropTypes.string,
  border: PropTypes.bool,
  children: PropTypes.node,
}

const Table = styled(TableBase)`
  table-layout: fixed;
  margin: 0px;
  padding: 0px;
  padding: 0px;
  color: #333;
  width: 100%;
  font-weight: inherit;
  border-collapse: collapse;
  border-spacing: 0;
  overflow: auto;
  ${props => props.border && `
  li {
      border-top: 1px solid rgba(0,0,0,0.15);
      &:last-child {
        border-bottom: 1px solid rgba(0,0,0,0.15);
      }
    }
  `}
`

const TableRow = styled.tr`
  color: white;
  box-shadow: 0px 5px 30px 0px transparent;
  &:hover {
    color: #333;
    background-color: white;
    box-shadow: 0px 5px 30px 0px rgba(0,0,0,0.5);
  }
`

const TableCell = styled.td`
  padding: 12px 24px;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  select {
    color: initial;
  }
`

const HeaderRow = styled.tr`
  padding: 0px;
  background-color: #00b5ad;
  color: white;
  text-align: left;
`

const HeaderCell = styled.th`
  padding: 12px 24px;
  font-weight: inherit;
  text-transform: uppercase;
  text-overflow: ellipsis;
`

export {Table, TableRow, TableCell, HeaderRow, HeaderCell}