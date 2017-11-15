import {
  GET_RESPONSE_REQUEST,
  GET_RESPONSE_SUCCESS,
  GET_RESPONSE_FAILURE,
} from './actionTypes';

export function getResponseRequest(text) {
  return {
    type: GET_RESPONSE_REQUEST,
    text,
  }
}

export function getResponseSuccess(payload) {
  return {
    type: GET_RESPONSE_SUCCESS,
    payload,
  }
}

export function getResponseFailure(payload) {
  return {
    type: GET_RESPONSE_FAILURE,
    payload,
  }
}