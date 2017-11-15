import styled from 'styled-components';
import {Input} from 'rebass';

export const BaseInput = styled(Input)`
  position: relative;
  box-shadow: 0 0 0 1px rgba(34,36,38,.15) inset;
  background: white;
  &:focus {
    box-shadow: 0 0 0 1px rgba(34,36,38,.35) inset;
  }
`

export const TealInput = styled(Input)`
  position: relative;
  box-shadow: 0 0 0 1px #008c86 inset;
  background: white;
  &:focus {
    box-shadow: 0 0 0 1px #00b5ad inset;
  }
`