import {takeLatest, call, put} from 'redux-saga/effects';
import apiRequest from '../utils/apiRequest';
import {
  GET_RESPONSE_REQUEST,
} from './actionTypes';
import {
  getResponseSuccess,
  getResponseFailure,
} from './actions';

export function* fetchResponse(action) {
  if (action.text) {
    try {
      const resp = yield call(apiRequest, `/api/examples/?query=${encodeURIComponent(action.text)}`, 'get');
      yield put(getResponseSuccess(JSON.stringify(resp, null, 4)))
    }
    catch (error) {
      yield put(getResponseFailure(error))
    }
  }
}

export function* watchResponseRequest() {
  yield takeLatest(GET_RESPONSE_REQUEST, fetchResponse);
}

export function* homeSagas() {
  yield call(watchResponseRequest)
}