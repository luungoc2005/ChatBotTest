import {homeSagas} from './HomePage/sagas';
import {call} from 'redux-saga/effects'

export function* rootSaga() {
  yield call(homeSagas);
}