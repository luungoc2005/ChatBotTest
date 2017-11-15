import styled from 'styled-components';
import {Button} from 'rebass';

export const BaseButton = styled(Button)`
  color: #fff;
  border-radius: 1px;
  padding: .78571429em 1.5em .78571429em;
  min-width: 105px;

  &:focus,
  &:hover {
    box-shadow: initial;
  }

  &:active {
    box-shadow: initial;
  }
`

export const GreenButton = styled(BaseButton)`
  background-color: #21ba45;
  &:focus,
  &:hover {
    background-color: #16ab39;
  }
  &:active {
    background-color: #198f35;
  }
`

export const TealButton = styled(BaseButton)`
  background-color: #00b5ad;
  &:focus,
  &:hover {
    background-color: #009c95;
  }
  &:active {
    background-color: #00827c;
  }
`

export const RedButton = styled(BaseButton)`
  background-color: #db2828;
  &:focus,
  &:hover {
    background-color: #d01919;
  }
  &:active {
    background-color: #b21e1e;
  }
`