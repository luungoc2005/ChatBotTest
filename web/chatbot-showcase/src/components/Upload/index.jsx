import React, {PureComponent} from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import {TealButton} from '../Button';

class UploadButtonBase extends PureComponent {
  static propTypes = {
    style: PropTypes.object,
    className: PropTypes.string,
    onChange: PropTypes.func,
  };

  handleUploadClick() {
    if (this.inputElement) {
      this.inputElement.click();
    }
  }

  render() {
    const {className, style, onChange, ...ownProps} = this.props;
    return (
      <div style={style} className={className}>
        <input 
          type='file'
          onChange={(e) => onChange(e)}
          value=''
          {...ownProps}
          ref={element => this.inputElement = element}
        />
        <TealButton onClick={() => this.handleUploadClick()}>
          UPLOAD
        </TealButton>
      </div>
    );
  }
}

export const UploadButton = styled(UploadButtonBase)`
  position: relative;
  display: inline-block;
  input {
    opacity: 0;
    width: 0px;
    height: 0px;
    position: absolute;
  }
`;