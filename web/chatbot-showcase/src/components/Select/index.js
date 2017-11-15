import styled from 'styled-components';
import {Select} from 'rebass';

export const BaseSelect = styled(Select)`
  position: relative;
  select {
    padding: 8px;
    outline: none;
    box-shadow: 0 0 0 1px rgba(34,36,38,.15) inset;
    background: white;
    &:focus {
      box-shadow: 0 0 0 1px rgba(34,36,38,.35) inset;
    }
  }
`
export const TealSelect = styled(BaseSelect)`
  select {
    box-shadow: 0 0 0 1px #008c86 inset;
    &:focus {
      box-shadow: 0 0 0 1px #00b5ad inset;
    }
  }
`